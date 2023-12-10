"""Check mouse and keyboard, cretaes objects and take actions"""


import time
import sys
import pygame
from ball import Ball
from mouse import Mouse
from showing import ShowingBall


class ChIn:
    """check mouse and keyboard and take actions"""

    def __init__(self,game):
        self.game = game
        self.msp = None
        self.mst = None


    def check_in(self, game):
        """check inputs and call the functions for each event"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.check_mb_down(game, event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.check_mb_up(game, event)
            if event.type == pygame.KEYDOWN:
                self.check_key(game, event)

    def check_mb_down(self, game, event):
        """do work for mouse buttons down"""

        self.msp = pygame.mouse.get_pos()
        self.mst = time.perf_counter()
        if event.button == 1 or  event.button == 2:
            self.create_object("showing")
        if event.button == 3 and not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.create_object("grab")
            self.actions("deselect")
        if event.button == 3 and pygame.key.get_pressed()[pygame.K_LSHIFT] and\
            not game.wbf.select_flag:
            self.create_object("select")

    def check_mb_up(self, game, event):
        """do work for mouse buttons up"""

        if event.button == 1:
            self.create_object("click_ball")
        if event.button == 2:
            self.create_object("orbite_ball")
        if event.button == 3:
            if game.wbf.select_flag:
                self.actions("select_balls")
            else:
                self.actions("loose")

    def check_key(self, game, event):
        """do work for mouse keys pressed"""

        if event.key == pygame.K_p:
            game.wbf.pause_flag ^= True   # pause
        if event.key == pygame.K_a:
            game.wbf.attraction_flag ^= True   # toggle attraction
        if event.key == pygame.K_g:
            game.wbf.gravity_flag ^= True      # toggle gravity
        if event.key == pygame.K_l:
            game.wbf.energy_loss_flag ^= True  # toggle loss enrgy
        if event.key == pygame.K_t:
            game.screen.trace_flag ^=True         # toggle trace
            game.screen.trace_image.fill(game.settings.background_color)
        if event.key == pygame.K_n:
            self.create_object("key_ball")
        if event.key == pygame.K_m:
            self.create_object("50_balls")
        if event.key == pygame.K_DELETE:
            if game.wbf.ball_grabed:
                self.actions("delete_grabed")
            else:
                self.actions("delete_selected")



    def create_object(self,mode):
        """create objets according to event"""

        game= self.game
        match mode:

            case "showing":
                game.showing_ball = ShowingBall(game,msp=self.msp, mst=self.mst )
                return
            case "grab":
                game.wbf.grab_flag = True
                #get rel avoyds fake mouse veloc
                pygame.mouse.get_rel()
                # create ball that represent the mouse
                obj = Mouse(game,mode="grab")
                game.balls_dict[0] = obj
            case "select":
                game.wbf.select_flag = True
                obj = Mouse( game, mode="select")
                game.balls_dict[0] = obj
            case "click_ball":
                game.showing_ball = None
                game.ball_count += 1
                obj= Ball(game,msp=self.msp,mst=self.mst,mode="click",count=game.ball_count)
                game.balls_dict[game.ball_count] = obj
            case "orbite_ball":
                game.showing_ball = None
                game.ball_count += 1
                obj= Ball(game,msp=self.msp,mst=self.mst,mode="orbite",count=game.ball_count)
                game.balls_dict[game.ball_count] = obj
            case "key_ball":
                game.ball_count += 1
                # create a ball from the corner
                obj= Ball(game,mode="key",count=game.ball_count)
                game.balls_dict[game.ball_count] = obj
            case "50_balls":
                for _ in range(50):
                    game.ball_count += 1
                    # create a ball from the corner
                    obj= Ball(game,mode="key",count=game.ball_count)
                    game.balls_dict[game.ball_count] = obj



    def actions(self,action):
        """do actions according to event"""
        game= self.game

        match action:

            case "select_balls":
                game.wbf.select_flag= not game.wbf.select_flag
                game.balls_dict.pop(0)
                for key in game.wbf.preselected:
                    if game.balls_dict[key].selected:
                        game.balls_dict[key].selected = False
                        game.balls_dict[key].color =pygame.Color((255,0,0,255))
                    else:
                        game.balls_dict[key].selected = True
                        game.balls_dict[key].color =pygame.Color((70,70,70,255))
            case "deselect":
                for key in game.balls_dict.copy().keys():
                    if not key == 0:
                        game.balls_dict[key].selected = False
            case "loose":
                game.wbf.grab_flag = False
                game.balls_dict.pop(0)
                game.wbf.ball_grabed = None
            case "delete_grabed":
                game.wbf.grab_flag = False
                game.balls_dict.pop(game.wbf.ball_grabed)
                game.wbf.ball_grabed = None
            case "delete_selected":
                for key in game.balls_dict.copy().keys():
                    if not key==0:
                        if game.balls_dict[key].selected:
                            game.balls_dict[key].selected = False
                            game.balls_dict.pop(key)
                game.wbf.select_flag = False
                game.preselected =set()
