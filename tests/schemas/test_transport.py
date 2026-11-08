from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.transport import (
    CarrierParams,
    CodingSystem,
    NearestSettlementParams,
    NearestStationsParams,
    ScheduleEvent,
    ScheduleParams,
    ShowSystems,
    StationsParams,
    ThreadParams,
    TransportSearchParams,
    TransportType,
)


@pytest.fixture
def field_date():
    return date(2026, 11, 15)


@pytest.fixture
def location_params(field_date):
    return {
        "from_location_id": 1,
        "to_location_id": 2,
        "date": field_date,
    }


@pytest.fixture
def code_params(field_date):
    return {
        "from_code": "c213",
        "to_code": "c2",
        "date": field_date,
    }


@pytest.fixture
def schedule_params():
    return {
        "station": "s9600213",
    }


@pytest.fixture
def thread_params():
    return {}


@pytest.fixture
def nearest_params():
    return {
        "lat": 55.7558,
        "lng": 37.6173,
        "distance": 50,
    }


class TestTransportSearchParams:
    """Tests for TransportSearchParams schema."""

    def test_valid_with_location_ids(self, location_params):
        params = TransportSearchParams(**location_params)

        assert params.from_location_id == 1
        assert params.to_location_id == 2
        assert params.date == date(2026, 11, 15)

    def test_valid_with_codes(self, code_params):
        params = TransportSearchParams(**code_params)

        assert params.from_code == "c213"
        assert params.to_code == "c2"

    @pytest.mark.parametrize("location_id", ["from_location_id", "to_location_id"])
    def test_location_ids_must_be_provided_together(self, location_params, location_id):
        location_params[location_id] = None

        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)

    @pytest.mark.parametrize("code", ["from_code", "to_code"])
    def test_codes_must_be_provided_together(self, code_params, code):
        code_params[code] = None

        with pytest.raises(ValidationError):
            TransportSearchParams(**code_params)

    def test_location_ids_and_codes_are_mutually_exclusive(
        self, location_params, code_params
    ):
        with pytest.raises(ValidationError):
            TransportSearchParams(**{**location_params, **code_params})

    def test_route_source_is_required(self, field_date):

        with pytest.raises(ValidationError):
            TransportSearchParams(date=field_date)

    def test_date_is_required(self, location_params):
        del location_params["date"]

        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)

    def test_default_pagination(self, location_params):
        params = TransportSearchParams(**location_params)

        assert params.limit == 20
        assert params.offset == 0

    @pytest.mark.parametrize("limit", [0, 101, -1])
    def test_invalid_limit(self, location_params, limit):
        location_params["limit"] = limit
        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)

    @pytest.mark.parametrize("limit", [1, 20, 100])
    def test_valid_limit(self, location_params, limit):
        location_params["limit"] = limit
        params = TransportSearchParams(**location_params)
        assert params.limit == limit

    @pytest.mark.parametrize("offset", [-1, -10])
    def test_invalid_offset(self, location_params, offset):
        location_params["offset"] = offset
        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)

    def test_valid_offset(self, location_params):
        location_params["offset"] = 10
        params = TransportSearchParams(**location_params)
        assert params.offset == 10

    def test_valid_transport_types(self, location_params):
        location_params["transport_types"] = [
            TransportType.PLANE,
            TransportType.TRAIN,
            TransportType.BUS,
        ]
        params = TransportSearchParams(**location_params)
        assert params.transport_types == [
            TransportType.PLANE,
            TransportType.TRAIN,
            TransportType.BUS,
        ]

    def test_invalid_transport_type(self, location_params):
        location_params["transport_types"] = ["invalid"]

        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)

    @pytest.mark.parametrize(
        ("field", "value", "expected"),
        [
            ("system", "yandex", CodingSystem.YANDEX),
            ("system", "iata", CodingSystem.IATA),
            ("show_systems", "all", ShowSystems.ALL),
        ],
    )
    def test_valid_coding_systems(self, location_params, field, value, expected):
        location_params[field] = value
        params = TransportSearchParams(**location_params)
        assert getattr(params, field) == expected

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("system", "invalid"),
            ("show_systems", "invalid"),
        ],
    )
    def test_invalid_coding_systems(self, location_params, field, value):
        location_params[field] = value
        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)


class TestScheduleParams:
    """Tests for ScheduleParams schema."""

    def test_valid_with_required_fields(self, schedule_params):
        params = ScheduleParams(**schedule_params)

        assert params.station == "s9600213"
        assert params.date is None
        assert params.event == ScheduleEvent.DEPARTURE
        assert params.limit == 20
        assert params.offset == 0

    def test_station_is_required(self):
        with pytest.raises(ValidationError):
            ScheduleParams()

    @pytest.mark.parametrize("station", ["", " "])
    def test_invalid_station(self, schedule_params, station):
        schedule_params["station"] = station

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    def test_valid_date(self, schedule_params, field_date):
        schedule_params["date"] = field_date
        params = ScheduleParams(**schedule_params)

        assert params.date == field_date

    @pytest.mark.parametrize(
        ("event", "expected"),
        [
            ("departure", ScheduleEvent.DEPARTURE),
            ("arrival", ScheduleEvent.ARRIVAL),
        ],
    )
    def test_valid_event(self, schedule_params, event, expected):
        schedule_params["event"] = event
        params = ScheduleParams(**schedule_params)

        assert params.event == expected

    def test_invalid_event(self, schedule_params):
        schedule_params["event"] = "invalid"

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    def test_valid_direction_for_suburban(self, schedule_params):
        schedule_params["transport_types"] = ["suburban"]
        schedule_params["direction"] = "forward"
        params = ScheduleParams(**schedule_params)

        assert params.direction == "forward"

    def test_direction_without_suburban(self, schedule_params):
        schedule_params["direction"] = "forward"

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    def test_direction_with_other_transport_type(self, schedule_params):
        schedule_params["transport_types"] = ["train"]
        schedule_params["direction"] = "forward"

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    def test_direction_without_transport_types(self, schedule_params):
        schedule_params["transport_types"] = None
        schedule_params["direction"] = None
        params = ScheduleParams(**schedule_params)

        assert params.direction is None

    def test_valid_transport_types(self, schedule_params):
        schedule_params["transport_types"] = [
            "plane",
            "train",
            "suburban",
        ]
        params = ScheduleParams(**schedule_params)

        assert params.transport_types == [
            TransportType.PLANE,
            TransportType.TRAIN,
            TransportType.SUBURBAN,
        ]

    def test_invalid_transport_type(self, schedule_params):
        schedule_params["transport_types"] = ["invalid"]

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    @pytest.mark.parametrize(
        ("field", "value", "expected"),
        [
            ("system", "yandex", CodingSystem.YANDEX),
            ("system", "iata", CodingSystem.IATA),
            ("show_systems", "all", ShowSystems.ALL),
            ("show_systems", "esr", ShowSystems.ESR),
        ],
    )
    def test_valid_coding_systems(self, schedule_params, field, value, expected):
        schedule_params[field] = value
        params = ScheduleParams(**schedule_params)

        assert getattr(params, field) == expected

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("system", "invalid"),
            ("show_systems", "invalid"),
        ],
    )
    def test_invalid_coding_systems(self, schedule_params, field, value):
        schedule_params[field] = value

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    @pytest.mark.parametrize("limit", [0, 101, -1])
    def test_invalid_limit(self, schedule_params, limit):
        schedule_params["limit"] = limit

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    @pytest.mark.parametrize("limit", [1, 20, 100])
    def test_valid_limit(self, schedule_params, limit):
        schedule_params["limit"] = limit
        params = ScheduleParams(**schedule_params)

        assert params.limit == limit

    @pytest.mark.parametrize("offset", [-1, -10])
    def test_invalid_offset(self, schedule_params, offset):
        schedule_params["offset"] = offset

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)

    def test_valid_offset(self, schedule_params):
        schedule_params["offset"] = 10

        params = ScheduleParams(**schedule_params)

        assert params.offset == 10

    def test_extra_field_is_forbidden(self, schedule_params):
        schedule_params["unknown"] = "value"

        with pytest.raises(ValidationError):
            ScheduleParams(**schedule_params)


class TestThreadParams:
    def test_valid_empty_params(self, thread_params):
        params = ThreadParams(**thread_params)

        assert params.date is None
        assert params.show_systems is None
        assert params.result_timezone is None

    def test_valid_date(self, thread_params, field_date):
        thread_params["date"] = field_date
        params = ThreadParams(**thread_params)

        assert params.date == field_date

    @pytest.mark.parametrize(
        ("show_systems", "expected"),
        [
            ("yandex", ShowSystems.YANDEX),
            ("esr", ShowSystems.ESR),
            ("all", ShowSystems.ALL),
        ],
    )
    def test_valid_show_systems(self, thread_params, show_systems, expected):
        thread_params["show_systems"] = show_systems
        params = ThreadParams(**thread_params)

        assert params.show_systems == expected

    def test_invalid_show_systems(self, thread_params):
        thread_params["show_systems"] = "invalid"

        with pytest.raises(ValidationError):
            ThreadParams(**thread_params)

    @pytest.mark.parametrize("timezone", ["", " ", "   "])
    def test_invalid_result_timezone(self, thread_params, timezone):
        thread_params["result_timezone"] = timezone

        with pytest.raises(ValidationError):
            ThreadParams(**thread_params)

    @pytest.mark.parametrize("timezone", ["Europe/Moscow", " Europe/Moscow "])
    def test_valid_result_timezone(self, thread_params, timezone):
        thread_params["result_timezone"] = timezone
        params = ThreadParams(**thread_params)

        assert params.result_timezone == "Europe/Moscow"

    def test_extra_field_is_forbidden(self, thread_params):
        thread_params["unknown"] = "value"

        with pytest.raises(ValidationError):
            ThreadParams(**thread_params)


class TestNearestStationsParams:
    def test_valid_params(self, nearest_params):
        params = NearestStationsParams(**nearest_params)

        assert params.lat == 55.7558
        assert params.lng == 37.6173
        assert params.distance == 50
        assert params.transport_types is None

    def test_valid_transport_types(self, nearest_params):
        nearest_params["transport_types"] = ["train", "suburban"]

        params = NearestStationsParams(**nearest_params)

        assert params.transport_types == [
            TransportType.TRAIN,
            TransportType.SUBURBAN,
        ]

    @pytest.mark.parametrize("lat", [-90, 90, 0, 55.7558])
    def test_valid_latitude(self, nearest_params, lat):
        nearest_params["lat"] = lat
        params = NearestStationsParams(**nearest_params)

        assert params.lat == lat

    @pytest.mark.parametrize("lat", [-90.1, 90.1, -91, 91])
    def test_invalid_latitude(self, nearest_params, lat):
        nearest_params["lat"] = lat

        with pytest.raises(ValidationError):
            NearestStationsParams(**nearest_params)

    @pytest.mark.parametrize("lng", [-180, 180, 0, 37.6173])
    def test_valid_longitude(self, nearest_params, lng):
        nearest_params["lng"] = lng
        params = NearestStationsParams(**nearest_params)

        assert params.lng == lng

    @pytest.mark.parametrize("lng", [-180.1, 180.1, -181, 181])
    def test_invalid_longitude(self, nearest_params, lng):
        nearest_params["lng"] = lng

        with pytest.raises(ValidationError):
            NearestStationsParams(**nearest_params)

    def test_invalid_distance(self, nearest_params):
        nearest_params["distance"] = 0

        with pytest.raises(ValidationError):
            NearestStationsParams(**nearest_params)

    def test_invalid_transport_type(self, nearest_params):
        nearest_params["transport_types"] = ["invalid"]

        with pytest.raises(ValidationError):
            NearestStationsParams(**nearest_params)

    def test_extra_field_is_forbidden(self, nearest_params):
        nearest_params["unknown"] = "value"

        with pytest.raises(ValidationError):
            NearestStationsParams(**nearest_params)


class TestNearestSettlementParams:
    def test_valid_params(self, nearest_params):
        params = NearestSettlementParams(**nearest_params)

        assert params.lat == 55.7558
        assert params.lng == 37.6173
        assert params.distance == 50

    @pytest.mark.parametrize("lat", [-90, 90])
    def test_valid_latitude_boundaries(self, nearest_params, lat):
        nearest_params["lat"] = lat
        params = NearestSettlementParams(**nearest_params)

        assert params.lat == lat

    @pytest.mark.parametrize("lat", [-90.1, 90.1])
    def test_invalid_latitude(self, nearest_params, lat):
        nearest_params["lat"] = lat

        with pytest.raises(ValidationError):
            NearestSettlementParams(**nearest_params)

    @pytest.mark.parametrize("lng", [-180, 180])
    def test_valid_longitude_boundaries(self, nearest_params, lng):
        nearest_params["lng"] = lng
        params = NearestSettlementParams(**nearest_params)

        assert params.lng == lng

    @pytest.mark.parametrize("lng", [-180.1, 180.1])
    def test_invalid_longitude(self, nearest_params, lng):
        nearest_params["lng"] = lng

        with pytest.raises(ValidationError):
            NearestSettlementParams(**nearest_params)

    @pytest.mark.parametrize("distance", [0, -1])
    def test_invalid_distance(self, nearest_params, distance):
        nearest_params["distance"] = distance

        with pytest.raises(ValidationError):
            NearestSettlementParams(**nearest_params)

    def test_missing_required_field(self):
        with pytest.raises(ValidationError):
            NearestSettlementParams(lat=55.7558, lng=37.6173)

    def test_extra_field_is_forbidden(self, nearest_params):
        nearest_params["unknown"] = "value"

        with pytest.raises(ValidationError):
            NearestSettlementParams(**nearest_params)


class TestCarrierParams:
    def test_valid_empty_params(self):
        params = CarrierParams()

        assert params.system is None

    @pytest.mark.parametrize(
        ("system", "expected"),
        [
            ("yandex", CodingSystem.YANDEX),
            ("iata", CodingSystem.IATA),
            ("sirena", CodingSystem.SIRENA),
            ("express", CodingSystem.EXPRESS),
            ("esr", CodingSystem.ESR),
        ],
    )
    def test_valid_system(self, system, expected):
        params = CarrierParams(system=system)

        assert params.system == expected

    def test_invalid_system(self):
        with pytest.raises(ValidationError):
            CarrierParams(system="invalid")

    def test_extra_field_is_forbidden(self):
        with pytest.raises(ValidationError):
            CarrierParams(unknown="value")


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

    def test_valid_transport_types(self):
        params = StationsParams(transport_types=["train", "bus"])

        assert params.transport_types == [
            TransportType.TRAIN,
            TransportType.BUS,
        ]

    def test_invalid_transport_type(self):
        with pytest.raises(ValidationError):
            StationsParams(transport_types=["invalid"])

    @pytest.mark.parametrize(
        ("system", "expected"),
        [
            ("yandex", CodingSystem.YANDEX),
            ("iata", CodingSystem.IATA),
            ("sirena", CodingSystem.SIRENA),
            ("express", CodingSystem.EXPRESS),
            ("esr", CodingSystem.ESR),
        ],
    )
    def test_valid_system(self, system, expected):
        params = StationsParams(system=system)

        assert params.system == expected

    def test_invalid_system(self):
        with pytest.raises(ValidationError):
            StationsParams(system="invalid")

    @pytest.mark.parametrize(
        ("show_systems", "expected"),
        [
            ("yandex", ShowSystems.YANDEX),
            ("esr", ShowSystems.ESR),
            ("all", ShowSystems.ALL),
        ],
    )
    def test_valid_show_systems(self, show_systems, expected):
        params = StationsParams(show_systems=show_systems)

        assert params.show_systems == expected

    def test_invalid_show_systems(self):
        with pytest.raises(ValidationError):
            StationsParams(show_systems="invalid")

    @pytest.mark.parametrize("lang", ["", " ", "a"])
    def test_invalid_lang(self, lang):
        with pytest.raises(ValidationError):
            StationsParams(lang=lang)

    @pytest.mark.parametrize("lang", ["ru", "en", "ru-RU"])
    def test_valid_lang(self, lang):
        params = StationsParams(lang=lang)

        assert params.lang == lang

    def test_lang_whitespace_is_stripped(self):
        params = StationsParams(lang=" ru ")

        assert params.lang == "ru"

    def test_extra_field_is_forbidden(self):
        with pytest.raises(ValidationError):
            StationsParams(unknown="value")
