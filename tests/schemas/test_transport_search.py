import pytest
from pydantic import ValidationError

from app.schemas.transport import TransportSearchParams


class TestTransportSearchParams:
    def test_valid_with_location_ids(self, location_params):
        params = TransportSearchParams(**location_params)

        assert params.from_location_id == 1
        assert params.to_location_id == 2
        assert params.date == location_params["date"]

    def test_valid_with_codes(self, code_params):
        params = TransportSearchParams(**code_params)

        assert params.from_code == "c213"
        assert params.to_code == "c2"

    @pytest.mark.parametrize(
        "location_id",
        ["from_location_id", "to_location_id"],
    )
    def test_location_ids_must_be_provided_together(
        self,
        location_params,
        location_id,
    ):
        location_params[location_id] = None

        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)

    @pytest.mark.parametrize("code", ["from_code", "to_code"])
    def test_codes_must_be_provided_together(self, code_params, code):
        code_params[code] = None

        with pytest.raises(ValidationError):
            TransportSearchParams(**code_params)

    def test_location_ids_and_codes_are_mutually_exclusive(
        self,
        location_params,
        code_params,
    ):
        with pytest.raises(ValidationError):
            TransportSearchParams(**{**location_params, **code_params})

    def test_route_source_is_required(self, field_date):
        with pytest.raises(ValidationError):
            TransportSearchParams(date=field_date)

    def test_date_is_required(self, location_params):
        location_params.pop("date")

        with pytest.raises(ValidationError):
            TransportSearchParams(**location_params)
