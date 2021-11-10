# State Space Search Laboratory

## TODO: 

Fill missing code according to the `TODO:` comments in the following files:
- `solvers/generic/uninformed.py`
- `solvers/generic/best_first.py`
- `solvers/iddfs.py`
- `solvers/idastar.py`
- `problems/grid_pathfinding/heuristics/euclidean_heuristic.py`
- `problems/grid_pathfinding/heuristics/manhattan_heuristic.py`
- `problems/grid_pathfinding/heuristics/diagonal_heuristic.py`
- `problems/n_puzzle/heuristics/n_puzzle_tiles_out_of_place_heuristic.py`
- `problems/n_puzzle/heuristics/n_puzzle_manhattan_heuristic.py`
- `problems/blocks_world/blocks_world_heuristic.py`
- `problems/blocks_world/blocks_world_problem.py`
- `problems/blocks_world/blocks_world_action.py`

### Useful links:

- [interactive pathfinding on grids](http://krzysztof.kutt.pl/didactics/psi/pathfinder/)
- [definitions of various grid heuristics](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#heuristics-for-grid-maps)
- [nice blog post about A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [elegant n-puzzle visualization](http://krzysztof.kutt.pl/didactics/psi/npuzzles/)

## Grading

* [ ] Make sure, you have a **private** group
  * [how to create a group](https://docs.gitlab.com/ee/user/group/#create-a-group)
* [ ] Fork this project into your private group
  * [how to create a fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#creating-a-fork)
* [ ] Add @bobot-is-a-bot as the new project's member (role: **maintainer**)
  * [how to add an user](https://docs.gitlab.com/ee/user/project/members/index.html#add-a-user)

## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Solve the exercises
    * use MiniZincIDE, whatever
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to the gitlab master branch
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
- `python solve.py -p rush_hour -a astar -h rush_hour_indirect problems/rush_hour/instances/81.txt` (every problem has several instances in the `instances` directory)

You can also run a benchmark:
- `python benchmark.py -p <problem> -t timeout <path_to_instance>`, e.g.
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
