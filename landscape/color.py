class RGBColor:
    MIN_VAL = 0
    MAX_VAL = 255

    def __init__(self, r, g, b):
        self._are_rgb_values_valid(r, g, b)
        self.r = r
        self.g = g
        self.b = b

    def _are_rgb_values_valid(self, *values):
        for value in values:
            self._is_rgb_value_valid(value)

    def _is_rgb_value_valid(self, value):
        if (value < self.MIN_VAL 
            or value > self.MAX_VAL 
            or not isinstance(value, int)):
            raise ValueError(f'invalid rgb value: {value}')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.r}, {self.g}, {self.b})'

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple()

    def to_tuple(self):
        return (self.r, self.g, self.b)

    def tinted(self, factor):
        r = self._tint_value(self.r, factor)
        g = self._tint_value(self.g, factor)
        b = self._tint_value(self.b, factor)
        return RGBColor(r, g, b)

    def _is_factor_valid(self, factor):
        if factor < 0 or factor > 1:
            raise ValueError(f'invalid factor: {factor}')

    def _tint_value(self, value, factor):
        return round(value + ((self.MAX_VAL - value) * factor))
        
