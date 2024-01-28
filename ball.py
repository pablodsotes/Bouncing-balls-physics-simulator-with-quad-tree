"""Ball class and metods"""

# pylint: disable=E0203

import time
import random
import pygame
import numpy as np
V = pygame.math.Vector2


class Ball():
    """define a ball with all its attributes"""

    def __init__(self,game, **kwargs):
        self.game = game
        self.grabed = False
        self.number = kwargs.get("count")
        self.mode = kwargs.get("mode")
        self.selected = False
        self.color = pygame.Color(255,0,0,255)
        if self.mode == "key":
            self.radius = 5
            self.p = V(
                50+50*random.random(), 50+50*random.random())
            self.v = V(30, 30)
        else:
            self.radius = 30 * (time.perf_counter() - kwargs.get("mst"))
            self.p = V(pygame.mouse.get_pos())
            self.v = V(pygame.mouse.get_pos()) - V(kwargs.get("msp"))
        self.trace_p = [int(self.p[0]),int(self.p[1])]
        self.mass = (3 * (self.radius**2))
        self.rect = pygame.Rect((0, 0, 2 * self.radius, 2 * self.radius))
        self.rect.center = self.p
        self.att = V((0, 0))

    def draw(self):
        """draw ball"""

        # pylint: disable=E1101
        if not self.selected:
            self.color.hsva = (
                min(0.3 * (self.v).magnitude(), 270), 100, 100, 100)
        pygame.draw.circle( self.game.screen.image,(self.color),(self.p),self.radius)



                # draw arrow
        if self.game.wbf.attraction_flag:
            p = self.p
            w = self.att / 50
            a, b = (1.5 * w[1] + 13.5 * w[0] + p[0], -
                    1.5 * w[0] + 13.5 * w[1] + p[1])
            c, d = (-1.5 * w[1] + 13.5 * w[0] + p[0],
                    1.5 * w[0] + 13.5 * w[1] + p[1])
            pygame.draw.polygon(
                self.game.screen.image, (255, 255, 255, 255), [
                    (14 * w + p), (a, b), ((20 * w + p)), (c, d)]
            )
            pygame.draw.line(
                self.game.screen.image,
                (255, 255, 255, 255),
                (p),
                ((p[0] + 17 * w[0], p[1] + 17 * w[1])),
                max(abs(int((w).magnitude())), 1),
            )
            
    def update(self,wbf):
        """update ball position"""

        if not wbf.grab_flag:
            #loose all balls
            self.grabed = False

        if not self.grabed:
            self.p += self.v * wbf.dt
            self.rect.center = self.p
            #energy loss
            self.v[1] -= wbf.energy_loss_flag * ((0.01 * self.v[1]) ** 3) * wbf.dt
            self.v[0] -= wbf.energy_loss_flag * ((0.01 * self.v[0]) ** 3) * wbf.dt

    def update_acceleration(self,game,wbf):
        """update v and p because of acceleration"""
        # atraction + gravity
        a = V((0, 0))
        a[1] = wbf.gravity_flag * game.settings.G + wbf.attraction_flag * self.att[1]
        a[0] = wbf.attraction_flag * self.att[0]
        self.p += (0.5 * a * (wbf.dt**2))
        self.v = self.v + wbf.dt*a
