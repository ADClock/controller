from controller.model.clock_wall_simulation import ClockSimulation
from controller.model.instruction_receiver import HandInstruction


def get_clock_simulation():
    sim = ClockSimulation()
    sim.minute.current_position = 42
    sim.hour.current_position = 42
    return sim


def test_update_plan_nothing():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.IDLE, HandInstruction.IDLE)
    assert sim.hour.target_position() == 42
    assert sim.minute.target_position() == 42


def test_update_plan_reset_hour():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.RESET, HandInstruction.IDLE)
    assert sim.hour.target_position() == 0
    assert sim.minute.target_position() == 0


def test_update_plan_reset_minute():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.IDLE, HandInstruction.RESET)
    assert sim.hour.target_position() == 0
    assert sim.minute.target_position() == 0


def test_update_plan_reset_both():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.RESET, HandInstruction.RESET)
    assert sim.hour.target_position() == 0
    assert sim.minute.target_position() == 0


def test_update_plan_hour_backwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.COUNTER_CLOCKWISE, HandInstruction.IDLE)
    assert sim.hour.target_position() == 41
    assert sim.minute.target_position() == 42


def test_update_plan_hour_forwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.CLOCKWISE, HandInstruction.IDLE)
    assert sim.hour.target_position() == 43
    assert sim.minute.target_position() == 42


def test_update_plan_minute_backwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.IDLE, HandInstruction.COUNTER_CLOCKWISE)
    assert sim.hour.target_position() == 42
    assert sim.minute.target_position() == 41


def test_update_plan_minute_forwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.IDLE, HandInstruction.CLOCKWISE)
    assert sim.hour.target_position() == 42
    assert sim.minute.target_position() == 43


def test_update_plan_hour_and_minute_backwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.COUNTER_CLOCKWISE, HandInstruction.COUNTER_CLOCKWISE)
    assert sim.hour.target_position() == 41
    assert sim.minute.target_position() == 41


def test_update_plan_hour_and_minute_forwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.CLOCKWISE, HandInstruction.CLOCKWISE)
    assert sim.hour.target_position() == 43
    assert sim.minute.target_position() == 43


def test_update_plan_hour_backwards_and_minute_forwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.COUNTER_CLOCKWISE, HandInstruction.CLOCKWISE)
    assert sim.hour.target_position() == 41
    assert sim.minute.target_position() == 43


def test_update_plan_hour_forwards_and_minute_backwards():
    sim = get_clock_simulation()
    sim.update_plan(HandInstruction.CLOCKWISE, HandInstruction.COUNTER_CLOCKWISE)
    assert sim.hour.target_position() == 43
    assert sim.minute.target_position() == 41
