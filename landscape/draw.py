from dataclasses import dataclass
from PIL import Image, ImageDraw

from landscape.geometry import XOrderedSegment, Point

DEFAULT_DRAW_MODE = 'RGB'


class Dimensions:
    def __init__(self, width, height):
        self.width = self._get_if_valid(width)
        self.height = self._get_if_valid(height)

    def _get_if_valid(self, dimension):
        if not isinstance(dimension, int) or dimension < 0:
            raise ValueError(f'Dimension must be integer > 0, but got {dimension}')
        return dimension

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height


class LandscapeImage:
    def __init__(self, dimensions, color=None):
        self.dimensions = dimensions
        self.image = self._image(color)
        self.draw_tool = self._draw_tool(self.image)

    def _image(self, color):
        width_and_height = (self.dimensions.width, self.dimensions.height)
        return Image.new(DEFAULT_DRAW_MODE, width_and_height, color)

    def _draw_tool(self, image):
        return ImageDraw.Draw(image)

    def draw_hill(self, start, end, color, displacement_factor, 
                 roughness, iterations):
        self._check_points_in_image(start, end)
        segment = XOrderedSegment(start, end)
        segment.iterative_displacement(displacement_factor, roughness, iterations)
        self._draw_polygon(segment.points, color)

    def _check_points_in_image(self, *points):
        for point in points: 
            if not self._is_in_image(point):
                raise ValueError(f'Point {point} outside of dimensions {self.dimensions}')

    def _is_in_image(self, point):
        return (0 <= point.x <= self.dimensions.width and
                0 <= point.y <= self.dimensions.height)

    def _draw_polygon(self, points, color):
        coordinates = self._polygon_draw_coordinates(points)
        self.draw_tool.polygon(coordinates, color)

    def _polygon_draw_coordinates(self, points):
        points = self._polygon_points(points)
        return self._draw_coordinates(points) 

    def _polygon_points(self, points):
        start, end = Point(points[0].x, 0), Point(points[-1].x, 0)
        return [start, *points, end]

    def _draw_coordinates(self, points):
        return [(p.x, self.dimensions.height - p.y) for p in points]

    def save(self, filename):
        self.image.save(filename)


class BlueHills(LandscapeImage):
    def __init__(self, dimensions):
        super().__init__(dimensions, (200, 211, 220))

    def _relative_point(self, x_rel, y_rel):
        return Point(int(self.dimensions.width*x_rel), int(self.dimensions.height*y_rel))

    def render(self):
        self.draw_hill(self._relative_point(0, 0.7), self._relative_point(1, 0.8), 
                (155, 189, 214), 30, 1.2, 4)
        self.draw_hill(self._relative_point(0, 0.6), self._relative_point(1, 0.76),
                (132, 172, 207), 40, 1.2, 6)
        self.draw_hill(self._relative_point(0, 0.54), self._relative_point(1, 0.78),
                (98, 138, 181), 80, 1, 8)
        self.draw_hill(self._relative_point(0.3, 0.4), self._relative_point(1, 0.76),
                (84, 123, 167), 80, 1, 8)
        self.draw_hill(self._relative_point(0, 0.36), self._relative_point(1, 0.4),
                (47, 79, 126), 50, 0.8, 9)
        self.draw_hill(self._relative_point(0, 0.26), self._relative_point(1, 0.16),
                (22, 49, 89), 50, 0.6, 10)

