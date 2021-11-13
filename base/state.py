from abc import ABC
from typing import Hashable


class State(ABC, Hashable):
    """
    Class that contains all changeable information about problem. 
    """
