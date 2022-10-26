from controller.model.clock_wall import ClockWall


def test_clock_wall_plan_execution():
    wall = ClockWall(8, 3)
    wall.planning.clocks[4].hour.set_target_position(90)
    wall.execute_plan()

    assert wall.simulation.clocks[4].hour.current_position == 90
