"""Fill and sweep the grid seaching for collitions , mouse grab, or selection"""

import numpy as np
from apply_physics import wall_bounce, grab, bounce_velocities


def fill_matrix(matrix, balls, game):
    """fill matrix with ball numbers inside each cell"""

    sw = game.settings.screen_width
    sh = game.settings.screen_height

    # clear the matrix
    for row in matrix:
        for lst in row:
            lst.clear()

    for nr, ball in balls.items():
        # asign ball to its cell/s on matrix
        l = grid(ball.rect.left, sw)
        r = grid(ball.rect.right, sw)
        t = grid(ball.rect.top, sh)
        b = grid(ball.rect.bottom, sh)
        # for all the cell the ball encompass
        for i in range(t, b + 1):
            for j in range(l, r + 1):
                matrix[i][j].append(nr)


def grid(edge, size):
    """compares each ball edge with lines of the grid"""

    if edge > size / 2:
        if edge >= 3 * size / 4:
            if edge > 7 * size / 8:
                return 7
            return 6
        if edge >= 5 * size / 8:
            return 5
        return 4
    if edge >= size / 4:
        if edge >= 3 * size / 8:
            return 3
        return 2
    if edge >= size / 8:
        return 1
    return 0


def sweep_matrix(matrix, balls, game,wbf):
    """check for collitions for each cell in the matrix"""

    already_checked = set()
    wbf.preselected = set()
    # sweep 64 cells
    for i in range(0, 8):
        for j in range(0, 8):
            for n in range(len(matrix[i][j])):
                # for each ball key and for the other ball keys
                k1 = matrix[i][j][n]
                for m in range(n + 1, len(matrix[i][j])):
                    k2 = matrix[i][j][m]
                    # some balls share more than one cell
                    if (k1, k2) in already_checked:
                        continue
                    already_checked.add((k1, k2))
                    if overlaps(balls[k1], balls[k2]):
                        if str(type(balls[k2])) != "<class 'mouse.Mouse'>" and\
                            str(type(balls[k1])) != "<class 'mouse.Mouse'>":
                            bounce_velocities(balls[k1], balls[k2], game)
                        elif balls[k2].mode == "select":
                            wbf.preselected.add(k1)

                        # if k1 is already grabed or no ball is grabed
                        elif k1 == wbf.ball_grabed or not wbf.ball_grabed:
                            wbf.ball_grabed = k1
                            grab(balls[k1], balls[k2])

                if i == 0 or i == 7 or j == 0 or j == 7:
                    wall_bounce(balls[k1], game)


def overlaps(ball1, ball2) -> bool:
    """check if balls overlap"""
    # checking for horizontal proyection overlap
    if (ball1.rect.right > ball2.rect.left) and (ball1.rect.left < ball2.rect.right):
        # checking for vertical proyection overlap
        if (ball1.rect.bottom > ball2.rect.top) and (
            ball1.rect.top < ball2.rect.bottom
        ):
            # only check the rectangle
            if ball2.mode == "select":
                return True
            # checking if actualy touching or overlap
            if np.linalg.norm(ball2.p - ball1.p) <= (ball1.radius + ball2.radius):
                return True
    return False
