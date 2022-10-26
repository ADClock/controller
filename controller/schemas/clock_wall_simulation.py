from pydantic import BaseModel, Field


class HandSimulation(BaseModel):
    """
    Attributes to return via API for a simulated clock hand.
    """
    current_position: int = Field(..., description="The current position of the hand.")
    planned_steps: int = Field(..., description="The number of steps that are planned to be executed.")

    class Config:
        orm_mode = True


class ClockSimulation(BaseModel):
    """
    Attributes to return via API for a simulated clock.
    """
    x: int = Field(..., description="x position of the clock.")
    y: int = Field(..., description="y position of the clock.")
    hour: HandSimulation = Field(..., description="The simulated hour hand.")
    minute: HandSimulation = Field(..., description="The simulated minute hand.")

    class Config:
        orm_mode = True
