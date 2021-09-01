import queue
import collections

import Node as nd
from queue import Queue


class Board:
    def __init__(self, x_len, y_len):
        self.matrix = [[nd.Node(x, y) for y in range(y_len)] for x in range(x_len)]
        self.width = x_len
        self.height = y_len

        self.x_start = None
        self.y_start = None
        self.x_finish = None
        self.y_finish = None

        self.data = collections.defaultdict(list)
        self.data['size'].append((x_len, y_len))


    def place_wall(self, x, y):  # places a wall in a given place
        self.matrix[x][y].type = nd.Type.WALL
        self.data['walls'].append((x, y))

    def place_start(self, x, y):
        self.x_start = x
        self.y_start = y
        self.data['start'].append((x, y))


    def place_finish(self, x, y):
        self.x_finish = x
        self.y_finish = y
        self.data['finish'].append((x, y))


    def get_next(self, x, y):  # return nodes that might be visited in next step
        next_nodes = []
        for i, j in [[1,0],[0,1],[-1,0],[0,-1]]:
            # I can do that because python checks 'if' statements from left to right, so the coordinates must be valid
            if self.valid_coordinates(x + i, y + j):
                if self.matrix[x + i][y + j].color == nd.Color.WHITE and self.matrix[x + i][y + j].type == nd.Type.NODE:
                    next_nodes.append((x + i, y + j))

        return next_nodes

    def valid_coordinates(self, x, y):  # checks if coordinates are being placed within boarders
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            return True
        return False

    def print_path(self, node):
        if node is None:
            return
        self.data['path'].append((node.x, node.y))
        self.print_path(node.parent)
    
    def BFS(self):
        self.matrix[self.x_start][self.y_start].color = nd.Color.GREY
        self.matrix[self.x_start][self.y_start].d = 0
        self.matrix[self.x_start][self.y_start].parent = None

        q = queue.Queue()
        q.put((self.x_start, self.y_start))
        while q.empty() is False:
            u_x, u_y = q.get()
            u_neighbors_coordinates = self.get_next(u_x, u_y)
            for v_x, v_y in u_neighbors_coordinates:
                if self.matrix[v_x][v_y].color == nd.Color.WHITE:
                    self.matrix[v_x][v_y].color = nd.Color.GREY
                    self.matrix[v_x][v_y].d = self.matrix[u_x][u_y].d + 1
                    self.matrix[v_x][v_y].parent = self.matrix[u_x][u_y]
                    q.put((v_x, v_y))
            self.matrix[u_x][u_y].color = nd.Color.BLACK

