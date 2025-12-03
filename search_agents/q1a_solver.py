#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def _reconstruct_path(came_from, goal):
    actions = []
    node = goal
    while node in came_from:
        parent, action = came_from[node]
        actions.append(action)
        node = parent
    actions.reverse()
    return actions


def q1a_solver(problem: q1a_problem):
    start = problem.getStartState()
    goal = problem.goal

    frontier = util.PriorityQueue()  # holds only states (positions)
    g_cost = {start: 0}
    came_from = {}

    frontier.push(start, astar_heuristic(start, goal))

    while not frontier.isEmpty():
        state = frontier.pop()

        # Goal check on pop (A* optimality)
        if problem.isGoalState(state):
            return _reconstruct_path(came_from, state)

        current_g = g_cost.get(state)
        if current_g is None:
            # Outdated pop (defensive), skip
            continue

        for next_state, action, step_cost in problem.getSuccessors(state):
            tentative_g = current_g + step_cost
            if tentative_g < g_cost.get(next_state, float('inf')):
                g_cost[next_state] = tentative_g
                came_from[next_state] = (state, action)
                f = tentative_g + astar_heuristic(next_state, goal)
                frontier.push(next_state, f)

    return []  # No path found


def astar_heuristic(current, goal):
    # Manhattan distance on 4-connected grid (admissible and consistent)
    if goal is None or current is None:
        return 0
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
