"""Screen class with draw objects methods"""

import time
import pygame

WHITE = (255,255,255)

class Screen:
    """The screen with its draw methods"""
    def __init__(self,game):
        self.image = pygame.display.set_mode(
            (game.settings.screen_width, game.settings.screen_height)
        )
        pygame.display.set_caption("bouncing balls")
        self.image.fill((game.settings.background_color))
        self.trace_image = pygame.Surface((800, 800), pygame.SRCALPHA)
        self.trace_image.fill(game.settings.background_color)
        self.trace_color = pygame.Color(0,0,0,255)
        self.trace_flag = False

    def draw_balls(self,game):
        """draw balls"""

        for ball in game.balls_dict.values():
            if str(type(ball)) != "<class 'mouse.Mouse'>":
                ball.draw()
        if game.showing_ball:
            game.showing_ball.draw(game)

    def draw_grid(self):
        """draw grid"""

        for i in range(1, 8):
            pygame.draw.line(self.image, WHITE,(0, i * 100), (800, i * 100))
            pygame.draw.line(self.image, WHITE,(i * 100, 0), (i * 100, 800))

    def draw_mouse(self,game):
        """draw mouse frame"""

        mouse = game.balls_dict.get(0)
        if mouse:
            mouse.draw()

    def draw_traces(self,game):
        """draw_balls_and_traces"""

        if self.trace_flag:
            self.image.blit(self.trace_image, (0, 0))

            for ball in game.balls_dict.values():
                if str(type(ball)) != "<class 'mouse.Mouse'>":
                    #sometime balls are out of the screen
                    try:
                        #if pixel had changed
                        if ball.trace_p[0] !=int(ball.p[0]) or ball.trace_p[1] !=int(ball.p[1]):
                            ball.trace_p = [int(ball.p[0]),int(ball.p[1])]
                            pixel=self.trace_image.get_at(ball.trace_p)
                            self.trace_color.hsva= ((time.time()/10)%360,100,100,100)
                            self.trace_color= self.trace_color.lerp(pixel,0.90)
                            self.trace_image.set_at(ball.trace_p, (self.trace_color))
                    # if ball is out of screen , no problem, do nothing
                    except IndexError:
                        pass
            if game.wbf.attraction_flag:
                pygame.draw.circle(self.trace_image,(0,0,0,255),(game.wbf.mass_center),1)
