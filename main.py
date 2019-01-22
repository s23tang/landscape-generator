from PIL import Image, ImageDraw
from landscape.geometry import Point, XOrderedSegment

def default_colors():
    return {
        'background': (240, 203, 163),
        'layers': {
            'l1': (195, 157, 224),
            'l2': (158, 98, 204),
            'l3': (130, 79, 138),
            'l4': (68, 28, 99)
        } 
    }

def red_colors():
    return {
        'background': (235, 102, 4),
        'layers': {
            'l1': (176, 77, 20),
            'l2': (168, 84, 30),
            'l3': (119, 77, 42),
            'l4': (113, 81, 45),
            'l5': (66, 54, 32),
            'l6': (7, 7, 7)
        } 
    }

def blue_colors():
    return {
        'background': (200, 211, 220),
        'layers': {
            'l1': (155, 189, 214),
            'l2': (132, 172, 207),
            'l3': (98, 138, 181),
            'l4': (84, 123, 167),
            'l5': (47, 79, 126),
            'l6': (22, 49, 89)
        } 
    }

class LandscapePng:
    def __init__(self, width, height, colors):
        self.width = width
        self.height = height
        self.colors = colors
        self.image = self._new_image()
        self.draw = self._draw_image()

    def _new_image(self, mode='RGBA'):
        return Image.new(mode, (self.width, self.height), self.colors['background'])

    def _draw_image(self):
        return ImageDraw.Draw(self.image)

    def draw_hill(self, start_point, end_point, layer_id,
                        displacement_factor, roughness, iterations):
        s = XOrderedSegment()
        s.add(start_point, end_point)
        s.iterative_displacement(displacement_factor, roughness, iterations)
        points = [(0, self.height)] + [(p.x, self.height-p.y) for p in s.points] + [(self.width, self.height)]
        self.draw.polygon(points, self.colors['layers'][layer_id])

def draw(width, height, colors):
    lp = LandscapePng(width, height, colors)
    lp.draw_hill(Point(0, 350), Point(width, 400), 'l1', 30, 1.2, 4)
    lp.draw_hill(Point(0, 300), Point(width, 380), 'l2', 40, 1.2, 6)
    lp.draw_hill(Point(0, 270), Point(width, 390), 'l3', 80, 1, 8)
    lp.draw_hill(Point(300, 200), Point(width, 380), 'l4', 80, 1, 8)
    lp.draw_hill(Point(0, 180), Point(width, 200), 'l5', 50, 0.8, 9)
    lp.draw_hill(Point(0, 130), Point(width, 80), 'l6', 50, 0.6, 10)
    lp.image.save('test.png')

if __name__ == '__main__':
    draw(1000, 500, blue_colors())
