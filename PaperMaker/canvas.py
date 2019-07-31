from PIL import ImageFont, ImageDraw, Image


class Canvas():

    def __init__(self, text):
        self.text = text
        self.font_path = r"F:\CODE\asd\FontTest\Fonts\simsun.ttc"
        self.font_size = 24
        self.margin = (0, 0, 0, 0)
        self.font_color = (0, 0, 0)
        self.bgcolor = (255, 255, 255)

    @property
    def font(self):
        return ImageFont.truetype(self.font_path, self.font_size, encoding="utf-8")

    @property
    def top(self):
        return self.margin[0]

    @property
    def left(self):
        return self.margin[1]

    @property
    def down(self):
        return self.margin[2]

    @property
    def right(self):
        return self.margin[3]

    @property
    def size(self):
        x, y = self.font.getsize(self.text)
        return (self.left + x + self.right, self.top + self.font_size + self.down)

    def setFont_size(self, font_size):
        self.font_size = font_size

    def setMargin(self, margin):
        self.margin = margin

    def drawText(self):
        img = Image.new("RGB", self.size, self.bgcolor)
        draw = ImageDraw.Draw(img)
        draw.text((self.margin[0], self.margin[1]), self.text, font=self.font, fill=self.font_color)
        return img


def PIL_saveImg(img):
    savepath = "123.jpg"
    print(savepath)
    img.save(savepath)
    return


img = Image.new("RGB", (500, 500), (255, 255, 255))

strrrr = """一嘎达商店里盖卡是的健康的
阿克苏都会开始的卡收到就好阿萨德换了卡金黄色的
阿萨德了开奖号爱德华按时肯定会
"""

size_temp = (0, 0)

n = 0
for i in strrrr:
    if i == '\n':
        n += 1
        size_temp = (0, size_temp[1] + font_size[1])
        continue

    c = Canvas(i)
    font_size = c.size

    im = c.drawText()
    img.paste(im, size_temp)
    size_temp = (size_temp[0] + font_size[0], size_temp[1])
    print(font_size, size_temp)

PIL_saveImg(img)
#
# font = ImageFont.truetype(r"F:\CODE\asd\FontTest\Fonts\batang.ttc", 14, encoding="utf-8")
# print(font.getsize(","))
