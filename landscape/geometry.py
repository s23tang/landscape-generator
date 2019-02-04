import os
import random
from dataclasses import dataclass
from itertools import tee


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def midpoint_x(point1, point2):
        return (point1.x + point2.x)/2

    @staticmethod
    def midpoint_y(point1, point2):
        return (point1.y + point2.y)/2

    @staticmethod
    def midpoint(point1, point2):
        return Point(
            Point.midpoint_x(point1, point2),
            Point.midpoint_y(point1, point2)
        )

    @staticmethod
    def displaced_midpoint(point1, point2, displace_factor):
        midpoint = Point.midpoint(point1, point2)
        midpoint.displace(displace_factor)
        return midpoint

    def displace(self, displace_factor):
        self.y += random.choice([-displace_factor, displace_factor])


class XOrderedSegment:
    def __init__(self, *points):
        self.points = []
        self.add(*points)

    @property
    def pairwise_points(self):
        p1, p2 = tee(self.points)
        next(p2, None)
        return list(zip(p1, p2))

    def add(self, *points):
        for point in points:
            self._add_point(point)

    def _add_point(self, point):
        low, high = 0, len(self.points)
        while low < high:
            mid = (low+high)//2
            if point.x < self.points[mid].x:
                high = mid
            else:
                low = mid + 1
        self.points.insert(low, point)

    def iterative_displacement(self, displace_factor, roughness, iterations):
        for _ in range(iterations):
            self.displace_midpoints(displace_factor)
            displace_factor = self._roughen_displace_factor(displace_factor, roughness)

    def displace_midpoints(self, displace_factor):
        for p1, p2 in self.pairwise_points:
            displaced_midpoint = Point.displaced_midpoint(p1, p2, displace_factor)
            self.add(displaced_midpoint)

    def _roughen_displace_factor(self, displace_factor, roughness):
        return displace_factor * pow(2, -roughness)

