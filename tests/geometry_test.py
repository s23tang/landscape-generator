from PIL import Image, ImageDraw
from landscape.geometry import Point, XOrderedSegment


class TestPoint:
    def test_point_create(self):
        p = Point(1,2)
        assert p.x == 1
        assert p.y == 2

    def test_midpoint_x_calculated_correctly(self):
        mid_x_even = Point.midpoint_x(Point(-10,5), Point(8, -6))
        mid_x_rounded = Point.midpoint_x(Point(1,1), Point(2,10))
        assert mid_x_even == -1.0
        assert mid_x_rounded == 1.5

    def test_midpoint_y_calculated_correctly(self):
        mid_y_even = Point.midpoint_y(Point(-10,5), Point(8, 5))
        mid_y_rounded = Point.midpoint_y(Point(1,5), Point(2,-6))
        assert mid_y_even == 5.0
        assert mid_y_rounded == -0.5

    def test_y_displacement(self):
        p = Point(1,3)
        p.displace(5)
        assert p.y in (-2.0, 8.0)
        p.displace(-2.5)
        assert p.y in (-4.5, 0.5, 5.5, 10.5)

    def test_displaced_midpoint(self):
        p1, p2 = Point(1,2), Point(-10,9)
        p3 = Point.displaced_midpoint(p1, p2, 5)
        assert p3.x == -4.5
        assert p3.y in (0.5, 10.5)

    def test_comparison(self):
        p1, p2, p3 = Point(1,2), Point(2,3), Point(1,2)
        assert p1 == p3
        assert p1 != p2
        assert p2 != p3


class TestXOrderedSegment:
    def test_add_point_is_ordered_ascending(self):
        s = XOrderedSegment()
        p1 = Point(1,2)
        p2 = Point(-10,5)
        p3 = Point(50,-9)
        s._add_point(p1)
        assert s.points == [p1]
        s._add_point(p2)
        assert s.points == [p2, p1]
        s._add_point(p3)
        assert s.points == [p2, p1, p3]

    def test_add_multiple_points(self):
        s = XOrderedSegment()
        p1 = Point(10,10)
        p2 = Point(15,10)
        p3 = Point(-90,-50)
        s.add(p1, p2, p3)
        assert s.points == [p3, p1, p2]

        p4 = Point(5,5)
        s.add(p4)
        assert s.points == [p3, p4, p1, p2]

    def test_create_with_multiple_points(self):
        p1, p2, p3 = Point(1, 1), Point(-1, -5), Point(20, -5)
        s = XOrderedSegment(p1, p2, p3)
        assert s.points == [p2, p1, p3]

    def test_pairwise_points(self):
        s = XOrderedSegment()
        assert s.points == []
        assert s.pairwise_points == []

        p1 = Point(1,1)
        s.add(p1)
        assert s.points == [p1]
        assert s.pairwise_points == []

        p2 = Point(-3,100)
        s.add(p2)
        assert s.points == [p2, p1]
        assert s.pairwise_points == [(p2, p1)]

        p3 = Point(10, 0)
        s.add(p3)
        assert s.points == [p2, p1, p3]
        assert s.pairwise_points == [(p2, p1), (p1, p3)]

        p4 = Point(-90, 1)
        s.add(p4)
        assert s.points == [p4, p2, p1, p3]
        assert s.pairwise_points == [(p4, p2), (p2, p1), (p1, p3)]

    def test_displace_midpoints(self):
        s = XOrderedSegment()
        s.displace_midpoints(5)
        assert s.points == []

        p1 = Point(5,0)
        s.add(p1)
        s.displace_midpoints(5)
        assert s.points == [p1]

        p2 = Point(-1,1)
        s.add(p2)
        s.displace_midpoints(5)
        assert len(s.points) == 3
        assert s.points[0] == p2 and s.points[2] == p1
        assert s.points[1] in (Point(2,5.5), Point(2,-4.5))

        s.displace_midpoints(1)
        assert len(s.points) == 5
        assert s.points[0] == p2 and s.points[4] == p1
        assert s.points[2] in (Point(2,5.5), Point(2,-4.5))
        assert s.points[1].x == 0.5
        assert s.points[3].x == 3.5

    def test_iterative_displacement(self):
        s = XOrderedSegment()
        factor, rough, iters = 5, 2, 2
        s.iterative_displacement(factor, rough, iters)
        assert s.points == []

        p1 = Point(1,2)
        s.add(p1)
        s.iterative_displacement(factor, rough, iters)
        assert s.points == [p1]

        p2 = Point(3,4)
        s.add(p2)
        s.iterative_displacement(factor, rough, iters)
        assert len(s.points) == 5
        assert s.points[0] == p1 and s.points[4] == p2
        assert s.points[2] in (Point(2,8), Point(2,-2))
        assert s.points[1].x == 1.5
        assert s.points[3].x == 2.5

