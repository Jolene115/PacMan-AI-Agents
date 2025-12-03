#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

import time
from collections import deque
from game import Directions, Actions

def q1b_solver(problem: q1b_problem):
    """
    Multi-algorithm solver that implements and compares three search algorithms:
    - Best-First Search
    - Nearest Greedy Search  
    - A* Search (with adaptive complexity handling)
    
    Uses scoring metric: score = dots_collected * 10 - path_length (+500 bonus if all dots eaten)
    Returns the path from the best performing algorithm.
    """
    
    # Initialize timing
    start_time = time.time()
    TIME_LIMIT = 9.0  # Conservative time limit
    
    # Get problem parameters
    start_state = problem.getStartState()
    start_pos, start_food = start_state
    walls = problem.walls
    food_count = len(start_food)
    
    # Adaptive time allocation based on complexity
    # Give A* less time on complex layouts to prevent timeout
    if food_count > 15:
        a_star_time = TIME_LIMIT / 6  # Reduced time for complex layouts
        other_time = TIME_LIMIT / 2.5
    else:
        a_star_time = TIME_LIMIT / 3  # Normal time for simpler layouts
        other_time = TIME_LIMIT / 3
    
    # Algorithm implementations with adaptive timing
    algorithms = [
        ("Nearest Greedy Search", nearest_greedy_search, other_time),
        ("Best-First Search", best_first_search, other_time),
        ("A* Search", a_star_search, a_star_time)
    ]
    
    results = []
    best_score = float('-inf')
    best_path = []
    
    print(f"\n=== Algorithm Comparison (Food count: {food_count}) ===")
    print(f"{'Algorithm':<20} {'Score':<8} {'Path Length':<12} {'Dots':<6} {'Time':<8}")
    print("-" * 60)
    
    # Test each algorithm
    for algo_name, algo_func, algo_time_limit in algorithms:
        if time.time() - start_time > TIME_LIMIT * 0.85:
            print(f"{algo_name:<20} SKIPPED (time limit)")
            break
            
        algo_start = time.time()
        try:
            path = algo_func(problem, algo_time_limit)
            algo_time = time.time() - algo_start
            
            # Skip empty paths
            if not path:
                print(f"{algo_name:<20} NO PATH FOUND")
                continue
            
            # Calculate score
            score, dots_collected = calculate_score(problem, path)
            
            # Skip invalid scores
            if score == float('-inf'):
                print(f"{algo_name:<20} INVALID PATH")
                continue
            
            results.append({
                'name': algo_name,
                'path': path,
                'score': score,
                'dots': dots_collected,
                'path_length': len(path),
                'time': algo_time
            })
            
            print(f"{algo_name:<20} {score:<8.1f} {len(path):<12} {dots_collected:<6} {algo_time:<8.3f}s")
            
            # Track best result
            if score > best_score:
                best_score = score
                best_path = path
                
        except Exception as e:
            print(f"{algo_name:<20} ERROR: {str(e)[:30]}")
            continue
    
    # Print ranking
    if results:
        print("\n=== Algorithm Ranking ===")
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        for i, result in enumerate(sorted_results, 1):
            print(f"{i}. {result['name']}: Score {result['score']:.1f}")
    
    # Fallback if no valid path found
    if not best_path:
        print("\nWARNING: No valid path found, using fallback greedy")
        best_path = fallback_greedy(problem, TIME_LIMIT - (time.time() - start_time))
    
    return best_path


def calculate_score(problem, path):
    """Calculate score using the metric: dots*10 - path_length (+500 if all eaten)"""
    if not path:
        return float('-inf'), 0
    
    # Simulate path execution
    state = problem.getStartState()
    dots_collected = 0
    
    for action in path:
        # Find the successor state for this action
        found_successor = False
        for successor_state, successor_action, cost in problem.getSuccessors(state):
            if successor_action == action:
                old_pos, old_food = state
                new_pos, new_food = successor_state
                
                # Check if a dot was collected (food set got smaller)
                if len(old_food) > len(new_food):
                    dots_collected += 1
                
                state = successor_state
                found_successor = True
                break
        
        if not found_successor:
            return float('-inf'), 0
    
    # Calculate final score
    score = dots_collected * 10 - len(path)
    
    # Bonus for eating all dots
    final_pos, final_food = state
    if len(final_food) == 0:
        score += 500
    
    return score, dots_collected


def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def admissible_heuristic(state):
    """
    Admissible heuristic for A* search.
    Returns minimum Manhattan distance to nearest food.
    This is always <= actual cost, making it admissible.
    """
    pos, food_set = state
    
    if not food_set:
        return 0
    
    # Just distance to nearest food - guaranteed admissible
    return min(manhattan_distance(pos, food_pos) for food_pos in food_set)


def mst_heuristic(state):
    """
    More informed but still admissible heuristic using MST approximation.
    Returns distance to nearest food + MST of remaining foods.
    """
    pos, food_set = state
    
    if not food_set:
        return 0
    
    if len(food_set) == 1:
        return manhattan_distance(pos, next(iter(food_set)))
    
    # Distance to nearest food
    min_dist = min(manhattan_distance(pos, food) for food in food_set)
    
    # For complex layouts, just use simple heuristic to avoid computation overhead
    if len(food_set) > 10:
        return min_dist
    
    # Approximate MST using nearest neighbor (still admissible as it underestimates)
    food_list = list(food_set)
    mst_cost = 0
    visited = set()
    current = food_list[0]
    visited.add(current)
    
    while len(visited) < len(food_list):
        nearest = None
        nearest_dist = float('inf')
        for food in food_list:
            if food not in visited:
                dist = manhattan_distance(current, food)
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest = food
        if nearest:
            mst_cost += nearest_dist
            visited.add(nearest)
            current = nearest
    
    # Divide by 2 to ensure admissibility (we're double counting in worst case)
    return min_dist + mst_cost // 2


def best_first_search(problem, time_limit):
    """
    Best-First Search implementation using scoring heuristic.
    Prioritizes states with highest potential score.
    """
    start_time = time.time()
    frontier = util.PriorityQueue()
    visited = set()
    
    start_state = problem.getStartState()
    frontier.push((start_state, []), 0)
    
    best_score = float('-inf')
    best_path = []
    nodes_expanded = 0
    max_nodes = 5000  # Limit for complex layouts
    
    while not frontier.isEmpty() and nodes_expanded < max_nodes:
        if time.time() - start_time > time_limit:
            break
            
        state, path = frontier.pop()
        nodes_expanded += 1
        
        # Convert state to hashable form for visited set
        pos, food_set = state
        state_key = (pos, food_set)
        
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Check if goal reached
        if problem.isGoalState(state):
            return path
        
        # Calculate current score for this state
        current_score, dots = calculate_score(problem, path)
        if current_score > best_score and current_score != float('-inf'):
            best_score = current_score
            best_path = path
        
        # Expand successors
        for successor_state, action, cost in problem.getSuccessors(state):
            new_path = path + [action]
            
            # Priority based on potential score
            s_pos, s_food = successor_state
            # Heuristic: reward food collection, penalize distance
            food_collected = len(start_state[1]) - len(s_food)
            priority = -(food_collected * 10 - len(new_path))
            
            frontier.push((successor_state, new_path), priority)
    
    return best_path


def nearest_greedy_search(problem, time_limit):
    """
    Greedy search that always goes to the nearest food.
    Uses BFS to find shortest path to nearest food.
    """
    start_time = time.time()
    state = problem.getStartState()
    path = []
    
    while not problem.isGoalState(state) and time.time() - start_time < time_limit:
        pos, food_set = state
        
        if not food_set:
            break
        
        # Find nearest food using Manhattan distance
        nearest_food = min(food_set, key=lambda f: manhattan_distance(pos, f))
        
        # BFS to nearest food
        food_path = bfs_to_food(problem, state, nearest_food, time_limit - (time.time() - start_time))
        
        if not food_path:
            # If can't reach target, try any reachable food
            for food in sorted(food_set, key=lambda f: manhattan_distance(pos, f)):
                food_path = bfs_to_food(problem, state, food, time_limit - (time.time() - start_time))
                if food_path:
                    break
        
        if not food_path:
            break
        
        # Execute path to food
        path.extend(food_path)
        
        # Update state by simulating the path
        for action in food_path:
            for successor_state, successor_action, cost in problem.getSuccessors(state):
                if successor_action == action:
                    state = successor_state
                    break
    
    return path


def a_star_search(problem, time_limit):
    """
    A* Search implementation with admissible heuristic.
    Uses g(n) + h(n) where g(n) is path cost and h(n) is admissible heuristic.
    """
    start_time = time.time()
    frontier = util.PriorityQueue()
    visited = {}  # state_key -> best_g_cost
    
    start_state = problem.getStartState()
    pos, food_set = start_state
    
    # Choose heuristic based on complexity
    if len(food_set) > 8:
        heuristic = admissible_heuristic  # Simple for complex layouts
    else:
        heuristic = mst_heuristic  # More informed for simpler layouts
    
    frontier.push((start_state, [], 0), heuristic(start_state))
    
    nodes_expanded = 0
    max_nodes = 3000 if len(food_set) > 15 else 10000
    
    while not frontier.isEmpty() and nodes_expanded < max_nodes:
        if time.time() - start_time > time_limit:
            break
            
        state, path, g_cost = frontier.pop()
        nodes_expanded += 1
        
        # Create hashable state key
        pos, food_set = state
        state_key = (pos, food_set)
        
        # Skip if we've seen this state with better or equal cost
        if state_key in visited and visited[state_key] <= g_cost:
            continue
        visited[state_key] = g_cost
        
        # Check goal
        if problem.isGoalState(state):
            return path
        
        # Early termination for complex layouts if taking too long
        if len(food_set) > 15 and time.time() - start_time > time_limit * 0.7:
            break
        
        # Expand successors
        for successor_state, action, step_cost in problem.getSuccessors(state):
            new_path = path + [action]
            new_g_cost = g_cost + step_cost
            
            # Skip if we've seen this successor with better cost
            s_pos, s_food = successor_state
            s_key = (s_pos, s_food)
            if s_key in visited and visited[s_key] <= new_g_cost:
                continue
            
            # Calculate f(n) = g(n) + h(n)
            h_cost = heuristic(successor_state)
            f_cost = new_g_cost + h_cost
            
            frontier.push((successor_state, new_path, new_g_cost), f_cost)
    
    # Return empty if no solution found within constraints
    return []


def bfs_to_food(problem, start_state, target_food, time_limit):
    """
    BFS to find shortest path from current state to target food.
    Returns list of actions.
    """
    start_time = time.time()
    queue = deque([(start_state, [])])
    visited = set()
    
    while queue and time.time() - start_time < time_limit:
        state, path = queue.popleft()
        pos, food_set = state
        
        # Create hashable state key
        state_key = (pos, food_set)
        if state_key in visited:
            continue
        visited.add(state_key)
        
        # Check if we reached the target food
        if pos == target_food:
            return path
        
        # Expand successors
        for successor_state, action, cost in problem.getSuccessors(state):
            new_path = path + [action]
            queue.append((successor_state, new_path))
    
    return []


def fallback_greedy(problem, time_limit):
    """
    Simple fallback that just tries to collect any reachable food.
    Used when all other algorithms fail.
    """
    start_time = time.time()
    state = problem.getStartState()
    path = []
    
    while time.time() - start_time < time_limit:
        pos, food_set = state
        if not food_set:
            break
        
        # Try to move towards any food
        best_action = None
        best_distance = float('inf')
        
        for successor_state, action, cost in problem.getSuccessors(state):
            s_pos, s_food = successor_state
            if s_food != food_set:  # Found food
                return path + [action]
            
            # Move towards nearest food
            if food_set:
                min_dist = min(manhattan_distance(s_pos, f) for f in food_set)
                if min_dist < best_distance:
                    best_distance = min_dist
                    best_action = action
        
        if best_action:
            path.append(best_action)
            # Update state
            for successor_state, action, cost in problem.getSuccessors(state):
                if action == best_action:
                    state = successor_state
                    break
        else:
            break
    
    return path
