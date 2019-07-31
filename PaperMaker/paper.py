from PIL import ImageFont, ImageDraw, Image


class Paper():
    # 纸张大小
    PAPER_SIZE_A4 = (1280, 1280)  # PIX
    # 纸张内边距
    PAPER_MARGIN_NORMAL = (150, 188, 150, 188)  # PIX, 上左下右

    def __init__(self):
        self._size = Paper.PAPER_SIZE_A4
        self._margin = Paper.PAPER_MARGIN_NORMAL

        self._print_size = (0, 0)
        self._scale = 1

        # 分栏
        self.subField = 1
        # 间距
        self.spacing = 80

    def setSubField(self, num):
        self.subField = num

    def setSpacing(self, num):
        self.spacing = num

    @property
    def size(self):
        return self._size

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    @property
    def top(self):
        return self._margin[0]

    @property
    def left(self):
        return self._margin[1]

    @property
    def down(self):
        return self._margin[2]

    @property
    def right(self):
        return self._margin[3]

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

    def creat(self):
        return Image.new("RGB", self.size, (255, 255, 255))

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


p = Paper()
print(p)
p.setSubField(3)
p.setSpacing(40)
print(p.getEditableArea())
print(p.isEditable((400, 200)))
