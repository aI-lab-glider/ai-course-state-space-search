from typing import Optional, Tuple
from PIL import Image, ImageDraw

class GridDrawer:
    def __init__(self, image: Image.Image, grid):
        self.image = image
        self.grid = grid
        self.draw = ImageDraw.Draw(self.image)

    def calculate_cell_params(self):
        cell = int(self.image.width / self.grid.shape[0]), int(self.image.height / self.grid.shape[1])
        cell_side = min(cell)
        border = int(cell_side / 10)
        return cell_side, cell_side, border


    def draw_grid(self):
        cell_width, cell_height, _ = self.calculate_cell_params()
        draw = ImageDraw.Draw(self.image)
        for x in range(0, self.image.width, cell_width):
            line = ((x, 0), (x, self.image.height))
            draw.line(line, fill="black")

        for y in range(0, self.image.height, cell_height):
            line = ((0, y), (self.image.width, y))
            draw.line(line, fill="black")
 
    def get_cell_coords(self, x: int, y: int, x_end: Optional[int] = None, y_end: Optional[int] = None):
            cell_width, cell_height, border = self.calculate_cell_params()
            x_start = x * cell_width + border
            x_end = (x_end or (x + 1)) * cell_width - border
            y_start = y * cell_height + border
            y_end = (y_end or (y + 1)) * cell_width - border
            return (x_start, y_start, x_end, y_end)

    def draw_rectangle(self, grid_coords: Tuple[int, ...], fill: Optional[Tuple[int, int, int]]=None):
        coords = self.get_cell_coords(*grid_coords)
        self.draw.rectangle(coords, fill)

    def draw_circle(self, grid_x: int, grid_y: int, fill: Optional[Tuple[int, int, int]]=None):
        coords = self.get_cell_coords(grid_x, grid_y)
        self.draw.ellipse(coords, fill)

