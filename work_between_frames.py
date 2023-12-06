"""do the physics between the frames"""

import time
import numpy as np
from searching_for_overlaps import sweep_matrix, fill_matrix
from apply_physics import attraction, mass_center


class Wbf:
    """"worh bwtweeen frams"""
    def __init__(self) -> ():
        self.time = time.perf_counter()
        self.dt = time.perf_counter()
        self.preselected = set()
        self.grabed = None
        self.mass_center =np.array((0,0),dtype=np.float64)
        self.attraction_flag = False
        self.gravity_flag = False
        self.grab_flag = False
        self.ball_grabed = None  # the number of the ball that is grabed
        self.energy_loss_flag = False
        self.select_flag = False
        self.pause_flag = False

    def work(self,game):
        """do physics, check for collitions,make gravity,change velocities"""

        c = 0  # to pass statics
        start = time.perf_counter()
        end = start
        balls = game.balls_dict
        # 8x8
        matrix = [[[]for _ in range(8)] for _ in range(8)]

        # while time is under screen refresh time do the work
        while (end - start) < (1 / 60):


            self.dt = time.perf_counter()  - self.time
            self.time = time.perf_counter()
            if self.pause_flag:
                self.dt = 0

            s = time.perf_counter()
            fill_matrix(matrix, balls, game)
            sweep_matrix(matrix,balls,game,self)
            self.mass_center = mass_center(balls)
            for ball in balls.values():
                if str(type(ball)) != "<class 'mouse.Mouse'>":
                    ball.update(self)
                    if self.attraction_flag:
                        ball.att = attraction(ball,game)
            if self.attraction_flag or self.gravity_flag:
                for ball in balls.values():
                    if str(type(ball)) != "<class 'mouse.Mouse'>":
                        ball.update_acceleration(game,self)
            end = time.perf_counter()
            c = 1 / (end - s)
        return c
