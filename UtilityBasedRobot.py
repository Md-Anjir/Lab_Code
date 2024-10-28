import pygame
import random
import time
from collections import deque

# Constants
ROWS = 6
COLS = 7
CELL_SIZE = 50
WIN_WIDTH = COLS * CELL_SIZE
WIN_HEIGHT = ROWS * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)  # New color for nearest object

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.2:
                    self.grid[i][j] = 1  # Hurdle
                elif random.random() < 0.4:
                    self.grid[i][j] = 2  # Object

    def draw(self, win, nearest_object):
        for i in range(self.rows):
            for j in range(self.cols):
                pygame.draw.rect(win, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                if self.grid[i][j] == 1:
                    pygame.draw.rect(win, RED, (j * CELL_SIZE + 5, i * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))
                elif self.grid[i][j] == 2:
                    if (i, j) == nearest_object:
                        pygame.draw.circle(win, ORANGE, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
                    else:
                        pygame.draw.circle(win, GREEN, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

class Robot:
    def __init__(self, grid):
        self.grid = grid
        self.row = random.randint(1, grid.rows - 2)
        self.col = random.randint(1, grid.cols - 2)
        while self.grid.grid[self.row][self.col] == 1:
            self.row = random.randint(1, grid.rows - 2)
            self.col = random.randint(1, grid.cols - 2)
        self.path = [(self.row, self.col)]

    def move_to(self, position):
        self.row, self.col = position
        self.path.append((self.row, self.col))

    def draw(self, win):
        pygame.draw.circle(win, BLUE, (self.col * CELL_SIZE + CELL_SIZE // 2, self.row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        for i, j in self.path:
            pygame.draw.circle(win, YELLOW, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 8)


def is_hurdle_free(grid, row, col, visited):
    """
    Check if the given position (row, col) is within bounds, not a hurdle, and not visited.
    """
    if 0 <= row < grid.rows and 0 <= col < grid.cols:
        if grid.grid[row][col] != 1 and (row, col) not in visited:
            return True
    return False


def bfs_find_path(grid, start, end):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        # If the end is reached, return the path
        if current == end:
            return path

        for direction in directions:
            new_row, new_col = current[0] + direction[0], current[1] + direction[1]

            # Use the new hurdle-checking function here
            if is_hurdle_free(grid, new_row, new_col, visited):
                queue.append(((new_row, new_col), path + [(new_row, new_col)]))

    return None


def find_nearest_object(grid, robot):
    min_distance = float('inf')
    nearest_object = None

    for i in range(grid.rows):
        for j in range(grid.cols):
            if grid.grid[i][j] == 2:
                path = bfs_find_path(grid, (robot.row, robot.col), (i, j))
                if path and len(path) < min_distance:
                    min_distance = len(path)
                    nearest_object = (i, j)

    return nearest_object


def collect_object(grid, robot):
    if grid.grid[robot.row][robot.col] == 2:
        grid.grid[robot.row][robot.col] = 0
        return True
    return False


def move_towards_object(grid, robot, obj_pos):
    path = bfs_find_path(grid, (robot.row, robot.col), obj_pos)
    if path:
        for step in path:
            robot.move_to(step)
            break  # Move one step towards the object


def main():
    for _ in range(5):
        pygame.init()
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Robot Navigation")

        grid = Grid(ROWS, COLS)
        grid.randomize()
        robot = Robot(grid)


        clock = pygame.time.Clock()
        running = True

        if collect_object(grid, robot):
            print("Object collected!")
        pygame.display.update()
        clock.tick(1)


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Find the nearest object
            nearest_object = find_nearest_object(grid, robot)
            if nearest_object:
                win.fill(WHITE)
                grid.draw(win, nearest_object)
                robot.draw(win)
                pygame.display.update()

                # Step 2: Add a short delay before moving
                time.sleep(1)  # 1 second delay to show marking

                # Move towards the marked object
                move_towards_object(grid, robot, nearest_object)

                if collect_object(grid, robot):
                    print("Object collected!")
                pygame.display.update()
                clock.tick(1)

            # Check if the robot is at the border
            if robot.row == 0 or robot.row == grid.rows - 1 or robot.col == 0 or robot.col == grid.cols - 1:
                print("Robot has reached the border. Stopping.")
                running = False

            # Draw the updated grid and robot position
            win.fill(WHITE)
            grid.draw(win, nearest_object)
            robot.draw(win)
            pygame.display.update()

            # Control the overall frame rate
            clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
