import os
import tempfile
import pytest
from landscape.geometry import Point
from landscape.draw import Dimensions, LandscapeImage, DEFAULT_DRAW_MODE


class TestDimensions:
    def assert_create_dimensions_error(self, width, height):
        with pytest.raises(ValueError) as err:
            Dimensions(width, height)

    def test_create_dimensions(self):
        d1 = Dimensions(100, 10)

        assert d1.width == 100 and d1.height == 10
        self.assert_create_dimensions_error(-10, 10)
        self.assert_create_dimensions_error(10, -10)
        self.assert_create_dimensions_error(0.5, 10)
        self.assert_create_dimensions_error(10, 0.9)
        self.assert_create_dimensions_error(10, -0.9)
        self.assert_create_dimensions_error(-0.8, 10)

    def test_equality(self):
        d1 = Dimensions(1, 1)
        d2 = Dimensions(10, 50)
        d3 = Dimensions(1, 1)
        
        assert d1 != d2 and d2 != d3 and d1 == d3


class TestLandscapeImage:
    def assert_points_outside_image_error(self, image, *points):
        for point in points:
            with pytest.raises(ValueError) as err:
                image._check_points_in_image(point)

    def assert_images_save(self, image, filenames):
        temp_dir = tempfile.TemporaryDirectory()

        for filename in filenames:
            filename = os.path.join(temp_dir.name, filename)
            image.save(filename)
            assert os.path.isfile(filename)

        temp_dir.cleanup()

    def test_create_landscape_image(self):
        dim = Dimensions(100, 10)
        image = LandscapeImage(dim)

        assert image.dimensions == dim
        assert image.image.mode == DEFAULT_DRAW_MODE
        assert image.image.size == (dim.width, dim.height)
        assert image.image.im == image.draw_tool.im

    def test_checking_invalid_points(self):
        image = LandscapeImage(Dimensions(50, 50))
        image._check_points_in_image(Point(0, 50), Point(50, 0), Point(0, 0), Point(50, 50))
        self.assert_points_outside_image_error(
            image, Point(-1, -1), Point(0, 51), Point(55, 40), Point(10, -40))

    def test_get_polygon_coordinates(self):
        p1, p2, p3 = Point(1,1), Point(2,2), Point(3,3)
        image = LandscapeImage(Dimensions(10,10))
        coordinates = image._polygon_draw_coordinates([p1, p2, p3])
        
        assert coordinates == [(1,10), (1,9), (2,8), (3,7), (3,10)]

    def test_draw_hill(self):
        p1, p2 = Point(2,4), Point(9,5)
        image = LandscapeImage(Dimensions(10,10))
        image.draw_hill(p1, p2, (10,10,10), 30, 1.2, 4)

    def test_saves(self):
        image = LandscapeImage(Dimensions(8,8))
        filenames = ['_test.jpg', '_test.jpg', '_test.png', '_test.gif']
        self.assert_images_save(image, filenames)
