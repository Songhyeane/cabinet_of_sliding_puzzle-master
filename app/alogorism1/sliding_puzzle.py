import sys
sys.path.append('/home/hyeane/바탕화면/cabinet_of_sliding_puzzle-master/app')

import getopt
import sys

import numpy as np

# from solver import Solver
from app.alogorism1.solver import Solver


# samples
# goal_state = np.array([[1, 2, 3],
#                       [4, 5, 6],
#                       [7, 8, 0]])
#
# init_state = np.array([[1, 8, 7],
#                       [3, 0, 5],
#                       [4, 6, 2]])

def BFS(init_state, goal_state, max_iter, heuristic):
    solver = Solver(init_state, goal_state, heuristic, max_iter)
    path = solver.solve_bfs()
    step = 0
    orders = []

    if len(path) == 0:
        exit(1)

    init_idx = init_state.flatten().tolist().index(0)
    init_i, init_j = init_idx // goal_state.shape[0], init_idx % goal_state.shape[0]

    # print()
    # print('INITIAL STATE')
    for i in range(goal_state.shape[0]):
        pass
        # print(init_state[i, :])
    # print()
    for node in reversed(path):
        step += 1
        cur_idx = node.get_state().index(0)
        cur_i, cur_j = cur_idx // goal_state.shape[0], cur_idx % goal_state.shape[0]

        new_i, new_j = cur_i - init_i, cur_j - init_j

        direction = 0

        unit = node.get_state()[init_i * 3 + init_j]

        if new_j == 0 and new_i == -1:
            direction = 2
            # print('Moved UP    from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        elif new_j == 0 and new_i == 1:
            direction = 0
            # print('Moved DOWN  from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        elif new_i == 0 and new_j == 1:
            direction = 3
            # print('Moved RIGHT from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        else:
            direction = 1
        # print('Moved LEFT  from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        # print('Score using ' + heuristic + ' heuristic is ' + str(node.get_score() - node.get_level()) + ' in level ' + str(node.get_level()))

        init_i, init_j = cur_i, cur_j

        for i in range(goal_state.shape[0]):
            pass
            # print(np.array(node.get_state()).reshape(goal_state.shape[0], goal_state.shape[0])[i, :])

        # print(unit)
        orders.append([step, unit, direction])
        # print()

    return orders
    # print(solver.get_summary())


def A_star(init_state, goal_state, max_iter, heuristic):
    solver = Solver(init_state, goal_state, heuristic, max_iter)
    path = solver.solve_a_star()
    step = 0
    orders = []

    if len(path) == 0:
        exit(1)

    init_idx = init_state.flatten().tolist().index(0)
    init_i, init_j = init_idx // goal_state.shape[0], init_idx % goal_state.shape[0]

    # print()
    # print('INITIAL STATE')
    for i in range(goal_state.shape[0]):
        pass
        # print(init_state[i, :])
    # print()
    for node in reversed(path):
        step += 1
        cur_idx = node.get_state().index(0)
        cur_i, cur_j = cur_idx // goal_state.shape[0], cur_idx % goal_state.shape[0]

        new_i, new_j = cur_i - init_i, cur_j - init_j

        direction = 0

        unit = node.get_state()[init_i * 3 + init_j]

        if new_j == 0 and new_i == -1:
            direction = 2
            # print('Moved UP    from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        elif new_j == 0 and new_i == 1:
            direction = 0
            # print('Moved DOWN  from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        elif new_i == 0 and new_j == 1:
            direction = 3
            # print('Moved RIGHT from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        else:
            direction = 1
            # print('Moved LEFT  from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j))+'direction'+str(direction))
        # print('Score using ' + heuristic + ' heuristic is ' + str(node.get_score() - node.get_level()) + ' in level ' + str(node.get_level()))

        init_i, init_j = cur_i, cur_j

        # print(node.get_state())

        for i in range(goal_state.shape[0]):
            pass
            # print(np.array(node.get_state()).reshape(goal_state.shape[0], goal_state.shape[0])[i, :])

        # print(unit)
        orders.append([step, unit, direction])
        # print()

    return orders
    # print(solver.get_summary())


def main(argv, init_state, goal_state):
    max_iter = 5000
    heuristic = "manhattan"
    algorithm = "a_star"
    n = 3

    try:
        opts, args = getopt.getopt(argv, "hn:", ["mx=", "heur=", "astar", "bfs"])
    except getopt.GetoptError:
        # print('python sliding_puzzle.py -h <help> -n <matrix shape ex: n = 3 -> 3x3 matrix> --mx <maximum_nodes> --heur <heuristic> --astar (default algorithm) or --bfs')
        raise Exception
    for opt, arg in opts:
        if opt == '-h':
            # print('python sliding_puzzle.py -h <help> -n <matrix shape ex: n = 3 -> 3x3 matrix> --mx <maximum_nodes> --heur <heuristic> --astar (default algorithm) or --bfs')
            sys.exit()
        elif opt == '-n':
            n = int(arg)
        elif opt in ("--mx"):
            max_iter = int(arg)
        elif opt in ("--heur"):
            if arg == "manhattan" or arg == "misplaced_tiles":
                heuristic = (arg)
        elif opt in ("--astar"):
            algorithm = "a_star"
        elif opt in ("--bfs"):
            algorithm = "bfs"

    while True:
        try:
            # init_state = input("Enter a list of " + str(n * n) + " numbers representing the inital state, SEPERATED by WHITE SPACE(1 2 3 etc.): ")
            init_state = init_state.split()
            for i in range(len(init_state)):
                init_state[i] = int(init_state[i])
            # goal_state = input("Enter a list of " + str(n * n) + " numbers representing the goal state, SEPERATED by WHITE SPACE(1 2 3 etc.): ")
            goal_state = goal_state.split()
            for i in range(len(goal_state)):
                goal_state[i] = int(goal_state[i])
            if len(goal_state) == len(init_state) and len(goal_state) == n * n:
                break
            else:
                pass
                # print("Please re-enter the input again correctly")
        except Exception as ex:
            raise Exception
            # print(ex)

    init_state = np.array(init_state).reshape(n, n)
    goal_state = np.array(goal_state).reshape(n, n)

    if algorithm == "a_star":
        result = A_star(init_state, goal_state, max_iter, heuristic)
        return result
    else:
        result = BFS(init_state, goal_state, max_iter, heuristic)
        return result


if __name__ == "__main__":
    # '__name__이라는 변수의 값이 __main__이라면 아래의 코드를 실행하라.'
    main(sys.argv[1:])
