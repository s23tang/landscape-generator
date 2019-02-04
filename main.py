from landscape.draw import Dimensions, BlueHills


if __name__ == '__main__':
    hills = BlueHills(Dimensions(1000, 500))
    hills.render()
    hills.save('test.png')
