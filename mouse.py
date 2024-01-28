"""Mouse select and mouse grabing"""

import time
import pygame
V = pygame.math.Vector2


class Mouse():
    """an object that represent mouse grabing or selection frame"""

    def __init__(self, game, **kwargs):
        self.p = V(pygame.mouse.get_pos())
        self.radius = 1
        self.rect = pygame.Rect(self.p[0], self.p[1], 1, 1)
        self.rect.center = self.p
        self.v = V((0, 0))
        self.msp = self.p
        self.mode = kwargs.get("mode")
        self.game = game
        self.time = time.perf_counter()

    def draw(self):
        """resizes the selection frame aand drwaw it"""

        if self.mode == "select":
            width = abs(pygame.mouse.get_pos()[0]-self.msp[0])
            height = abs(pygame.mouse.get_pos()[1] - self.msp[1])
            if pygame.mouse.get_pos()[0]-self.msp[0] > 0:
                self.rect.left = self.msp[0]
            else:
                self.rect.left = pygame.mouse.get_pos()[0]
            if pygame.mouse.get_pos()[1] - self.msp[1] > 0:
                self.rect.top = self.msp[1]
            else:
                self.rect.top = pygame.mouse.get_pos()[1]
            self.rect.width = width
            self.rect.height = height

            pygame.draw.rect(self.game.screen.image,
                             (255, 255, 255, 255), self.rect, 1)
