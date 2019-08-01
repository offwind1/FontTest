from .canvas import Canvas
from .color import OColor
from .block import Block, QuestionNumber
from .font import OFont
import random
from utility import *
from .setting import Singleton


def getRandomChar():
    return chr(random.randint(0x4E00, 0x9FA5))


class Question(Canvas):

    def __init__(self, width):
        self.setting = Singleton().question_setting

        super().__init__()
        self._width = width
        self._height = 800
        self.retract = self.setting.retract

        self.img = self.image
        self.push_point = (0, 0)

        chars_num = random.randint(*self.setting.chars_range)

        self.question_number = QuestionNumber()
        self.addQuestionNumber()

        self.question_chars = [Block() for s in range(chars_num)]
        self.addQuestionChars()

        self.img = self.img.crop((0, 0) + self.size)

    def chars_box(self, point):
        chars_box = [block.add_real_pos(point) for block in self.question_chars]
        chars_box += [self.question_number.add_real_pos(point)]
        return chars_box

    @property
    def size(self):
        return (self._width, self._height)

    def addQuestionNumber(self):
        self.pasteImage(self.origin, self.question_number.drawText())
        self.question_number.add_real_pos(self.origin)
        self.push_point = add_point(self.origin, self.question_number.size)

    def pasteImage(self, point, img):
        self.img.paste(img, point)

    def getStartPoint(self, y):
        """
        ||——————————————————||
        ||——————————————————||
        ||      |  x now_point
        ||      |           ||
        ||      |           ||
        ||------*push_point ||
        ||                  ||
        ||                  ||
        ||                  ||
        ||                  ||
        ||——————————————————||
        |————————————————————|
        :param now_point:
        :return:
        """
        if y < self.push_point[1]:
            x = self.push_point[0]
            if x < self.startX:
                x = self.startX
        else:
            x = self.startX
        return x, y

    @property
    def startX(self):
        """
        x = margin_left + retract
        :return:
        """
        return self.left + self.retract

    @property
    def limitX(self):
        return self._width - self.right

    def checkFocus(self, focus, char_block):
        x, y = focus
        w, h = char_block.size
        if x + w > self.limitX:
            focus = self.getStartPoint(y + h)
        return focus

    def addQuestionChars(self):
        focus_point = self.getStartPoint(self.origin[1])

        for char_block in self.question_chars:
            focus_point = self.checkFocus(focus_point, char_block)
            self.pasteImage(focus_point, char_block.drawText())
            char_block.add_real_pos(focus_point)

            focus_point = (add_point_x(focus_point, char_block.size), focus_point[1])

        self._height = add_point_y(focus_point, char_block.size) + self.down
