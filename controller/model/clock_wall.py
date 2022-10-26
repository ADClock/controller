import time
from typing import List

from controller.model.clock_wall_planning import ClockWallPlanning
from controller.model.clock_wall_simulation import ClockWallSimulation
from controller.model.instruction_receiver import InstructionReceiver


class ClockWall:
    """
    Wall of clocks.

    This is the main class for controlling the ADClock.
    It contains the simulation and the planning.
    """
    size_x: int = 0
    size_y: int = 0

    simulation: ClockWallSimulation
    planning: ClockWallPlanning

    instruction_receiver: List[InstructionReceiver]

    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.simulation = ClockWallSimulation(size_x, size_y)
        self.planning = ClockWallPlanning(self.simulation)
        self.instruction_receiver = []
        self.instruction_receiver.append(self.simulation)

    def execute_plan(self):
        """
        This method is called, when the plan should be executed.

        The simulation and the plan is taken from the instance and the instructions are created.
        """
        clock_instructions = self.planning.get_instructions()

        for instruction in clock_instructions:
            for receiver in self.instruction_receiver:
                receiver.execute(instruction)
            # wait 4 ms
            time.sleep(0.004)
            self.simulation.tick()  # TODO remove this

    def get_clock_id(self, x: int, y: int) -> int:
        """
        Get the clock id for the given position.
        """
        return x * self.size_y + y

    def get_clock_position(self, clock_id: int) -> (int, int):
        """
        Get the position for the given clock id.
        """
        return clock_id // self.size_y, clock_id % self.size_y
