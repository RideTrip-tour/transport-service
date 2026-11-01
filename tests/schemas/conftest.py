from datetime import date

import pytest


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
    return {"station": "s9600213"}


@pytest.fixture
def nearest_params():
    return {
        "lat": 55.7558,
        "lng": 37.6173,
        "distance": 50,
    }
