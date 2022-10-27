from enum import Enum


class HandInstruction(Enum):
    IDLE = 0
    RESET = 1
    CLOCKWISE = 2
    COUNTER_CLOCKWISE = 3


class ClockInstruction:

    hour: HandInstruction
    minute: HandInstruction

    __slots__ = ['hour', 'minute']

    def __init__(self, hour: HandInstruction, minute: HandInstruction):
        self.hour = hour
        self.minute = minute

    def __str__(self):
        return f'ClockInstruction({self.hour}, {self.minute})'


class ClockWallInstruction:
    """
    Holds the instructions for the next step.
    """
    clock_instructions: [ClockInstruction]

    __slots__ = ['clock_instructions']

    def __init__(self, clock_instructions: [ClockInstruction]):
        self.clock_instructions = clock_instructions

    def __str__(self):
        return str([str(clock) for clock in self.clock_instructions])


class InstructionReceiver:
    """
    This class is used to receive instructions and process them.
    """

    def execute(self, data: ClockWallInstruction):
        """
        This method is called when new instructions are available.
        """
        pass
