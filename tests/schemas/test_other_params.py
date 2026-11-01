import pytest
from pydantic import ValidationError

from app.schemas.transport import (
    CarrierParams,
    NearestSettlementParams,
    NearestStationsParams,
    StationsParams,
    ThreadParams,
)

COORDINATE_SCHEMAS = [
    NearestStationsParams,
    NearestSettlementParams,
]


class TestCoordinatesParams:
    @pytest.mark.parametrize("schema", COORDINATE_SCHEMAS)
    def test_valid_coordinates(self, schema, nearest_params):
        params = schema(**nearest_params)

        assert params.lat == 55.7558
        assert params.lng == 37.6173
        assert params.distance == 50

    @pytest.mark.parametrize("schema", COORDINATE_SCHEMAS)
    @pytest.mark.parametrize("lat", [-90, 90, 0, 55.7558])
    def test_valid_latitude(self, schema, nearest_params, lat):
        params = schema(**{**nearest_params, "lat": lat})

        assert params.lat == lat

    @pytest.mark.parametrize("schema", COORDINATE_SCHEMAS)
    @pytest.mark.parametrize("lat", [-90.1, 90.1, -91, 91])
    def test_invalid_latitude(self, schema, nearest_params, lat):
        with pytest.raises(ValidationError):
            schema(**{**nearest_params, "lat": lat})

    @pytest.mark.parametrize("schema", COORDINATE_SCHEMAS)
    @pytest.mark.parametrize("lng", [-180, 180, 0, 37.6173])
    def test_valid_longitude(self, schema, nearest_params, lng):
        params = schema(**{**nearest_params, "lng": lng})

        assert params.lng == lng

    @pytest.mark.parametrize("schema", COORDINATE_SCHEMAS)
    @pytest.mark.parametrize("lng", [-180.1, 180.1, -181, 181])
    def test_invalid_longitude(self, schema, nearest_params, lng):
        with pytest.raises(ValidationError):
            schema(**{**nearest_params, "lng": lng})

    @pytest.mark.parametrize("schema", COORDINATE_SCHEMAS)
    @pytest.mark.parametrize("distance", [0, -1])
    def test_invalid_distance(self, schema, nearest_params, distance):
        with pytest.raises(ValidationError):
            schema(**{**nearest_params, "distance": distance})

    @pytest.mark.parametrize(
        "schema",
        COORDINATE_SCHEMAS,
    )
    @pytest.mark.parametrize(
        "missing_field",
        ["lat", "lng", "distance"],
    )
    def test_required_fields(self, schema, nearest_params, missing_field):
        payload = {
            key: value for key, value in nearest_params.items() if key != missing_field
        }

        with pytest.raises(ValidationError):
            schema(**payload)


class TestThreadParams:
    def test_valid_empty_params(self):
        params = ThreadParams()

        assert params.date is None
        assert params.show_systems is None
        assert params.result_timezone is None

    def test_valid_date(self, field_date):
        params = ThreadParams(date=field_date)

        assert params.date == field_date


class TestCarrierParams:
    def test_valid_empty_params(self):
        params = CarrierParams()

        assert params.system is None


class TestStationsParams:
    def test_valid_empty_params(self):
        params = StationsParams()

        assert params.station_types is None
        assert params.transport_types is None
        assert params.system is None
        assert params.show_systems is None
        assert params.lang is None

    def test_valid_station_types(self):
        params = StationsParams(station_types=["station", "settlement"])

        assert params.station_types == ["station", "settlement"]

    @pytest.mark.parametrize("lang", ["ru", "en", "ru-RU"])
    def test_valid_lang(self, lang):
        params = StationsParams(lang=lang)

        assert params.lang == lang

    @pytest.mark.parametrize("lang", ["", " ", "a"])
    def test_invalid_lang(self, lang):
        with pytest.raises(ValidationError):
            StationsParams(lang=lang)

    def test_lang_whitespace_is_stripped(self):
        params = StationsParams(lang=" ru ")

        assert params.lang == "ru"
