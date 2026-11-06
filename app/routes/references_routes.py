import logging

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/references", tags=["References"])


def raise_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Путь не найден.",
    )


@router.get("/references/transport-types")
async def get_transport_types():
    raise_not_found()


@router.get("/references/station-types")
async def get_station_types():
    raise_not_found()


@router.get("/references/systems")
async def get_coding_systems():
    raise_not_found()
