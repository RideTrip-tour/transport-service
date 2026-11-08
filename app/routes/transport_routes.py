import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, status

from app.schemas.constants import MIN_LEN_UID
from app.schemas.transport import (
    CarrierParams,
    NearestSettlementParams,
    NearestStationsParams,
    ScheduleParams,
    StationsParams,
    ThreadParams,
    TransportSearchParams,
)

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/transport", tags=["Transport"])


def raise_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Путь не найден.",
    )


@router.get("/search")
async def search_transport(params: Annotated[TransportSearchParams, Query()]):
    raise_not_found()


@router.get("/schedule")
async def get_schedule(params: Annotated[ScheduleParams, Query()]):
    raise_not_found()


@router.get("/thread/{uid}")
async def get_thread(
    uid: Annotated[str, Path(min_length=MIN_LEN_UID)],
    params: Annotated[ThreadParams, Query()],
):
    raise_not_found()


@router.get("/nearest-stations")
async def get_nearest_stations(
    params: Annotated[NearestStationsParams, Query()],
):
    raise_not_found()


@router.get("/nearest-settlement")
async def get_nearest_settlement(
    params: Annotated[NearestSettlementParams, Query()],
):
    raise_not_found()


@router.get("/carrier/{code}")
async def get_carrier(
    code: Annotated[str, Path(min_length=1)],
    params: Annotated[CarrierParams, Query()],
):
    raise_not_found()


@router.get("/stations")
async def get_stations(
    params: Annotated[StationsParams, Query()],
):
    raise_not_found()


@router.get("/filters")
async def get_transport_filters():
    raise_not_found()


@router.get("/copyright")
async def get_copyright():
    raise_not_found()
