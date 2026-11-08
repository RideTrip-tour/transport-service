from unittest.mock import patch

import pytest

from app.db import database


@pytest.mark.asyncio
async def test_get_async_session(session):
    with patch.object(database, "AsyncSessionLocal", return_value=session):
        async for result in database.get_async_session():
            assert result is session

    session.rollback.assert_not_awaited()
    session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_async_session_rollback(session):
    with patch.object(database, "AsyncSessionLocal", return_value=session):
        generator = database.get_async_session()

        assert await generator.__anext__() is session

        with pytest.raises(ValueError, match="Database error"):
            await generator.athrow(ValueError("Database error"))

    session.rollback.assert_awaited_once()
    session.close.assert_awaited_once()
