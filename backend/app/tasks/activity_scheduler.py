import asyncio
import logging
from contextlib import asynccontextmanager

from app.core.database import SessionLocal
from app.services.activity_service import activity_service

logger = logging.getLogger("sports-partner")


async def _status_refresh_loop() -> None:
    while True:
        await asyncio.sleep(60)
        db = SessionLocal()
        try:
            activity_service.refresh_all_statuses(db)
        except Exception as exc:
            logger.warning("Activity status refresh failed: %s", exc)
        finally:
            db.close()


@asynccontextmanager
async def activity_scheduler_lifespan():
    task = asyncio.create_task(_status_refresh_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
