from PIL import ImageFont, ImageDraw, Image
from .canvas import Canvas
from .color import OColor
from .font import OFont

from utility import *
from .setting import Singleton
import random


def getRandomChar():
    return chr(random.randint(0x4E00, 0x9FA5))


class BOX(Canvas):

    def __init__(self, text):
        super().__init__()

        self.text = text
        self._font = self.setting.font
        self.real_location = self.origin

    def add_real_pos(self, point):
        self.real_location = add_point(self.real_location, point)
        return self.real_location + (self.width, self.height)

    @property
    def font(self):
        return self.setting.font

    @property
    def font_size(self):
        return self.setting.font_size

    @property
    def font_color(self):
        return self.setting.font_color

    @property
    def width(self):
        w, h = self.font.getsize(self.text)
        return w

    @property
    def height(self):
        return self.font_size

    @property
    def size(self):
        return (self.left + self.width + self.right,
                self.top + self.height + self.down)

    @property
    def contentRect(self):
        x, y = self.origin
        w, h = self.font.getsize(self.text)
        return (x, y, w, h)

    def drawText(self):
        img = self.image

        ImageDraw.Draw(img).text(self.origin, self.text, font=self.font, fill=self.font_color)
        return img


# 题号填充内容
numberTextArr = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.",
                 "11.", "12.", "13.", "14.", "15.", "16.", "17.", "18.", "19.", "20.",
                 "21.", "22.", "23.", "24.", "25.", "26.", "27.", "28.", "29.", "30."]


class Block(BOX):
    def __init__(self):
        self.setting = Singleton().block_setting
        super().__init__(getRandomChar())


def getRandomnumber():
    return random.choice(numberTextArr)


class QuestionNumber(BOX):

    def __init__(self):
        self.setting = Singleton().question_number_setting
        super().__init__(getRandomnumber())
