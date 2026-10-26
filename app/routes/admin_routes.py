import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/admin/transport", tags=["Admin Transport"])
