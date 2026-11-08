import pytest
from pydantic import ValidationError

from app.schemas.transport import (
    ScheduleEvent,
    ScheduleParams,
)


class TestScheduleParams:
    def test_valid_with_required_fields(self, schedule_params):
        params = ScheduleParams(**schedule_params)

        assert params.station == "s9600213"
        assert params.date is None
        assert params.event == ScheduleEvent.DEPARTURE

    def test_station_is_required(self):
        with pytest.raises(ValidationError):
            ScheduleParams()

    @pytest.mark.parametrize("station", ["", " "])
    def test_invalid_station(self, schedule_params, station):
        with pytest.raises(ValidationError):
            ScheduleParams(**{**schedule_params, "station": station})

    @pytest.mark.parametrize(
        ("event", "expected"),
        [
            ("departure", ScheduleEvent.DEPARTURE),
            ("arrival", ScheduleEvent.ARRIVAL),
        ],
    )
    def test_valid_event(self, schedule_params, event, expected):
        params = ScheduleParams(**{**schedule_params, "event": event})

        assert params.event == expected

    def test_invalid_event(self, schedule_params):
        with pytest.raises(ValidationError):
            ScheduleParams(**{**schedule_params, "event": "invalid"})

    def test_valid_direction_for_suburban(self, schedule_params):
        params = ScheduleParams(
            **{
                **schedule_params,
                "transport_types": ["suburban"],
                "direction": "forward",
            }
        )

        assert params.direction == "forward"

    @pytest.mark.parametrize(
        "transport_types",
        [None, ["train"], ["bus"], ["plane"]],
    )
    def test_direction_requires_suburban(
        self,
        schedule_params,
        transport_types,
    ):
        with pytest.raises(ValidationError):
            ScheduleParams(
                **{
                    **schedule_params,
                    "transport_types": transport_types,
                    "direction": "forward",
                }
            )

    def test_direction_without_transport_types(self, schedule_params):
        params = ScheduleParams(**schedule_params)

        assert params.direction is None
