import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState

class q1a_problem:
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        gameState: A GameState object (pacman.py)

        Store anything else that you think would helpful for your agent
        """
        self.startingGameState: GameState = gameState
        self.food = gameState.getFood()
        self.walls = gameState.getWalls()

        food_list = self.food.asList()
        if len(food_list) != 1:
            raise ValueError(f"q1a expects exactly one dot, found {len(food_list)}.")
        self.goal: Tuple[int, int] = food_list[0]

    @log_function
    def getStartState(self) -> Tuple[int, int]:
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return self.startingGameState.getPacmanPosition()

    @log_function
    def isGoalState(self, state: Tuple[int, int]) -> bool:
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        return state == self.goal

    @log_function
    def getSuccessors(self, state: Tuple[int, int]):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        # ------------------------------------------
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        successors = []
        x, y = state
        width, height = self.walls.width, self.walls.height

        # Check all possible actions (up, down, left, right)
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            # Check if the next position is not a wall
            if 0 <= nextx < width and 0 <= nexty < height and not self.walls[nextx][nexty]:
                successors.append(((nextx, nexty), action, 1))
        return successors




