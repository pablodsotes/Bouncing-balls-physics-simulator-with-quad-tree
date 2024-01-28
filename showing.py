"""A ball that its been throwed"""

import time

import pygame
V = pygame.math.Vector2


class ShowingBall():
    """show the ball that will be created"""

    def __init__(self, game, **kwargs):
        self.mst = kwargs.get("mst")
        self.msp = kwargs.get("msp")
        self.game = game
        self.color = pygame.Color(255, 0, 0, 255)
        self.v = V((0, 0))

    def draw(self, game):
        """draw showing ball"""

        self.v = V(pygame.mouse.get_pos()) - V(self.msp)
        game.showing_ball.color.hsva = (
            min(0.3 * (game.showing_ball.v).magnitude(), 270), 100, 100, 100)
        radius = 30 * (time.perf_counter() - self.mst)
        r = radius
        p = pygame.mouse.get_pos()
        pygame.draw.circle(game.screen.image, (self.color), (p), r)

        # draw arrow
        w = self.v / 100
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
            int((w).magnitude()),
        )
