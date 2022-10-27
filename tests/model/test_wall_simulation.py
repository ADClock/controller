from controller.model.clock_wall_simulation import ClockWallSimulation
from controller.model.instruction_receiver import ClockWallInstruction, ClockInstruction, HandInstruction


def test_wall_simulation_one_clock():
    sim = ClockWallSimulation(1, 1)
    assert len(sim.clocks) == 1


def test_wall_simulation_24_clocks():
    sim = ClockWallSimulation(8, 3)
    assert len(sim.clocks) == 24


def test_wall_simulation_planned_step():
    sim = ClockWallSimulation(1, 1)
    assert sim.clocks[0].hour.planned_steps == 0
    sim.execute(ClockWallInstruction([ClockInstruction(HandInstruction.CLOCKWISE, HandInstruction.IDLE)]))
    assert sim.clocks[0].hour.planned_steps == 1


def test_wall_simulation_tick():
    sim = ClockWallSimulation(1, 1)
    assert sim.clocks[0].minute.planned_steps == 0
    sim.execute(ClockWallInstruction([ClockInstruction(HandInstruction.IDLE, HandInstruction.CLOCKWISE)]))
    assert sim.clocks[0].minute.planned_steps == 1
    sim.tick()
    assert sim.clocks[0].minute.planned_steps == 0
    assert sim.clocks[0].minute.current_position == 1
