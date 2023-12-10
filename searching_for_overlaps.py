"""Fill and sweep the grid seaching for collitions , mouse grab, or selection"""

import numpy as np
from apply_physics import wall_bounce, grab, bounce_velocities


def fill_kdtree(ball_keys, game, groups, store_grid_flag):
    """fills kdtree groups"""
    center = (game.settings.screen_width/2, game.settings.screen_height/2)
    Node(center, 1, ball_keys, game, groups, store_grid_flag)


class Node:
    """a node with a center an a list of ball keys inside it"""

    def __init__(self, center, depth, ball_keys, game, groups, store_grid_flag) -> None:
        self.center = center
        self.depth = depth
        self.size = game.settings.screen_width/(2**depth)
        self.cells = [[], [], [], []]
        self.ball_keys = ball_keys
        self.divide(game, groups, store_grid_flag)
        if store_grid_flag:
            self.store_grid(game)

    def divide(self, game, groups, store_grid_flag):
        """divide cell if it correspond"""
        balls = game.balls_dict
        for k in self.ball_keys:
            # asign ball to its/their cell/s
            # evaluate each of 4 corners of the ball rect
            lt = split_in_4(balls[k].rect.left, balls[k].rect.top, self.center)
            rt = split_in_4(balls[k].rect.right,
                            balls[k].rect.top, self.center)
            lb = split_in_4(balls[k].rect.left,
                            balls[k].rect.bottom, self.center)
            rb = split_in_4(balls[k].rect.right,
                            balls[k].rect.bottom, self.center)
            # if any corner of ball's rect is in the cell,append ball
            if lt == 0 or rt == 0 or lb == 0 or rb == 0:
                self.cells[0].append(k)
            if lt == 1 or rt == 1 or lb == 1 or rb == 1:
                self.cells[1].append(k)
            if lt == 2 or rt == 2 or lb == 2 or rb == 2:
                self.cells[2].append(k)
            if lt == 3 or rt == 3 or lb == 3 or rb == 3:
                self.cells[3].append(k)

        for i in range(4):
            # if cell is short or prof is big don't divide again
            if len(self.cells[i]) in range(1, 10) or self.depth > 7:
                # save cell as it is
                groups.append(self.cells[i])
                continue
            # new center
            if len(self.cells[i]) == 0:
                continue
            if i in (0, 2):
                x = self.center[0]-self.size/2
            if i in (1, 3):
                x = self.center[0]+self.size/2
            if i in (0, 1):
                y = self.center[1]-self.size/2
            if i in (2, 3):
                y = self.center[1]+self.size/2
            # create new node with new center and +1 prof
            Node((x, y), self.depth+1,
                 self.cells[i], game, groups, store_grid_flag)

    def store_grid(self, game):
        """add each cross to be drawn later"""

        a = (self.center[0]-self.size, self.center[1])
        b = (self.center[0]+self.size, self.center[1])
        c = (self.center[0], self.center[1]-self.size)
        d = (self.center[0], self.center[1]+self.size)

        game.screen.grid.append([a, b])
        game.screen.grid.append([c, d])


def split_in_4(bx, by, center):
    """to what of 4 qudrants points belong"""

    x = center[0]
    y = center[1]
    if bx <= x:
        if by <= y:
            return 0
        return 2
    if by <= y:
        return 1
    return 3


def sweep_kdtree(kdtree_cells, balls, game, wbf):
    """check for collitions for each cell in the matrix"""

    already_checked = set()
    wbf.preselected = set()
    # sweep kdtree cells
    for cell in kdtree_cells:
        for i, n in enumerate(cell):
            k1 = n
            for m in range(i+1, len(cell)):
                k2 = cell[m]
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
