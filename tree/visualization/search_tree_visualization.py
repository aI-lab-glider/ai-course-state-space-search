import base64
from io import BytesIO
from pathlib import Path
from typing import Union

import networkx as nx
from bokeh.core.validation import silence
from bokeh.core.validation.warnings import MISSING_RENDERERS
from bokeh.io import show
from bokeh.models import (Circle)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, figure

from base.solver import Solver
from solve import SolvingMonitor
from tree import Node
from tree.tree import NodeEvent

silence(MISSING_RENDERERS, True)


class Visualization(SolvingMonitor):
    def __init__(self, solver: Solver, instance: Union[str, Path]):
        super().__init__(solver, instance)
        self.N = 0
        self.nodes = {}
        self.y = []
        self.x = []
        self.imgs = []
        self.G = nx.Graph()
        self.plot = figure(width=1300, height=600, x_range=(-10000, 10000),
                           y_range=(-10000, 10000), tooltips=self.set_tooltips())
        self.plot.title.text = "Tree visualization"

    def show_results(self):
        layout = self.hierarchy_pos(self.G, 0, x_range=(-50000, 100000), y_range=(-100000, 100000))
        graph_renderer = from_networkx(self.G, layout, scale=1, center=layout[0])
        graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
        graph_renderer.node_renderer.data_source.add(['<i>italics</i>'] * self.N, 'fonts')
        graph_renderer.node_renderer.data_source.add(self.imgs, 'imgs')
        self.plot.renderers.append(graph_renderer)
        show(self.plot)

    def update_graph(self, node):
        self.G.add_node(self.N)
        self.nodes[node] = self.N

        if self.N != 0:
            self.G.add_edge(self.N, self.nodes[node.parent])
        layout = self.hierarchy_pos(self.G, 0, x_range=(-50000, 100000), y_range=(-100000, 100000))
        self.x.append(layout[self.N][0])
        self.y.append(layout[self.N][1])

        buffered = BytesIO()
        image = self.solver.problem.to_image(node.state)
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        self.imgs.append(f"data:image/png;base64,{img_str.decode('utf-8')}")
        self.N += 1

    def got_event(self, node: Node, event: NodeEvent) -> None:
        if event == NodeEvent.Opened or self.N == 0:
            self.update_graph(node)

    def hierarchy_pos(self, G, root, levels=None, x_range=(0, 1), y_range=(0, 1)):
        """If there is a cycle that is reachable from root, then this will see infinite recursion.
           G: the graph
           root: the root node
           levels: a dictionary
                   key: level number (starting from 0)
                   value: number of nodes in this level
           width: horizontal space allocated for drawing
           height: vertical space allocated for drawing"""
        TOTAL = "total"
        CURRENT = "current"

        def make_levels(levels, node=root, current_level=0, parent=None):
            """Compute the number of nodes for each level
            """
            if current_level not in levels:
                levels[current_level] = {TOTAL: 0, CURRENT: 0}
            levels[current_level][TOTAL] += 1
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    levels = make_levels(levels, neighbor, current_level + 1, node)
            return levels

        def make_pos(pos, node=root, current_level=0, parent=None, vert_loc=0):

            dx = 1 / levels[current_level][TOTAL]
            left = dx / 2
            pos[node] = ((left + dx * levels[current_level][CURRENT]) * x_range[1] + x_range[0], vert_loc)
            levels[current_level][CURRENT] += 1
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    pos = make_pos(pos, neighbor, current_level + 1, node, vert_loc - vert_gap)
            return pos

        if levels is None:
            levels = make_levels({})
        else:
            levels = {l: {TOTAL: levels[l], CURRENT: 0} for l in levels}
        vert_gap = (y_range[1] - y_range[0]) / (max([l for l in levels]) + 1)
        return make_pos({})

    def set_tooltips(self):
        return """
            <div>
                <div>
                    <img
                        src="@imgs" height="300" alt="@imgs" width="300"
                        style="float: left; margin: 0px 15px 15px 0px;"
                        border="2"
                    ></img>
                </div>
                <div>
                    <span style="font-size: 15px; color: #966;">[$index]</span>
                </div>
                <div>
                    <span>@fonts{safe}</span>
                </div>
                <div>
                    <span style="font-size: 15px;">Location</span>
                    <span style="font-size: 10px; color: #696;">($x, $y)</span>
                </div>
            </div>
        """