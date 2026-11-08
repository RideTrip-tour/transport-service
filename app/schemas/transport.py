from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LATITUDE,
    MAX_LIMIT,
    MAX_LONGITUDE,
    MIN_DISTANCE,
    MIN_ID,
    MIN_LATITUDE,
    MIN_LEN_CODE,
    MIN_LEN_DIRECTION,
    MIN_LEN_LANG,
    MIN_LEN_STATION,
    MIN_LEN_TIMEZONE,
    MIN_LIMIT,
    MIN_LONGITUDE,
    MIN_OFFSET,
)
from app.utils.enums import CodingSystem, ScheduleEvent, ShowSystems, TransportType


class BaseTransportParams(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class BaseCodingParams(BaseTransportParams):
    system: CodingSystem | None = None


class BaseSystemsParams(BaseCodingParams):
    show_systems: ShowSystems | None = None


class BaseTimezoneParams(BaseSystemsParams):
    result_timezone: str | None = Field(
        default=None,
        min_length=MIN_LEN_TIMEZONE,
    )


class BasePaginationParams(BaseTransportParams):
    limit: int = Field(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT)
    offset: int = Field(default=DEFAULT_OFFSET, ge=MIN_OFFSET)


class BaseCoordinatesParams(BaseTransportParams):
    lat: float = Field(ge=MIN_LATITUDE, le=MAX_LATITUDE)
    lng: float = Field(ge=MIN_LONGITUDE, le=MAX_LONGITUDE)
    distance: int = Field(ge=MIN_DISTANCE)


class TransportSearchParams(
    BaseTimezoneParams,
    BasePaginationParams,
):
    from_location_id: int | None = Field(default=None, ge=MIN_ID)
    to_location_id: int | None = Field(default=None, ge=MIN_ID)
    from_code: str | None = Field(default=None, min_length=MIN_LEN_CODE)
    to_code: str | None = Field(default=None, min_length=MIN_LEN_CODE)
    date: Date
    transport_types: list[TransportType] | None = None

    @model_validator(mode="after")
    def validate_location_ids(self):
        if (self.from_location_id is None) != (self.to_location_id is None):
            raise ValueError("Both from_location_id and to_location_id are required")
        return self

    @model_validator(mode="after")
    def validate_codes(self):
        if (self.from_code is None) != (self.to_code is None):
            raise ValueError("Both from_code and to_code are required")
        return self

    @model_validator(mode="after")
    def validate_route_source(self):
        has_location_ids = self.from_location_id is not None
        has_codes = self.from_code is not None
        if has_location_ids == has_codes:
            raise ValueError("Provide either location IDs or station codes")
        return self


class ScheduleParams(BaseTimezoneParams, BasePaginationParams):
    station: str = Field(min_length=MIN_LEN_STATION)
    date: Date | None = None
    transport_types: list[TransportType] | None = None
    event: ScheduleEvent = ScheduleEvent.DEPARTURE
    direction: str | None = Field(default=None, min_length=MIN_LEN_DIRECTION)

    @model_validator(mode="after")
    def validate_direction(self):
        if self.direction is not None and (
            self.transport_types is None
            or TransportType.SUBURBAN not in self.transport_types
        ):
            raise ValueError("Direction is only available for suburban transport")
        return self


class ThreadParams(BaseTimezoneParams):
    date: Date | None = None


class NearestStationsParams(BaseCoordinatesParams):
    transport_types: list[TransportType] | None = None


class NearestSettlementParams(BaseCoordinatesParams):
    pass


class CarrierParams(BaseCodingParams):
    pass


class StationsParams(BaseSystemsParams):
    station_types: list[str] | None = None
    transport_types: list[TransportType] | None = None
    lang: str | None = Field(default=None, min_length=MIN_LEN_LANG)
