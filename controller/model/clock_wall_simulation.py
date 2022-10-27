from typing import List

from controller.model import MAX_STEPS
from controller.model.instruction_receiver import InstructionReceiver, HandInstruction, ClockWallInstruction


class HandSimulation:
    """
    Simulates a hand of a single clock.
    """
    current_position: int
    planned_steps: int

    def __init__(self):
        self.reset()

    def try_step(self):
        """
        This method needs to be called every four milliseconds.

        If the hand has pending steps it simulates one step.
        """
        if self.planned_steps > 0:
            self.planned_steps -= 1
            if self.current_position == MAX_STEPS - 1:
                self.current_position = 0
            else:
                self.current_position += 1
        elif self.planned_steps < 0:
            self.planned_steps += 1
            if self.current_position == 0:
                self.current_position = MAX_STEPS - 1
            else:
                self.current_position -= 1

    def reset(self):
        self.current_position = 0
        self.planned_steps = 0

    def target_position(self):
        return (self.current_position + self.planned_steps + MAX_STEPS) % MAX_STEPS


class ClockSimulation:
    """
    Simulation of one single clock.
    """
    minute: HandSimulation
    hour: HandSimulation
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.minute = HandSimulation()
        self.hour = HandSimulation()

    def update_plan(self, hour: HandInstruction, minute: HandInstruction):
        """
        This method is called when the clock is updated with new instructions.
        """
        if hour == HandInstruction.RESET or minute == HandInstruction.RESET:
            self.minute.reset()
            self.hour.reset()
        else:
            # Update hour hand
            if hour == HandInstruction.CLOCKWISE:
                self.hour.planned_steps += 1
            elif hour == HandInstruction.COUNTER_CLOCKWISE:
                self.hour.planned_steps -= 1

            # Update minute hand
            if minute == HandInstruction.CLOCKWISE:
                self.minute.planned_steps += 1
            elif minute == HandInstruction.COUNTER_CLOCKWISE:
                self.minute.planned_steps -= 1


class ClockWallSimulation(InstructionReceiver):
    """
    Simulation of the clock wall.

    The simulation receives the instructions that are send to the real clocks and simulates the movement.
    """
    clocks: List[ClockSimulation] = []

    def __init__(self, size_x: int, size_y: int):
        self.clocks = [ClockSimulation(x, y) for x in range(size_x) for y in range(size_y)]

    def tick(self):
        for clock in self.clocks:
            clock.minute.try_step()
            clock.hour.try_step()

    async def tick_async(self):
        self.tick()

    def execute(self, data: ClockWallInstruction):
        """
        This method is called when new instructions are available.
        """
        for i, clock in enumerate(self.clocks):
            clock.update_plan(data.clock_instructions[i].hour, data.clock_instructions[i].minute)
