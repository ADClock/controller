import asyncio

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from controller.adclock import adclock
from controller.api import api_router
from controller.core import settings
from controller.database import init_db

# Create FastAPI app and add all endpoints
app = FastAPI(title=settings.SERVER_NAME)
app.include_router(api_router)


# Initialize database and create models
@app.on_event("startup")
def init_database():
    init_db.check_connection()
    init_db.create_all()


# Start simulation
@app.on_event("startup")
async def run_simulation():
    asyncio.create_task(adclock.run_simulation())


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )
