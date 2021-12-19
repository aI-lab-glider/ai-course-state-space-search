import base64
from io import BytesIO
from solve import SolvingMonitor
from typing import Union
from base.solver import Solver

from pathlib import Path
import networkx as nx
from bokeh.io import output_file, show, save
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool, WheelZoomTool, PanTool, GraphRenderer, ColumnDataSource,
                          Image)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx, Figure, figure

from tree import Node
from tree.tree import NodeEvent
from networkx.drawing.nx_agraph import write_dot, graphviz_layout


MAX_WIDTH = 1400
HEIGHT = 700
SAME_CLUB_COLOR, DIFFERENT_CLUB_COLOR = "darkgrey", "red"

class Visualization(SolvingMonitor):
    def __init__(self, solver: Solver, instance: Union[str, Path]):
        super().__init__(solver, instance)
        self.N = 0
        self.nodes = {}
        self.y = []
        self.x = []
        self.imgs = []
        self.G = nx.Graph()
        self.plot = figure(width=1300, height=600,x_range=(-10000, 10000),
                      y_range=(-10000, 10000), tooltips=self.set_tooltips())

        #self.plot.axis.visible = False
        # self.plot.grid.visible = False
        # self.plot.background_fill_color = None
        # self.plot.border_fill_color = None
        # self.plot.outline_line_color = None
    def show_results(self):
        self.plot.title.text = "Tree visualization"
        #self.add_tools()
        show(self.plot)

    def add_tools(self):
        node_hover_tool = HoverTool(tooltips=[("index", "($x, $y)"),("(x,y)", "($x, $y)")])

        self.plot.add_tools(PanTool(),WheelZoomTool(),BoxZoomTool(), ResetTool(), node_hover_tool)

    def update_graph(self,node):
        self.plot = figure(width=1300, height=600,x_range=(-10000, 10000),
                      y_range=(-10000, 10000), tooltips=self.set_tooltips())
        self.G.add_node(self.N)
        self.nodes[node] = self.N

        if self.N == 0:
            layout = self.hierarchy_pos(self.G, 0, x_range=(-50000, 100000), y_range=(-100000, 100000))
            self.x.append(layout[self.N][0])
            self.y.append(layout[self.N][1])

            buffered = BytesIO()
            image = self.solver.problem.to_image(node.state)
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            self.imgs.append(f"data:image/png;base64,{img_str.decode('utf-8')}")
            self.N += 1
            return

        self.G.add_edge(self.N, self.nodes[node.parent])
        layout = self.hierarchy_pos(self.G,0,x_range=(-50000, 100000),y_range=(-100000, 100000))
        self.x.append(layout[self.N][0])
        self.y.append(layout[self.N][1])

        buffered = BytesIO()
        image = self.solver.problem.to_image(node.state)
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        self.imgs.append(f"data:image/png;base64,{img_str.decode('utf-8')}")


        self.graph_renderer = from_networkx(self.G, layout, scale=1, center=layout[0])
        self.graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
        self.plot.add_glyph(self.update_nodes(node,self.x,self.y,self.imgs),self.graph_renderer.node_renderer.glyph)
        self.plot.renderers.append(self.graph_renderer)
        self.N += 1


    def got_event(self, node: Node, event: NodeEvent) -> None:
        # if event == NodeEvent.Opened:
            self.update_graph(node)
            save(self.plot)
            self.solver.problem.to_image(node.state)


    def hierarchy_pos(self,G, root, levels=None, x_range=(0,1), y_range=(0,1)):
        '''If there is a cycle that is reachable from root, then this will see infinite recursion.
           G: the graph
           root: the root node
           levels: a dictionary
                   key: level number (starting from 0)
                   value: number of nodes in this level
           width: horizontal space allocated for drawing
           height: vertical space allocated for drawing'''
        TOTAL = "total"
        CURRENT = "current"

        def make_levels(levels, node=root, currentLevel=0, parent=None):
            """Compute the number of nodes for each level
            """
            if not currentLevel in levels:
                levels[currentLevel] = {TOTAL: 0, CURRENT: 0}
            levels[currentLevel][TOTAL] += 1
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    levels = make_levels(levels, neighbor, currentLevel + 1, node)
            return levels

        def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):

            dx = 1 / levels[currentLevel][TOTAL]
            left = dx / 2
            pos[node] = ((left + dx * levels[currentLevel][CURRENT]) * x_range[1]+x_range[0], vert_loc)
            levels[currentLevel][CURRENT] += 1
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc - vert_gap)
            return pos

        if levels is None:
            levels = make_levels({})
        else:
            levels = {l: {TOTAL: levels[l], CURRENT: 0} for l in levels}
        vert_gap = (y_range[1]-y_range[0])/ (max([l for l in levels]) + 1)
        return make_pos({})

    def update_nodes(self,node,x,y,imgs):
        source = ColumnDataSource(data=dict(
            x=x,
            y=y,
            imgs=imgs,
            fonts=[
                '<i>italics</i>'
            ]*self.N
        ))
        return source

    def set_tooltips(self):
        TOOLTIPS = """
            <div>
                <div>
                    <img
                        src="@imgs" height="42" alt="@imgs" width="42"
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
        return TOOLTIPS