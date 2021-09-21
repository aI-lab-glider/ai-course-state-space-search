from base import Problem 
from problems.route_finding.location import Location
from typing import Sequence, Tuple, Generator, Union
from collections import defaultdict


adj_list = Sequence[Tuple[Location, Location, int]]


class RouteFinding(Problem):
    def __init__(self, locations: Sequence[Location], routes: adj_list, initial: Location, goal: Location):
        super().__init__(initial, goal)
        self.locations = {loc.id: loc for loc in locations}
        self.routes = defaultdict(lambda: dict())
        self.add_routes(routes)


    def add_routes(self, routes: adj_list):
        for source, target, dist in routes:
            assert source in self.locations, f"unknown location {source}"
            assert target in self.locations, f"unknown location {target}"
            assert dist >= 0, f"Distance between {source} and {target} must be postive"
            self.routes[source][target] = dist
            self.routes[target][source] = dist


    def actions(self, location: Location) -> Generator[Location, None, None]:
        for neighbour in self.routes[location]:
            yield neighbour.id


    # TODO: What should be done if unspported action is passed? For now method will raise exception
    def transition_model(self, location: Location, action: Union[str, int]) -> Location:
        assert location in self.locations, f"Unknown location {location}"
        assert action in self.routes[location], f"Cannot take given action {action} from {location}"
        target = self.locations[action]
        return target


    def action_cost(self, source: Location, action: Union[str, int], target: Location) -> int:
        return self.routes[source][target]


    def is_goal(self, location: Location) -> bool:
        return self.goal == location

