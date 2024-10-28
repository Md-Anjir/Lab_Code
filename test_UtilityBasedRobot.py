from UtilityBasedRobot import Grid, Robot, is_hurdle_free, bfs_find_path, find_nearest_object, collect_object, move_towards_object

# Global variables for tracking test results
total_tests = 0
passed_tests = 0


def test_is_hurdle_free():
    global total_tests, passed_tests
    grid = Grid(6, 7)  # 6 rows, 7 columns
    grid.grid = [
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0]
    ]
    visited = set()

    tests = [
        (is_hurdle_free(grid, 0, 0, visited), True, "Empty cell"),
        (is_hurdle_free(grid, 0, 1, visited), False, "Hurdle cell"),
        (is_hurdle_free(grid, -1, 1, visited), False, "Out of bounds"),
        (is_hurdle_free(grid, 5, 6, visited), True, "Valid cell not visited")
    ]

    # Add (5, 6) to the visited set manually
    visited.add((5, 6))
    tests.append((is_hurdle_free(grid, 5, 6, visited), False, "Already visited"))

    for result, expected, description in tests:
        total_tests += 1
        if result == expected:
            passed_tests += 1
        else:
            print(f"Test failed: is_hurdle_free - {description}")


def test_bfs_find_path():
    global total_tests, passed_tests
    grid = Grid(6, 7)
    grid.grid = [
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0]
    ]

    tests = [
        (bfs_find_path(grid, (0, 0), (1, 6)) is not None, True, "Path with no hurdles"),
        (bfs_find_path(grid, (0, 0), (5, 6)) is not None, True, "Path avoiding hurdles"),
        (bfs_find_path(grid, (0, 0), (2, 0)) is None, True, "Blocked by hurdles"),
    ]

    for result, expected, description in tests:
        total_tests += 1
        if result == expected:
            passed_tests += 1
        else:
            print(f"Test failed: bfs_find_path - {description}")

def test_find_nearest_object():
    global total_tests, passed_tests
    grid = Grid(6, 7)
    grid.grid = [
        [0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 2],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0]
    ]
    robot = Robot(grid)
    robot.row, robot.col = 1, 1

    nearest_object = find_nearest_object(grid, robot)
    total_tests += 1
    if nearest_object == (0, 2):
        passed_tests += 1
    else:
        print("Test failed: find_nearest_object")

def test_collect_object():
    global total_tests, passed_tests
    grid = Grid(6, 7)
    grid.grid = [
        [0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    robot = Robot(grid)
    robot.row, robot.col = 0, 2

    total_tests += 1
    if collect_object(grid, robot) and grid.grid[0][2] == 0:
        passed_tests += 1
    else:
        print("Test failed: collect_object at robot's position")

    robot.row, robot.col = 1, 1
    total_tests += 1
    if not collect_object(grid, robot):
        passed_tests += 1
    else:
        print("Test failed: collect_object with no object")

def test_move_to_and_move_towards_object():
    global total_tests, passed_tests
    grid = Grid(6, 7)
    grid.grid = [
        [0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0]
    ]
    robot = Robot(grid)
    robot.row, robot.col = 1, 1

    robot.move_to((0, 1))
    total_tests += 1
    if robot.row == 0 and robot.col == 1 and robot.path[-1] == (0, 1):
        passed_tests += 1
    else:
        print("Test failed: move_to")

    move_towards_object(grid, robot, (0, 2))
    total_tests += 1
    if robot.row == 0 and robot.col == 2:
        passed_tests += 1
    else:
        print("Test failed: move_towards_object")

def run_all_tests():
    global total_tests, passed_tests
    test_is_hurdle_free()
    test_bfs_find_path()
    test_find_nearest_object()
    test_collect_object()
    test_move_to_and_move_towards_object()

    if total_tests > 0:
        pass_percentage = (passed_tests / total_tests) * 100
        print(f"Passed {passed_tests} out of {total_tests} tests.")
        print(f"Pass percentage: {pass_percentage:.2f}%")
    else:
        print("No tests to run.")

# Run tests
if __name__ == "__main__":
    run_all_tests()
