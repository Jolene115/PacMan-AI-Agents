# Pacman AI Agents – Search & Multi‑Agent Decision Making

Implemented AI agents for the Pacman game using classical search and multi‑agent adversarial decision making in Python.

The project showcases graph search algorithms (BFS, DFS, Uniform‑Cost Search, A*), adversarial search (minimax, alpha‑beta pruning, expectimax), and a hand‑crafted evaluation function that balances reward and risk in a dynamic game environment.

---

### Project Overview

This repository contains my implementations of:

- **Search agents** for solving a variety of Pacman maze problems.
- **Multi‑agent agents** that plan against adversarial ghosts.
- An **advanced evaluation function** that significantly improves Pacman’s performance compared to simple baseline agents.

The Pacman game framework (game engine, layouts and visualisation) is based on the classic Pacman AI project commonly used in teaching.  
All **agent logic, search algorithms and evaluation functions in `search_agents/` and `multiagent_agents/` were implemented by me**.

---

### Key Features

- **Classical Search (Search Agents)**
  - Implemented **BFS, DFS, Uniform‑Cost Search, and A\*** for grid‑based pathfinding.
  - Designed **admissible and consistent heuristics** to speed up A\* without losing optimality.
  - Applied these algorithms to different Pacman problem formulations (food collection, maze navigation, etc.).

- **Multi‑Agent Decision Making**
  - Implemented **minimax**, **alpha‑beta pruning**, and **expectimax** agents to control Pacman in adversarial settings against ghost agents.
  - Modelled ghosts as either adversarial or stochastic, and adapted the decision algorithm accordingly.
  - Tuned search depth and pruning to balance decision quality with computational cost.

- **Highlight: Advanced Evaluation Function (Most Challenging Part)**
  - Designed and tuned an **evaluation function** for multi‑agent Pacman that:
    - Considers distances to **food**, **ghosts**, and **capsules**.
    - Uses **ghost scared timers** to decide when to chase ghosts vs avoid them.
    - Penalises **dead‑ends** and **trap‑like states** to reduce the risk of being cornered.
    - Balances **immediate reward** (eating food, scoring points) with **long‑term survival**.
  - This evaluation function led to **higher average scores and win rates** compared to baseline reflex agents.

---

### How to Run

Install Python 3, then (optionally) create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt#### Run Search Agents (BFS / DFS / UCS / A*)

### Example commands – adjust agent/function names to match your code
python pacman_core/pacman.py -l smallClassic -p SearchAgent -a fn=depthFirstSearch
python pacman_core/pacman.py -l smallClassic -p SearchAgent -a fn=breadthFirstSearch
python pacman_core/pacman.py -l mediumClassic -p SearchAgent -a fn=uniformCostSearch
python pacman_core/pacman.py -l mediumClassic -p SearchAgent -a fn=aStarSearch,heuristic=manhattanHeuristic#### Run Multi‑Agent Agents (Minimax / Alpha‑Beta / Expectimax)

### Replace agent names with the ones defined in your multiAgents.py
python pacman_core/pacman.py -l mediumClassic -p MinimaxAgent -a depth=2
python pacman_core/pacman.py -l mediumClassic -p AlphaBetaAgent -a depth=3
python pacman_core/pacman.py -l mediumClassic -p ExpectimaxAgent -a depth=2#### Run Advanced Evaluation Agent (Your Part 2 Highlight)

# Example: using your advanced evaluation function
# Replace ReflexAgent / betterEvaluationFunction if your names are different
python pacman_core/pacman.py -l mediumClassic -p ReflexAgent -a evalFn=betterEvaluationFunctionUpdate the agent class names and arguments above to match your implementation.

---

### Skills Demonstrated

- **Algorithms & AI**
  - Graph search: BFS, DFS, Uniform‑Cost Search, A\*.
  - Adversarial search: minimax, alpha‑beta pruning, expectimax.
  - Heuristic and evaluation function design in a multi‑agent environment.

- **Programming**
  - Python, object‑oriented design, debugging and profiling search code.
  - Working with a non‑trivial existing codebase and integrating new components.

- **Reasoning**
  - Modelling complex game states and rewards.
  - Balancing short‑term vs long‑term objectives and risk vs reward.

---

### Attribution

The Pacman game framework (engine, layouts and graphics) is adapted from an existing Pacman AI framework.  
All search algorithms, multi‑agent logic and evaluation functions in this repository were implemented by me.
