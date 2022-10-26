from controller.model.clock_wall_simulation import HandSimulation, MAX_STEPS


def test_target_position_without_pending_steps():
    sim = HandSimulation()
    sim.current_position = 42
    sim.planned_steps = 0
    assert sim.target_position() == 42


def test_target_position_with_pending_steps():
    sim = HandSimulation()
    sim.current_position = 42
    sim.planned_steps = 5
    assert sim.target_position() == 47


def test_target_position_with_pending_steps_negative():
    sim = HandSimulation()
    sim.current_position = 42
    sim.planned_steps = -5
    assert sim.target_position() == 37


def test_target_position_with_pending_steps_overflow():
    sim = HandSimulation()
    sim.current_position = 1700
    sim.planned_steps = 10
    assert sim.target_position() == 5


def test_target_position_with_pending_steps_underflow():
    sim = HandSimulation()
    sim.current_position = 5
    sim.planned_steps = -10
    assert sim.target_position() == 1700


def test_target_position_full_rotation_forwards():
    sim = HandSimulation()
    sim.current_position = 60
    sim.planned_steps = MAX_STEPS
    assert sim.target_position() == 60


def test_target_position_full_rotation_backwards():
    sim = HandSimulation()
    sim.current_position = 60
    sim.planned_steps = - MAX_STEPS
    assert sim.target_position() == 60


def test_try_step_without_pending_steps():
    sim = HandSimulation()
    sim.current_position = 42
    sim.planned_steps = 0
    sim.try_step()
    assert sim.current_position == 42


def test_try_step_with_pending_steps():
    sim = HandSimulation()
    sim.current_position = 42
    sim.planned_steps = 5
    sim.try_step()
    assert sim.current_position == 43
    assert sim.planned_steps == 4


def test_try_step_with_pending_steps_negative():
    sim = HandSimulation()
    sim.current_position = 42
    sim.planned_steps = -5
    sim.try_step()
    assert sim.current_position == 41
    assert sim.planned_steps == -4


def test_try_step_with_pending_steps_overflow():
    sim = HandSimulation()
    sim.current_position = 1704
    sim.planned_steps = 10
    sim.try_step()
    sim.try_step()
    assert sim.current_position == 1
    assert sim.planned_steps == 8


def test_try_step_with_pending_steps_underflow():
    sim = HandSimulation()
    sim.current_position = 1
    sim.planned_steps = -10
    sim.try_step()
    sim.try_step()
    assert sim.current_position == 1704
    assert sim.planned_steps == -8


def test_reset():
    sim = HandSimulation()
    sim.current_position = 42
    sim.planned_steps = 5
    sim.reset()
    assert sim.current_position == 0
    assert sim.planned_steps == 0
    assert sim.target_position() == 0


def test_full_rotation_forwards():
    sim = HandSimulation()
    sim.current_position = 50
    sim.planned_steps = MAX_STEPS
    while sim.planned_steps != 0:
        sim.try_step()
    assert sim.current_position == 50
    assert sim.planned_steps == 0
    assert sim.target_position() == 50


def test_full_rotation_backwards():
    sim = HandSimulation()
    sim.current_position = 60
    sim.planned_steps = - MAX_STEPS
    while sim.planned_steps != 0:
        sim.try_step()
    assert sim.current_position == 60
    assert sim.planned_steps == 0
    assert sim.target_position() == 60
