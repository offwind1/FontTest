# class
from .color import OColor
from PIL import ImageFont


class ColorSetting():

    def __init__(self):
        self._color = OColor.WHITE

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color


class FontSetting():
    def __init__(self):
        self._font_path = "Fonts\simkai.ttf"
        self._font_size = 16
        self._encoding = "utf-8"
        self._font_color = OColor.BLACK

    @property
    def font_path(self):
        return self._font_path

    @font_path.setter
    def font_path(self, font_path):
        self._font_path = font_path

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, encoding):
        self._encoding = encoding

    @property
    def font(self):
        return ImageFont.truetype(self._font_path, self._font_size, encoding=self._encoding)

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def color(self, color):
        self._font_color = color


class MarginSetting(ColorSetting):

    def __init__(self):
        super().__init__()

        print("init MarginSetting")
        self._top = 0
        self._left = 0
        self._down = 0
        self._right = 0

    @property
    def margin(self):
        return (self._top, self._left, self._down, self._right)

    @margin.setter
    def margin(self, margin):
        self._top = margin[0]
        self._left = margin[1]
        self._down = margin[2]
        self._right = margin[3]

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, top):
        self._top = top

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left):
        self._left = left

    @property
    def down(self):
        return self._down

    @down.setter
    def down(self, down):
        self._down = down

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right):
        self._right = right


class SizeSetting():
    def __init__(self):
        self.w = 1280
        self.h = 1280

        print("init SizeSetting")

    @property
    def size(self):
        return (self.w, self.h)

    @property
    def width(self):
        return self.w

    @width.setter
    def width(self, w):
        self.w = w

    @property
    def height(self):
        return self.h

    @height.setter
    def height(self, h):
        self.h = h


class BlockSetting(MarginSetting, FontSetting):
    def __init__(self):
        MarginSetting.__init__(self)
        FontSetting.__init__(self)


class QuestionNumberSetting(MarginSetting, FontSetting):
    def __init__(self):
        MarginSetting.__init__(self)
        FontSetting.__init__(self)


class QuestionSetting(MarginSetting):
    def __init__(self):
        MarginSetting.__init__(self)

        self._retract = 20
        self._chars_min = 80
        self._chars_max = 130

    @property
    def chars_range(self):
        return self._chars_min, self._chars_max

    @property
    def chars_min(self):
        return self.chars_min

    @chars_min.setter
    def chars_min(self, min):
        self._chars_min = min

    @property
    def chars_max(self):
        return self._chars_max

    @chars_max.setter
    def chars_max(self, max):
        self._chars_max = max

    @property
    def retract(self):
        return self._retract

    @retract.setter
    def retract(self, retract):
        self._retract = retract


class PaperSetting(MarginSetting, SizeSetting):

    def __init__(self):
        # super(PaperSetting, self).__init__()
        # 分栏
        MarginSetting.__init__(self)
        SizeSetting.__init__(self)

        print("init PaperSetting")

        self._subField = 1
        # 间距
        self._spacing = 80

    @property
    def subField(self):
        return self._subField

    @subField.setter
    def subField(self, sub):
        self.subField = sub

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, spacing):
        self._spacing = spacing


class Setting():
    def __init__(self):
        self.paper_setting = PaperSetting()
        self.question_setting = QuestionSetting()
        self.question_number_setting = QuestionNumberSetting()
        self.block_setting = BlockSetting()


class Singleton():
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = Setting()
        return cls.instance
