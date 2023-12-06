"""Ball class and metods"""

# pylint: disable=E0203

import time
import pygame
import numpy as np


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
            self.radius = 10
            self.p = np.array((30,30), dtype=np.float64)
            self.v = np.array((100,100), dtype=np.float64)
        else:
            self.radius = 30 * (time.perf_counter() - kwargs.get("mst"))
            self.p = np.array(pygame.mouse.get_pos(), dtype=np.float64)
            self.v = np.array(pygame.mouse.get_pos()) - np.array(kwargs.get("msp"),dtype=np.float64)
        self.trace_p = [int(self.p[0]),int(self.p[1])]
        self.mass = np.float64(3 * (self.radius**2))
        self.rect = pygame.Rect((0, 0, 2 * self.radius, 2 * self.radius))
        self.rect.center = self.p
        self.att = np.array((0,0),dtype=np.float64)

    def draw(self):
        """draw ball"""

        # pylint: disable=E1101
        if not self.selected:
            self.color.hsva = (min(0.3 * np.linalg.norm(self.v),270),100,100,100)
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
                max(abs(int(np.linalg.norm(w))),1),
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
        a= np.array((0,0),dtype=np.float64)
        a[1] = wbf.gravity_flag * game.settings.G + wbf.attraction_flag * self.att[1]
        a[0] = wbf.attraction_flag * self.att[0]
        self.p += (0.5 * a * (wbf.dt**2))
        self.v += a * wbf.dt
