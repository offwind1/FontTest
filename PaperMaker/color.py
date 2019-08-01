class OColor():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, rgb=(255, 255, 255)):
        self._rgb = rgb

    @property
    def red(self):
        return self._rgb[0]

    @property
    def green(self):
        return self._rgb[1]

    @property
    def blue(self):
        return self._rgb[2]

    @property
    def rgb(self):
        return self._rgb

    def setRGB(self, rgb):
        self._rgb = rgb

    def __call__(self):
        return self._rgb
