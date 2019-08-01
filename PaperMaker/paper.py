from PIL import ImageFont, ImageDraw, Image
from .canvas import Canvas
from .color import OColor
from .question import Question
from utility import *
from .setting import Singleton


class Paper(Canvas):
    # 纸张大小
    PAPER_SIZE_A4 = (1280, 1280)  # PIX
    # 纸张内边距
    PAPER_MARGIN_NORMAL = (150, 188, 150, 188)  # PIX, 上左下右

    def __init__(self, size=PAPER_SIZE_A4, margin=PAPER_MARGIN_NORMAL, color=OColor.WHITE):
        self.setting = Singleton().paper_setting

        super().__init__()

        self._size = self.setting.size
        self.subField = self.setting.subField
        self.spacing = self.setting.spacing
        # self._size = size
        # # 分栏
        # self.subField = 1
        # # 间距
        # self.spacing = 80

        self.img = self.image

        self.reouser_list = []

    def setSubField(self, num):
        self.subField = num

    def setSpacing(self, num):
        self.spacing = num

    def pasteImage(self, point, img):
        self.img.paste(img, point)

    @property
    def size(self):
        return self._size

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    def setPaperSize(self, size):
        self._size = size

    def setPaperMargin(self, margin):
        self._margin = margin

    def getOneSubFieldWidth(self):
        off_paper_margin_width = self.width - self.left - self.right
        return round((off_paper_margin_width - (self.spacing * (self.subField - 1))) / self.subField)

    def getEditableArea(self):
        """
            获取可编辑区域
            :return x,y,w,h
        """
        sub_field_width = self.getOneSubFieldWidth()
        off_paper_margin_height = self.height - self.top - self.down

        list = []
        for i in range(self.subField):
            x = self.left + sub_field_width * i + self.spacing * i
            y = self.top
            width = sub_field_width
            height = off_paper_margin_height

            list.append((x, y, width, height))

        return list

    def addQuestions(self, ):
        for rect in self.getEditableArea():
            self.addQuestionsInRect(rect)

    def addQuestionsInRect(self, rect):
        x, y, w, h = rect
        focus_point = (x, y)

        question = Question(w)
        while add_point_y(focus_point, question.size) < y + h:
            self.pasteImage(focus_point, question.img)
            self.reouser_list.extend(question.chars_box(focus_point))
            focus_point = (x, add_point_y(focus_point, question.size))
            question = Question(w)

    def creat_regions(self):

        regions = []
        for x, y, w, h in self.reouser_list:
            regions.append({
                "region_attributes": {
                    "page_class_id": 1
                },
                "shape_attributes": {
                    "name": "rect",
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                }
            })

        json = {
            "filename": "123.jpg",
            "regions": regions,
            "size": "",
            "file_attributes": {}
        }

        return json

    def isEditable(self, point):
        """
        :param point:(x, y)
        :return: bool
        """
        px, py = point
        list = self.getEditableArea()

        for i, (x, y, w, h) in enumerate(list):
            if px > x and py > y and px < (x + w) and py < (y + h):
                return (x, y, w, h)
        return False

    def __str__(self):
        list = [
            "class: {}".format(self.__class__),
            "纸张大小: 宽度:{} pix 高度:{} pix".format(self.width, self.height),
            """
            页边距:
            上:{} pix 下:{} pix
            左:{} pix 右:{} pix
            """.format(self.top,
                       self.down,
                       self.left,
                       self.right),
        ]

        return "\n".join(list)
