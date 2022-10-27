from typing import List

from fastapi import Depends, APIRouter, HTTPException

import controller.schemas as schemas
from controller.api import deps
from controller.model.clock_wall import ClockWall

router = APIRouter()


@router.get("/", response_model=List[schemas.ClockSimulation])
def get_simulation_wall(wall: ClockWall = Depends(deps.get_clock_wall)) -> List[schemas.ClockSimulation]:
    """
    Returns the clock positions of the simulated wall.

    This should match the real wall.
    """
    return wall.simulation.clocks


@router.get("/id/{clock_id}", response_model=schemas.ClockSimulation,
            responses={404: {"description": "Clock not found"}})
def get_simulated_clock_by_id(wall: ClockWall = Depends(deps.get_clock_wall),
                              clock_id: int = 0) -> schemas.ClockSimulation:
    """
    Returns the simulated clock for the given id.

    This should match the real wall.
    """
    if not 0 <= clock_id < len(wall.simulation.clocks):
        raise HTTPException(status_code=404,
                            detail=f"Clock id not found. Choose a value in [0, {len(wall.simulation.clocks)})")

    return wall.simulation.clocks[clock_id]


@router.get("/position/{x}/{y}", response_model=schemas.ClockSimulation,
            responses={404: {"description": "Clock not found"}})
def get_simulated_clock_by_position(wall: ClockWall = Depends(deps.get_clock_wall),
                                    x: int = 0, y: int = 0) -> schemas.ClockSimulation:
    """
    Returns the simulated clock for the given position.

    This should match the real wall.
    """
    if not 0 <= x < wall.size_x:
        raise HTTPException(status_code=404,
                            detail=f"x is out of range. Choose a value in [0, {str(wall.size_x)})")
    if not 0 <= y < wall.size_x:
        raise HTTPException(status_code=404,
                            detail=f"y is out of range. Choose a value in [0, {str(wall.size_x)})")

    return wall.simulation.clocks[wall.get_clock_id(x, y)]
