import asyncio

from controller.model.clock_wall import ClockWall


class ADClock:
    wall: ClockWall

    def __init__(self):
        # TODO Load clock wall from configuration
        self.wall = ClockWall(8, 3)

    async def run_simulation(self):
        """
        Refresh simulation for clock wall
        """
        while True:
            await asyncio.gather(asyncio.sleep(0.004), self.wall.simulation.tick_async())


adclock = ADClock()
