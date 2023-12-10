"""         BALL BOUNCING GAME.

left click : throw balls
mid click : throw special orbite balls
The longer you press,thebigger the ball; the more you move the mouse, 
the faster the ball
right click : grab one ball
l Shift + right click + sweep: select/deselect balls
del : delete ball/balls
l: toggle loss energy for friction and bounce
g : toggle Earth's gravity
a : toggle attraction
t : toggle ball traces
By Pablo Daniel Sotes pablodsotes@yahoo.com.ar"""

import numpy as np
import pygame
from check_inputs import ChIn
from draw_on_screen import Screen
from work_between_frames import Wbf

class Game:
    """Initialize the screen and varibles of the game and run it"""

    def __init__(self) -> None:
        pygame.init()
        self.inputs = ChIn(self)
        self.settings = Settings()
        self.screen = Screen(self)
        self.wbf = Wbf()
        self.showing_ball = None
        self.balls_dict = {}
        self.ball_count = 0
        self.c = 0

    def run(self):
        """draw the frame"""

        while True:
            self.inputs.check_in(self)
            self.c = self.wbf.work(self)
            self.screen.image.fill((self.settings.background_color))
            self.screen.draw_traces(self)
            self.screen.draw_grid()
            self.screen.draw_balls(self)
            self.screen.draw_mouse(self)
            pygame.display.update()
            print(self.ball_count, self.c)

class Settings:
    """All the settings"""

    def __init__(self) -> None:
        self.screen_width = 800
        self.screen_height = 800
        self.background_color = (100, 100, 100, 255)
        self.color = (255, 0, 0, 0)
        self.G = np.float64(200)
        self.attraction_k = np.float64(100)


if __name__ == "__main__":
    game = Game()

    game.run()
