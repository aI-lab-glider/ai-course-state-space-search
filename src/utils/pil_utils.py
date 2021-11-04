from typing import Optional, Tuple
from PIL import Image, ImageDraw

class GridDrawer:
    def __init__(self, image: Image.Image, grid):
        self.image = image
        self.grid = grid
        self.draw = ImageDraw.Draw(self.image)
        self.cell_width, self.cell_height, self.border = self.calculate_cell_params()

    def calculate_cell_params(self):
        cell = int(self.image.width / self.grid.shape[0]), int(self.image.height / self.grid.shape[1])
        cell_side = min(cell)
        border = int(cell_side / 10)
        return cell_side, cell_side, border


    def draw_grid(self):
        draw = ImageDraw.Draw(self.image)
        for x in range(0, self.image.width, self.cell_width):
            line = ((x, 0), (x, self.image.height))
            draw.line(line, fill="black")

        for y in range(0, self.image.height, self.cell_height):
            line = ((0, y), (self.image.width, y))
            draw.line(line, fill="black")
 
    def get_cell_coords(self, x: int, y: int, grid_x_end: Optional[int] = None, grid_y_end: Optional[int] = None, padding = 0):
            x_start = x * self.cell_width + self.border + padding
            x_end = (grid_x_end or (x + 1)) * self.cell_width - self.border - padding
            y_start = y * self.cell_height + self.border + padding
            y_end = (grid_y_end or (y + 1)) * self.cell_width - self.border - padding
            return (x_start, y_start, x_end, y_end)

    def draw_rectangle(self, grid_coords: Tuple[int, ...], fill: Optional[Tuple[int, int, int]]=None, padding=0):
        coords = self.get_cell_coords(*grid_coords, padding=padding)
        self.draw.rectangle(coords, fill)

    def draw_circle(self, grid_x: int, grid_y: int, fill: Optional[Tuple[int, int, int]]=None):
        coords = self.get_cell_coords(grid_x, grid_y)
        self.draw.ellipse(coords, fill)

