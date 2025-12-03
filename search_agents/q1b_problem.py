# problems/q1b_problem.py
import logging
from typing import List, Tuple, FrozenSet

import util
from game import Actions, Directions
from logs.search_logger import log_function
from pacman import GameState


Position = Tuple[int, int]


class q1b_problem:
    """
    Multi-food search problem.
    State = (pacman_position, remaining_food_set)
    """

    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        self.startingGameState: GameState = gameState
        self.walls = gameState.getWalls()
        self.width, self.height = self.walls.width, self.walls.height

        # Remaining food as an immutable set of coordinates for hashing
        food_list: List[Position] = gameState.getFood().asList()
        self.start_food: FrozenSet[Position] = frozenset(food_list)

    @log_function
    def getStartState(self):
        pacman_pos: Position = self.startingGameState.getPacmanPosition()
        return pacman_pos, self.start_food

    @log_function
    def isGoalState(self, state):
        _, remaining = state
        return len(remaining) == 0

    @log_function
    def getSuccessors(self, state):
        successors = []
        (x, y), remaining = state

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(action)
            nx, ny = int(x + dx), int(y + dy)

            # explicit bounds + wall check
            if 0 <= nx < self.width and 0 <= ny < self.height and not self.walls[nx][ny]:
                next_pos = (nx, ny)

                # consume food if present at the next cell
                if next_pos in remaining:
                    next_remaining = frozenset(p for p in remaining if p != next_pos)
                else:
                    next_remaining = remaining

                successors.append(((next_pos, next_remaining), action, 1))

        return successors
