import pytest
from pydantic import ValidationError

from app.schemas.transport import (
    CarrierParams,
    CodingSystem,
    NearestSettlementParams,
    NearestStationsParams,
    ScheduleParams,
    ShowSystems,
    StationsParams,
    ThreadParams,
    TransportSearchParams,
    TransportType,
)

# Все схемы
ALL_SCHEMAS = [
    (
        TransportSearchParams,
        {
            "from_location_id": 1,
            "to_location_id": 2,
            "date": "2026-11-15",
        },
    ),
    (ScheduleParams, {"station": "s9600213"}),
    (ThreadParams, {}),
    (
        NearestStationsParams,
        {"lat": 55.7558, "lng": 37.6173, "distance": 50},
    ),
    (
        NearestSettlementParams,
        {"lat": 55.7558, "lng": 37.6173, "distance": 50},
    ),
    (CarrierParams, {}),
    (StationsParams, {}),
]

# Схемы с пагинацией
PAGINATION_SCHEMAS = [
    (
        TransportSearchParams,
        {"from_location_id": 1, "to_location_id": 2, "date": "2026-11-15"},
    ),
    (ScheduleParams, {"station": "s9600213"}),
]

# Схемы с часовым поясом
TIMEZONE_SCHEMAS = [
    (
        TransportSearchParams,
        {"from_location_id": 1, "to_location_id": 2, "date": "2026-11-15"},
    ),
    (ScheduleParams, {"station": "s9600213"}),
    (ThreadParams, {}),
]

# Схемы с системой кодирования
CODING_SCHEMAS = [
    (
        TransportSearchParams,
        {"from_location_id": 1, "to_location_id": 2, "date": "2026-11-15"},
    ),
    (ScheduleParams, {"station": "s9600213"}),
    (CarrierParams, {}),
    (StationsParams, {}),
]

# Схемы с параметром отображения систем
SYSTEMS_SCHEMAS = [
    (
        TransportSearchParams,
        {"from_location_id": 1, "to_location_id": 2, "date": "2026-11-15"},
    ),
    (ScheduleParams, {"station": "s9600213"}),
    (StationsParams, {}),
]

# Схемы с типами транспорта
TRANSPORT_TYPE_SCHEMAS = [
    (
        TransportSearchParams,
        {"from_location_id": 1, "to_location_id": 2, "date": "2026-11-15"},
    ),
    (ScheduleParams, {"station": "s9600213"}),
    (NearestStationsParams, {"lat": 55.7558, "lng": 37.6173, "distance": 50}),
    (StationsParams, {}),
]


class TestPaginationParams:
    @pytest.mark.parametrize(("schema", "payload"), PAGINATION_SCHEMAS)
    def test_default_pagination(self, schema, payload):
        params = schema(**payload)

        assert params.limit == 20
        assert params.offset == 0

    @pytest.mark.parametrize(("schema", "payload"), PAGINATION_SCHEMAS)
    @pytest.mark.parametrize("limit", [1, 20, 100])
    def test_valid_limit(self, schema, payload, limit):
        params = schema(**{**payload, "limit": limit})

        assert params.limit == limit

    @pytest.mark.parametrize(("schema", "payload"), PAGINATION_SCHEMAS)
    @pytest.mark.parametrize("limit", [0, 101, -1])
    def test_invalid_limit(self, schema, payload, limit):
        with pytest.raises(ValidationError):
            schema(**{**payload, "limit": limit})

    @pytest.mark.parametrize(("schema", "payload"), PAGINATION_SCHEMAS)
    @pytest.mark.parametrize("offset", [0, 10, 100])
    def test_valid_offset(self, schema, payload, offset):
        params = schema(**{**payload, "offset": offset})

        assert params.offset == offset

    @pytest.mark.parametrize(("schema", "payload"), PAGINATION_SCHEMAS)
    @pytest.mark.parametrize("offset", [-1, -10])
    def test_invalid_offset(self, schema, payload, offset):
        with pytest.raises(ValidationError):
            schema(**{**payload, "offset": offset})


class TestTimezoneParams:
    @pytest.mark.parametrize(("schema", "payload"), TIMEZONE_SCHEMAS)
    @pytest.mark.parametrize(
        "timezone",
        ["Europe/Moscow", "Europe/Zurich", " UTC "],
    )
    def test_valid_timezone(self, schema, payload, timezone):
        params = schema(**{**payload, "result_timezone": timezone})

        assert params.result_timezone == timezone.strip()

    @pytest.mark.parametrize(("schema", "payload"), TIMEZONE_SCHEMAS)
    @pytest.mark.parametrize("timezone", ["", " ", "   "])
    def test_invalid_timezone(self, schema, payload, timezone):
        with pytest.raises(ValidationError):
            schema(**{**payload, "result_timezone": timezone})


class TestCodingSystemParams:
    @pytest.mark.parametrize(("schema", "payload"), CODING_SCHEMAS)
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
    def test_valid_system(self, schema, payload, system, expected):
        params = schema(**{**payload, "system": system})

        assert params.system == expected

    @pytest.mark.parametrize(("schema", "payload"), CODING_SCHEMAS)
    def test_invalid_system(self, schema, payload):
        with pytest.raises(ValidationError):
            schema(**{**payload, "system": "invalid"})


class TestShowSystemsParams:
    @pytest.mark.parametrize(("schema", "payload"), SYSTEMS_SCHEMAS)
    @pytest.mark.parametrize(
        ("show_systems", "expected"),
        [
            ("yandex", ShowSystems.YANDEX),
            ("esr", ShowSystems.ESR),
            ("all", ShowSystems.ALL),
        ],
    )
    def test_valid_show_systems(self, schema, payload, show_systems, expected):
        params = schema(**{**payload, "show_systems": show_systems})

        assert params.show_systems == expected

    @pytest.mark.parametrize(("schema", "payload"), SYSTEMS_SCHEMAS)
    def test_invalid_show_systems(self, schema, payload):
        with pytest.raises(ValidationError):
            schema(**{**payload, "show_systems": "invalid"})


class TestTransportTypesParams:
    @pytest.mark.parametrize(("schema", "payload"), TRANSPORT_TYPE_SCHEMAS)
    def test_valid_transport_types(self, schema, payload):
        transport_types = ["plane", "train", "suburban", "bus"]

        params = schema(**{**payload, "transport_types": transport_types})

        assert params.transport_types == [
            TransportType.PLANE,
            TransportType.TRAIN,
            TransportType.SUBURBAN,
            TransportType.BUS,
        ]

    @pytest.mark.parametrize(("schema", "payload"), TRANSPORT_TYPE_SCHEMAS)
    def test_invalid_transport_type(self, schema, payload):
        with pytest.raises(ValidationError):
            schema(**{**payload, "transport_types": ["invalid"]})


class TestExtraFields:
    @pytest.mark.parametrize(("schema", "payload"), ALL_SCHEMAS)
    def test_extra_field_is_forbidden(self, schema, payload):
        with pytest.raises(ValidationError):
            schema(**{**payload, "unknown": "value"})
