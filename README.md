# Ai-search-solv

### Directory layout
    .
    ├── src
    │   ├── base
    │   │   ├── problem.py
    │   │   └── state.py
    │   ├── problems                    # List of defined problems (place to define problems)
    │   │   ├── ...
    │   │   ├── n_puzzle_problem.py
    │   │   └── ...
    │   ├── solvers                     # All solvers here
    │   ├── tree
    │   ├── conftest.py                 # Must be here cuz' other way pytest is not working. See Ad.1 :)
    │   └── main.py
    ├── tests                           # Tests, scoring system
    ├── .gitignore
    ├── README.md
    └── requirements.txt

### Usage
```bash
    echo "Insert tutos here later"
```

### Credits and used links for inspirations

1. https://github.com/Bishalsarang/8-Puzzle-Problem
1. https://medium.com/code-science/sudoku-solver-graph-coloring-8f1b4df47072

### AD

1. Read about `conftest` solution on  [StackOverflow](https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada)