from typing import Annotated

from fastapi import Depends
from shared.database.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession


async def managed_db_session():
    async with get_db_session() as db_session:
        yield db_session


DBSessionDep = Annotated[AsyncSession, Depends(managed_db_session)]
