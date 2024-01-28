"""do the physics between the frames"""

import time
import pygame
from searching_for_overlaps import sweep_kdtree, fill_kdtree
from apply_physics import attraction, mass_center
V = pygame.math.Vector2


class Wbf:
    """"worh bwtweeen frams"""
    def __init__(self) -> ():
        self.time = time.perf_counter()
        self.dt = time.perf_counter()
        self.preselected = set()
        self.grabed = None
        self.mass_center = V((0, 0))
        self.attraction_flag = False
        self.gravity_flag = False
        self.grab_flag = False
        self.ball_grabed = None  # the number of the ball that is grabed
        self.energy_loss_flag = False
        self.select_flag = False
        self.pause_flag = False
        self.store_grid_flag = True  # store grid just first time

    def work(self,game):
        """do physics, check for collitions,make gravity,change velocities"""

        c = 0  # to pass statics
        start = time.perf_counter()
        end = start
        balls = game.balls_dict

        # while time is under screen refresh time do the work
        self.store_grid_flag = True
        while (end - start) < (1 / 60):

            s = time.perf_counter()
            self.dt = time.perf_counter()  - self.time
            self.time = time.perf_counter()

            if self.pause_flag:
                self.dt = 0
            # move balls
            for ball in balls.values():
                if str(type(ball)) != "<class 'mouse.Mouse'>":
                    ball.update(self)
            # check kdtree for overlaps and bounces
            kdtree_cells = []
            fill_kdtree(balls.keys(), game, kdtree_cells, self.store_grid_flag)
            self.store_grid_flag = False
            sweep_kdtree(kdtree_cells, balls, game, self)
            # update attraction of each ball
            if len(game.balls_dict) > 0:
                self.mass_center = mass_center(balls)
            if self.attraction_flag:
                for ball in balls.values():
                    if str(type(ball)) != "<class 'mouse.Mouse'>":
                        ball.att = attraction(ball,game)
            # move balls according to attraction
            if self.attraction_flag or self.gravity_flag:
                for ball in balls.values():
                    if str(type(ball)) != "<class 'mouse.Mouse'>":
                        ball.update_acceleration(game,self)
            end = time.perf_counter()
            c = 1 / (end - s)
        return c
