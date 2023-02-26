# Lab 01 - state space search

State search 🔍 is a problem-solving method in AI and computer science 💻. It involves exploring a space of possible states to find a sequence of actions required to solve a problem 🤔. State search algorithms can be categorized into uninformed and informed search algorithms 🧐. Examples of state search algorithms include depth-first search 🕳️, breadth-first search 🌳, A* search ⭐, NBA* search 🏀, and others 🤔. Concepts introduced in state search have practical applications in game playing 🎮, robotics 🤖, logistics and supply chain management 🚛, automated planning 📆, and others 🤖💡. Understanding state search algorithms is essential for developing intelligent systems that can solve complex problems 🤖💡.

# TODO: 

Search for `TODO` text in the repository with CTRL+F and replace it with you code written according to it.


## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Complete TODOS the exercises
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to your repository main branch
    ```bash
    git push -u origin master
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file

## How To Run

This class requires Python with version at least 3.8.
Recommended way to run is to create a virtual environment first:
 
- `python -m venv state-search`
- `source state-search/bin/activate`

Then install required packages:
- `pip install -r requirements.txt`

Finally you can run a solver:
- `python solve.py -a <algorithm> -p <problem> -h <heuristic> <path_to_instance>`, e.g.

Where `<algorithm>` is one of:

```
- dfsrecursive
- dfsiter
- bfs
- dijkstra
- greedy
- astar
- nbastar
```

the `<heuristic>` depends on the selected `<problem>` and can be one of the following (select one from listed in `{}`):

```
- grid_path_finding: { grid_euclidean, grid_diagonal, grid_manhattan }
- n_puzzle: { n_puzzle_tiles_out_of_place, n_puzzle_manhattan }
- rush_hour: { rush_hour_distance_to_exit, rush_hour_blocking_cars, rush_hour_indirect }
- blocks_world: { blocks_world_naive }
- pancake: { pancake_gap, pancake_largest_pancake }

```


the `<problem>` is one of:

```
- grid_path_finding
- n_puzzle
- rush_hour
- blocks_world
- pancake
```

and `instance` is one of the files placed in `<problem>/instances` directory (see project structure below for example).

Example:

- `python solve.py -p rush_hour -a astar -h rush_hour_indirect problems/rush_hour/instances/81.txt` 



You can also run a benchmark:
- `python benchmark.py -p <problem> -t timeout <path_to_instance>`

Example: 

- `python benchmark.py -p rush_hour problems/rush_hour/instances/54.txt`

If you run script with incorrect arguments, you will get some helpful info ;)

## Project Structure

    .
    ├── base                # API for problem and solver classes
    ├── problems            # List of defined problems (place to define problems)
    │   ├── ...
    │   ├── n_puzzle        # directory with a problem
    │   │   ├── instances   # directory with problem instances
    │   │   └── ...
    │   └── ...
    ├── solvers             # directory with algorithms
    │   ├── generic         # code shared by several algorithms
    │   ├── bfs.py          # example of an algorithm
    │   └── ...
    ├── tree                # search tree representation
    ├── utils               # various utilities
    ├── solve.py            # solve tool (run as a script)
    ├── benchmark.py        # benchmark tool (run as a script)
    └── cli_config.py       # configuration of the cli tools (do not touch)




### Useful links:

- [interactive pathfinding on grids](http://krzysztof.kutt.pl/didactics/psi/pathfinder/)
- [definitions of various grid heuristics](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#heuristics-for-grid-maps)
- [nice blog post about A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [elegant n-puzzle visualization](http://krzysztof.kutt.pl/didactics/psi/npuzzles/)
- NBA* - papers explaining the algorithm: [1](https://www.researchgate.net/publication/46434387_Yet_another_bidirectional_algorithm_for_shortest_paths), [2 — requires access via AGH library/other means](https://www.sciencedirect.com/science/article/abs/pii/S0377221708007613), 
