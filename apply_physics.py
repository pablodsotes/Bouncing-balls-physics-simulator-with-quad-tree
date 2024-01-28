"""calculate new velocities after collition and avoid overlaps"""
import time
import math
import pygame
V = pygame.math.Vector2



def bounce_velocities(ball1, ball2, game):
    """applies elastic bounce physics"""

    p1 = ball1.p
    p2 = ball2.p
    if p2 == p1:
        # move to avoid zero division
        p2 = p2 + (1, -1)
    m1 = ball1.mass
    m2 = ball2.mass
    if ball1.grabed:  # to simulate it's fixed
        m1 = 1000000000
    if ball2.grabed:
        m2 = 1000000000
    # versor collition
    vc = V(V(p2 - p1)).normalize()
    # versor perpendicular
    vp = vc.rotate(90)

    # perpendicular components of v
    v1c = (ball1.v).project(vc)
    v2c = (ball2.v).project(vc)
    # parallel components of v
    v1p = (ball1.v).project(vp)
    v2p = (ball2.v).project(vp)
    # elastic bounce equations
    v1 = v1p + ((m1 - m2) / (m1 + m2)) * v1c + \
        (2 * m2 / (m1 + m2)) * v2c  # new veloc
    v2 = v2p + ((m2 - m1) / (m2 + m1)) * v2c + \
        (2 * m1 / (m2 + m1)) * v1c  # new veloc

    k = 1 - 0.05 * game.wbf.energy_loss_flag
    # applay new velocities
    if not ball1.grabed:
        ball1.v = k * v1
    if not ball2.grabed:
        ball2.v = k * v2

    overlap = abs((ball2.p - ball1.p).length() -
                  (ball1.radius + ball2.radius))
    # move away balls
    if not ball1.grabed:
        ball1.p -= overlap * vc * ball2.mass / (ball1.mass + ball2.mass)
    if not ball2.grabed:
        ball2.p += overlap * vc * ball1.mass / (ball2.mass + ball1.mass)

def wall_bounce(ball, game):
    """if bounce at a wall ,changes ball velocity and push the ball in"""

    if ball.p[0] + ball.radius > game.settings.screen_width:  # right wall
        ball.v[0] = -abs(ball.v[0])
        ball.p[0] -= (ball.p[0] - game.settings.screen_width + ball.radius)
    if ball.p[0] - ball.radius < 0:  # left wall
        ball.v[0] = abs(ball.v[0])
        ball.p[0] -= (ball.p[0] - ball.radius)
    if ball.p[1] + ball.radius - game.settings.screen_height > 0:  # floor
        ball.v[1] = -abs(ball.v[1])
        ball.p[1] -= (ball.p[1] - game.settings.screen_height + ball.radius)
    if ball.p[1] - ball.radius < 0:  # roof
        ball.v[1] = abs(ball.v[1])
        ball.p[1] -= (ball.p[1] - ball.radius)


def grab(ball1, mouse):
    """grab a ball with the mouse"""

    ball1.grabed = True
    d = mouse.p - ball1.p
    mouse.p = V(pygame.mouse.get_pos())
    ball1.p = V(pygame.mouse.get_pos()) - d
    mouse.rect.center = mouse.p
    ball1.rect.center = ball1.p
    # move ball with the mouse
    if (time.perf_counter() - mouse.time) > 0.1:
        rel = pygame.mouse.get_rel()
        mouse.v = (1/(time.perf_counter() - mouse.time)) * \
            V((rel))
        mouse.time = time.perf_counter()
        ball1.v = mouse.v


def attraction(ball,game):
    """calculate attraction generated for the other balls"""

    att = V(0, 0)

    balls = ball.game.balls_dict
    game = ball.game
    p1 = ball.p
    for n in balls.keys():
        # if not balls[n].mode == "grab" and not balls[n].mode == "select":
        if str(type(balls[n])) != "<class 'mouse.Mouse'>":
            if n != ball.number:
                p1 = ball.p
                p2 = balls[n].p

                # attraction versor
                if p2 == p1:
                    p2 += (balls[n].radius+ball.radius, 0)
                va = (p2 - p1).normalize()
                # Newton gravitation law
                att += game.settings.attraction_k * (
                    ((balls[n].mass) / (p2 - p1).length_squared())) * va

                # start velocity to achive balls orbite
            if ball.mode == "orbite" and (att[0] != 0 or att[1] != 0):
                # v = sqrt(a*r)*(perpendicular to 'a' versor)
                ball.v = math.sqrt((att).magnitude(
                ) * (game.wbf.mass_center - ball.p).length()) * (att.normalize()).rotate(90)
                ball.mode = None
    return att

def mass_center(balls):
    """calculate mass center"""

    count_mass_center = V((0, 0))
    total_mass = 0
    for ball in balls.values():
        if str(type(ball)) != "<class 'mouse.Mouse'>":
            total_mass += ball.mass
            count_mass_center += ball.p * ball.mass

    return  count_mass_center/total_mass
