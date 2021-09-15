
#TODO: Znaleźć sposób jak ładnie wrzucać tutaj odpowiednie klasy. Uogólniamy jak się da
#TODO: Typowanie

"""
Do wizualizacji np. drzew proponuje wykorzystać bibliotekę `pydot`
"""

class Solver(object):
    def __init__(self, *args):
        self.graph = {}
        self.start = dict() # State
        self.goal = None    # State
    
    def __str__(self) -> str:
        pass

    def solve(self, root_state, goal_state):
        pass
