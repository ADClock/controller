import sys

from controller.model.instruction_receiver import ClockInstruction, HandInstruction, ClockWallInstruction


def test_clock_wall_instruction_size():
    """
    Create list with 2000 instructions for 24 clocks.
    Check if object size is not too big.
    """
    wall_instructions = []
    for _ in range(2000):
        wall_instructions.append(ClockWallInstruction([ClockInstruction(HandInstruction.CLOCKWISE, HandInstruction.IDLE)
                                                       for _ in range(24)]))
    assert len(wall_instructions) == 2000
    assert len(wall_instructions[0].clock_instructions) == 24
    assert sys.getsizeof(wall_instructions) == 16184  # bytes
