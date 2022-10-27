from enum import Enum
from typing import List

from controller.model import MAX_STEPS
from controller.model.clock_wall_simulation import ClockWallSimulation, ClockSimulation, HandSimulation
from controller.model.instruction_receiver import HandInstruction, ClockInstruction, ClockWallInstruction


class Direction(Enum):
    AUTO = 1
    SHORTEST = 2
    CLOCKWISE = 3
    COUNTER_CLOCKWISE = 4


class Speed(Enum):
    AUTO = 1
    FAST = 2
    SLOW = 3


class HandPlan:
    """
    The plan for one single hand.
    """
    simulation: HandSimulation
    target_position: int
    direction: Direction
    speed: Speed

    def __init__(self, simulation: HandSimulation):
        self.simulation = simulation
        self.target_position = 0
        self.direction = Direction.AUTO
        self.speed = Speed.AUTO

    def set_speed(self, speed: Speed):
        self.speed = speed

    def set_direction(self, direction: Direction):
        self.direction = direction

    def set_target_position(self, target_position: int):
        self.target_position = target_position

    def set_target_position_relative(self, target_position_relative: int):
        self.target_position = (self.target_position + target_position_relative + MAX_STEPS) % MAX_STEPS

    def set_target_position_degree(self, target_position_degree: int):
        self.target_position = int(target_position_degree / 360 * MAX_STEPS)

    def get_required_steps(self, clockwise: bool):
        if clockwise:
            return (self.target_position - self.simulation.target_position() + MAX_STEPS) % MAX_STEPS
        else:
            return (self.simulation.target_position() - self.target_position + MAX_STEPS) % MAX_STEPS

    def get_instructions(self) -> List[HandInstruction]:
        """
        Returns the instructions for the hand.

        In the future there are more options possible. For example:
        - Wait steps before running
        - acceleration
        - deceleration
        """
        instructions = []

        # Calculate the required steps for the direction
        # TODO Automatic means to apply direction from above. But that is not implemented yet.
        clockwise = False
        if self.direction == Direction.CLOCKWISE:
            clockwise = True
        elif self.direction in (Direction.SHORTEST, Direction.AUTO) \
                and self.get_required_steps(True) < self.get_required_steps(False):
            clockwise = True

        steps_count = self.get_required_steps(clockwise)

        # Calculate the speed
        idle_between_steps = 0
        if self.speed == Speed.AUTO:
            pass
        elif self.speed == Speed.FAST:
            idle_between_steps = 0
        elif self.speed == Speed.SLOW:
            idle_between_steps = 1

        # Generate the instructions
        step_instruction = [HandInstruction.CLOCKWISE if clockwise else HandInstruction.COUNTER_CLOCKWISE] + \
                           [HandInstruction.IDLE] * idle_between_steps

        instructions.extend(step_instruction * steps_count)

        return instructions


class ClockPlan:
    hour: HandPlan
    minute: HandPlan

    force_reset: bool

    def __init__(self, simulated_clock: ClockSimulation):
        self.hour = HandPlan(simulated_clock.hour)
        self.minute = HandPlan(simulated_clock.minute)
        self.force_reset = False

    def force_reset(self):
        """
        Force the clock to reset to 0:00.
        After that the clock will continue with the planned movement.
        """
        self.force_reset = True

    def set_time(self, hour: int, minute: int):
        """
        Set the time of the clock.
        """
        self.hour.set_target_position_degree(int(hour * 30 + minute / 2))
        self.minute.set_target_position_degree(minute * 6)

    def get_instructions(self) -> List[ClockInstruction]:
        """
        Get the instructions for the clock.
        """
        hour_instructions = self.hour.get_instructions()
        minute_instructions = self.minute.get_instructions()

        instructions = []
        if self.force_reset:
            instructions.append(ClockInstruction(HandInstruction.RESET, HandInstruction.RESET))
            self.force_reset = False

        for i in range(max(len(hour_instructions), len(minute_instructions))):
            instructions.append(ClockInstruction(
                hour=hour_instructions[i] if i < len(hour_instructions) else HandInstruction.IDLE,
                minute=minute_instructions[i] if i < len(minute_instructions) else HandInstruction.IDLE
            ))

        return instructions


class ClockWallPlanning:
    """
    This class holds the plan for the clock wall.

    """

    clocks: List[ClockPlan] = []
    simulation: ClockWallSimulation

    def __init__(self, simulation: ClockWallSimulation):
        self.simulation = simulation
        self.clocks = [ClockPlan(simulated_clock) for simulated_clock in simulation.clocks]

    def get_instructions(self) -> List[ClockWallInstruction]:
        """
        Get the instructions for the clock wall.

        For all clocks the instructions are generated and then merged into one list with one entry for every step.
        """
        clock_instruction_sets = [clock.get_instructions() for clock in self.clocks]

        max_instructions = max(len(x) for x in clock_instruction_sets)
        idle_instruction = ClockInstruction(HandInstruction.IDLE, HandInstruction.IDLE)
        return [
            ClockWallInstruction([x[i] if len(x) > i else idle_instruction
                                  for x in clock_instruction_sets])
            for i in range(max_instructions)
        ]
