from fastapi import APIRouter

from .endpoints import users, authentication, clock_wall_simulation

api_router = APIRouter()
api_router.include_router(authentication.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(clock_wall_simulation.router, prefix="/simulation", tags=["Clock Wall Simulation"])
