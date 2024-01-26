"""calculate new velocities after collition and avoid overlaps"""
import time
import numpy as np
import pygame


def bounce_velocities(ball1, ball2, game):
    """applies elastic bounce physics"""

    p1 = ball1.p
    p2 = ball2.p
    if np.array_equal(p2, p1):
        # move to avoid zero division
        p2 = p2 + (1, -1)
    m1 = ball1.mass
    m2 = ball2.mass
    if ball1.grabed:  # to simulate it's fixed
        m1 = 1000000000
    if ball2.grabed:
        m2 = 1000000000
    # versor collition
    vc = np.array((p2 - p1) / np.linalg.norm(p2 - p1), dtype=np.float64)
    # versor perpendicular
    vp = np.array([vc[1], -vc[0]], dtype=np.float64)

    # perpendicular components of v
    v1c = (np.dot(ball1.v, vc)) * vc
    v2c = (np.dot(ball2.v, vc)) * vc
    # parallel components of v
    v1p = (np.dot(ball1.v, vp)) * vp
    v2p = (np.dot(ball2.v, vp)) * vp
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

    overlap = abs(np.linalg.norm(ball2.p - ball1.p) -
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
    mouse.p = np.array(pygame.mouse.get_pos(), dtype=np.float64)
    ball1.p = np.array(pygame.mouse.get_pos(), dtype=np.float64) - d
    mouse.rect.center = mouse.p
    ball1.rect.center = ball1.p
    # move ball with the mouse
    if (time.perf_counter() - mouse.time) > 0.1:
        rel = pygame.mouse.get_rel()
        mouse.v = (1/(time.perf_counter() - mouse.time)) * \
            np.array((rel), dtype=np.float64)
        mouse.time = time.perf_counter()
        ball1.v = mouse.v


def attraction(ball,game) -> np.array:
    """calculate attraction generated for the other balls"""

    att = np.array([0, 0], dtype=np.float64)

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
                if np.array_equal(p2, p1):
                    p2 += (balls[n].radius+ball.radius, 0)
                va = (p2 - p1) / np.linalg.norm(p2 - p1)
                # Newton gravitation law
                att += game.settings.attraction_k * np.array(
                    ((balls[n].mass) / (np.linalg.norm(p2 - p1)) ** 2) * va,
                    dtype=np.float64,
                )

                # start velocity to achive balls orbite
            if ball.mode == "orbite" and (att[0] != 0 or att[1] != 0):
                # v = sqrt(a*r)*(perpendicular to 'a' versor)
                ball.v = np.array(np.sqrt(np.linalg.norm(att) *\
                np.linalg.norm(game.wbf.mass_center - ball.p))) *\
                (att[1], -att[0])/np.linalg.norm(att)
                ball.mode = None
    return att

def mass_center(balls):
    """calculate mass center"""

    count_mass_center = np.array((0, 0), dtype=np.float64)
    total_mass = np.float64(0)
    for ball in balls.values():
        if str(type(ball)) != "<class 'mouse.Mouse'>":
            total_mass += ball.mass
            count_mass_center += ball.p * ball.mass

    return  count_mass_center/total_mass
