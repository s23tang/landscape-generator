import pytest
from landscape.colors import RGBColor


class TestRGBColor:
    def assert_rgb_value_raises_errors(self, values):
        for value in values:
            with pytest.raises(ValueError) as err: 
                RGBColor(*value)

    def test_init_bad_colors(self):
        values = [
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1),
            (256, 0, 0),
            (0, 256, 0),
            (0, 0, 256),
            (-5, 500, -2),
            (2.5, 0, 0),
            (50, 0, 255.5),
        ]
        self.assert_rgb_value_raises_errors(values)

    def test_valid_colors(self):
        color = RGBColor(100, 25, 230)
        assert color.r == 100 and color.g == 25 and color.b ==230

    def test_to_tuple(self):
        color = RGBColor(10, 123, 55)
        assert color.to_tuple() == (10, 123, 55)

    def test_representation(self):
        assert repr(RGBColor(1,1,1)) == 'RGBColor(1, 1, 1)'

    def test_equality(self):
        c1 = RGBColor(10, 15, 20)
        c2 = RGBColor(50, 60, 230)
        c3 = RGBColor(10, 15, 20)
        assert c1 == c3 and c1 != c2 and c2 != c3

    def test_tint(self):
        c1 = RGBColor(10, 15, 20).tinted(0.1)
        assert c1 == RGBColor(34, 39, 44)
        c2 = RGBColor(255, 255, 255).tinted(0.1)
        assert c2 == RGBColor(255, 255, 255)
        c3 = RGBColor(0, 0, 0).tinted(0.1)
        assert c3 == RGBColor(26, 26, 26)
        c4 = RGBColor(0, 0, 0).tinted(0.5)
        assert c4 == RGBColor(128, 128, 128)

        with pytest.raises(ValueError) as err:
            RGBColor(10, 15, 20).tinted(1.1)

        with pytest.raises(ValueError) as err:
            RGBColor(10, 15, 20).tinted(-0.1)
        

