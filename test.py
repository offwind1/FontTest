import codecs
from multiprocessing import Pool
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import os
import json
import sys

# ROOT_DIR = os.path.abspath("")
# FONT_DIR = os.path.join(ROOT_DIR, "fonts/")

ROOT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
FONT_DIR = os.path.join(ROOT_DIR, "fonts/")

SAVE_ROOT_DIR = ""
VALUE = 0

SAVE_DIR = os.path.join(SAVE_ROOT_DIR, "imgs/")
SAVE_LABELTXT_PATH = os.path.join(SAVE_ROOT_DIR, "labs/")

SAVE_trainTXT_PATH = os.path.join(ROOT_DIR, "0717_imgs_train.txt")
SAVE_valTXT_PATH = os.path.join(ROOT_DIR, "0717_imgs_val.txt")
SAVE_ClassIDDIC_PATH = os.path.join(ROOT_DIR, "ClassIDDIC.txt")


def update_save_path(path):
    global SAVE_ROOT_DIR
    global SAVE_DIR
    global SAVE_LABELTXT_PATH

    SAVE_ROOT_DIR = path
    SAVE_DIR = os.path.join(SAVE_ROOT_DIR, "imgs")
    SAVE_LABELTXT_PATH = os.path.join(SAVE_ROOT_DIR, "labs")

    if not os.path.exists(SAVE_DIR):
        os.mkdir(SAVE_DIR)
    if not os.path.exists(SAVE_LABELTXT_PATH):
        os.mkdir(SAVE_LABELTXT_PATH)

    # print(FONT_DIR)
    # print(SAVE_DIR)
    # print(SAVE_LABELTXT_PATH)
    # print(SAVE_ClassIDDIC_PATH)


# 目的：生成训练图片
#

# 1.研究字体

# 小五＝9磅 ==(9/72)*96=12px

# 五号＝10.5磅 ==(10.5/72)*96=14px

# 小四＝12磅 ==(12/72)*96=16px

# 四号＝14磅 ==(14/72)*96=18.67 =18px
# MONBAITI.TTF 数字
# PLANTC.TTF 英文（斜体）
# KAIU.TTF 括号内中文
# SIMSUN.TTC 宋体

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_PAGE = (0, 0, 0)

# 2.opencv生成训练素材
PAGE_SIZE_YOLO = (1280, 1280)
# 1080固定宽
PAGE_SIZE_A4_COMPRESS = (763, 1080)
# 120dpi => 2105×1487 => 1080 763
PAGE_SIZE_A4_120 = (1487, 2105)
# 150dpi => 1754×1240 => 1080 763
PAGE_SIZE_A4_150 = (1240, 1754)
# 300dpi => 3508×2479 => 1080 763
PAGE_SIZE_A4_3000 = (2479, 3508)


# 头、ROI和数据


# 3.生成训练Json
# 4.制定素材数量
# 一种字体10w张
# 直接生成 orgin train val 文件，控制class的均等

# 5.进行训练

def PIL_boxdrawNubmer(box_size, text, font_org, fontname, fontsize):
    backimg = PIL_getbackgroundImg(box_size, COLOR_WHITE)
    PIL_drawText(backimg, text, font_org, fontname, fontsize, COLOR_BLACK)
    return backimg


def cv2_getbackgroundImg(size, bgcolor):
    img = np.ones(size, dtype=np.uint8)
    bgr_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    bgr_img[:, :, 0] = bgcolor[0]
    bgr_img[:, :, 1] = bgcolor[1]
    bgr_img[:, :, 2] = bgcolor[2]
    return bgr_img


def PIL_fillText_textfill(img, imgsize, textArr, fontname, padding, fontsize):
    re = img.copy()
    imgw, imgh = imgsize[0:2]
    print(imgw, imgh)
    boxw = padding * 2 + fontsize
    boxh = boxw
    count_w = int(imgw / boxw)
    count_h = int(imgh / boxh)
    len_textarr = len(textArr)
    fontcolor = COLOR_BLACK
    regions = []
    for h in range(count_h):
        org_y = h * boxh + padding
        for w in range(count_w):
            index = random.randint(0, len_textarr - 1)
            text = textArr[index]
            org_x = w * boxw + padding
            org = [org_x, org_y]
            PIL_drawText(re, text, org, fontname, fontsize, fontcolor)
    return re


def json_check_region(x, y, w, h):
    re = {}
    re["shape_attributes"] = {"name": "rect", "x": x, "y": y, "width": w, "height": h}
    re["region_attributes"] = {"page_class_id": 1}
    return re


def json_check_via(filename, regions, imagesize):
    re = {}
    re["filename"] = str(filename)
    re["size"] = " "
    re["regions"] = regions
    re["file_attributes"] = {}
    re["img_width"] = imagesize[0]
    re["img_height"] = imagesize[1]
    return re


# 保存json
def save_json(path, data):
    print(path)
    with open(path, 'w') as f:
        f.write(json.dumps(data))


# debug
def showonetextwithrect(img, rect):
    re = PIL_drawrect(img, (rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]), 'red')
    showimg(re, "one")
    return


def showimg(img, Title):
    img = np.array(img)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(12, 9))
    plt.rcParams['figure.dpi'] = 300
    # plt.axis('equal')
    xmajorLocator = MultipleLocator(100)  # 将x主刻度标签设置为20的倍数
    ymajorLocator = MultipleLocator(100)  # 将y轴主刻度标签设置为0.5的倍数
    ax = plt.gca()  # 获取到当前坐标轴信息
    ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
    ax.invert_yaxis()  # 反转Y坐标轴
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.yaxis.set_major_locator(ymajorLocator)
    plt.title(Title)
    plt.imshow(img2)
    return


def plt_drawonepoint(p, size, fillcolor, edgecolor):
    plt.scatter(p[0], p[1], s=size, edgecolors=edgecolor, c=fillcolor)
    return


def plt_drawrect(q, s, linewidth, edgecolor):
    plt.gca().add_patch(
        plt.Rectangle(xy=(q[0], q[1]), width=s[0] - q[0], height=s[1] - q[1], edgecolor=edgecolor, fill=False,
                      linewidth=linewidth))
    return


def cv2_drawonepoint(img, p, size, fillcolor):
    re = img.copy()
    cv2.circle(re, p, size, fillcolor, 0)
    return re


def PIL_drawrect(img, box, color):
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, outline=color)
    return img


def debug_typecount(info):
    return


# 变化
# 倾斜图片
def to_RotationMatrix2D(cv_img, angle, scale, direction):
    #
    # angle 角度
    # scale 缩放
    re = cv_img.copy()
    num_rows, num_cols = re.shape[:2]  # y x
    center = (num_cols / 2, num_rows / 2)
    if direction == 0:
        angle = -angle
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
    re = cv2.warpAffine(re, rotation_matrix, (num_cols, num_rows), borderValue=COLOR_WHITE)
    return re


# 仿射变换
def to_AffineTransform(cv_img, fx, direction):
    re = cv_img.copy()
    num_rows, num_cols = re.shape[:2]  # 行y 列x
    if direction == 0:  # left
        # A---B
        #    C
        src_points = np.float32([[0, 0], [num_cols - 1, 0], [num_cols - 1, num_rows - 1]])
        dst_points = np.float32(
            [[int(fx * (num_cols - 1)), 0], [(num_cols - 1), 0], [int((1 - fx) * (num_cols - 1)), (num_rows - 1)]])
    if direction == 1:  # right
        # A---B
        # C
        src_points = np.float32([[0, 0], [num_cols - 1, 0], [0, num_rows - 1]])
        dst_points = np.float32([[0, 0], [int((1 - fx) * (num_cols - 1)), 0], [int(fx * (num_cols - 1)), num_rows - 1]])

    affine_matrix = cv2.getAffineTransform(src_points, dst_points)
    re = cv2.warpAffine(re, affine_matrix, (num_cols, num_rows), borderValue=COLOR_WHITE)
    return re


# 透视图片
def to_PerspectiveTransform(cv_img, fx, direction):
    re = cv_img.copy()
    num_rows, num_cols = re.shape[:2]  # 行y 列x
    if direction == 0:  # top
        # --A--B--
        # C------D
        src_points = np.float32([[0, 0], [num_cols - 1, 0], [0, num_rows - 1], [num_cols - 1, num_rows - 1]])
        dst_points = np.float32([[int(fx * (num_cols - 1)), 0], [int((1 - fx) * (num_cols - 1)), 0], [0, num_rows - 1],
                                 [num_cols - 1, num_rows - 1]])

    if direction == 1:  # bottom
        # A------B
        # --C--D--
        src_points = np.float32([[0, 0], [num_cols - 1, 0], [0, num_rows - 1], [num_cols - 1, num_rows - 1]])
        dst_points = np.float32([[0, 0], [num_cols - 1, 0], [int(fx * (num_cols - 1)), num_rows - 1],
                                 [int((1 - fx) * (num_cols - 1)), num_rows - 1]])

    projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    re = cv2.warpPerspective(re, projective_matrix, (num_cols, num_rows), borderValue=COLOR_WHITE)
    return re


# 扭曲图像
def to_wave(cv_img, angle, direction):
    re = cv_img.copy()

    num_rows, num_cols = re.shape[:2]  # 行y 列x
    re = np.zeros(re.shape, dtype=re.dtype)
    #  0
    # 3   1
    #  2
    if direction == 0:
        for i in range(num_rows):
            for j in range(num_cols):
                offset_x = 0
                offset_y = int(angle * math.sin(2 * 3.14 * j / (2 * num_cols)))
                # print(offset_y)
                if i + offset_y < num_rows:
                    re[i, j] = cv_img[(i + offset_y) % num_rows, j]
                else:
                    re[i, j] = 255

    if direction == 1:
        for i in range(num_rows):
            for j in range(num_cols):
                offset_x = int(angle * math.sin(2 * 3.14 * i / (2 * num_cols)))
                offset_y = 0
                if j - offset_x > 0:
                    re[i, j] = cv_img[i, (j - offset_x) % num_cols]
                else:
                    re[i, j] = 255

    if direction == 2:
        for i in range(num_rows):
            for j in range(num_cols):
                offset_x = 0
                offset_y = int(angle * math.sin(2 * 3.14 * j / (2 * num_cols)))
                if i - offset_y > 0:
                    re[i, j] = cv_img[(i - offset_y) % num_rows, j]
                else:
                    re[i, j] = 255

    if direction == 3:
        for i in range(num_rows):
            for j in range(num_cols):
                offset_x = int(angle * math.sin(2 * 3.14 * i / (2 * num_cols)))
                offset_y = 0
                if j + offset_x < num_cols:
                    re[i, j] = cv_img[i, (j + offset_x) % num_cols]
                else:
                    re[i, j] = 255
    return re


def add_noise(img):
    for i in range(20):  # 添加点噪声
        temp_x = np.random.randint(0, img.shape[0])
        temp_y = np.random.randint(0, img.shape[1])
        img[temp_x][temp_y] = 255
    return img


def add_erode(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img = cv2.erode(img, kernel)
    return img


def add_dilate(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img = cv2.dilate(img, kernel)
    return img


def do(img):
    type = random.randint(1, 4)
    img = np.array(img)
    if type == 1:
        img = add_noise(img)
    if type == 2:
        img = add_erode(img)
    if type == 3:
        img = add_dilate(img)
    if type == 4:
        img = img
    return img


# def do(self,img_list=[]):
#     aug_list= copy.deepcopy(img_list)
#     for i in range(len(img_list)):
#         im = img_list[i]
#         if self.noise and random.random()<0.5:
#             im = self.add_noise(im)
#         if self.dilate and random.random()<0.25:
#             im = self.add_dilate(im)
#         if self.erode and random.random()<0.25:
#             im = self.add_erode(im)
#         aug_list.append(im)
#     return aug_list

def PIL_getbackgroundImg(size, bgcolor):
    re = Image.new("RGB", size, bgcolor)
    return re


def PIL_drawText(img, text, org, fontname, fontsize, fontcolor):
    fontpath = FONT_DIR + fontname
    font = ImageFont.truetype(fontpath, fontsize, encoding="utf-8")
    draw = ImageDraw.Draw(img)
    draw.text(org, text, font=font, fill=fontcolor)
    return


def PIL_pasteImg(img, subimg, box_org):
    # x1,y1,w,h
    img.paste(subimg, box_org)
    return img


# def PIL_boxdra
def PIL_transform_rangdom(img, index):
    if index == 1:
        # 角度：-20-20(2) | 缩放：1.0-1.1(0.01) >20*2*11=242z
        random_angle = random.randint(1, 10) * 2
        random_resize = random.randint(100, 105) / 100
        random_direction = random.randint(0, 1)
        re_backimg = to_RotationMatrix2D(img, random_angle, random_resize, random_direction)

    #     if index == 2:
    #         # 平移度：0-0.09(0.01) | 左右方向：0,1 >10*2=20z
    #         random_offset = random.randint(1,9)/100
    #         random_direction = random.randint(0,1)
    #         re_backimg = to_AffineTransform(img,random_offset,random_direction)

    if index == 2:
        # 透视度：0-0.09(0.01) | 方向：0,1 >10*2=20z
        random_offset = random.randint(1, 9) / 100
        random_direction = random.randint(0, 1)
        re_backimg = to_PerspectiveTransform(img, random_offset, random_direction)

    if index == 3:
        # 透视度：0-5(1) | 方向：0,1,2,3 >6*4=24z
        random_offset = random.randint(0, 5)
        random_direction = random.randint(0, 3)
        re_backimg = to_wave(img, random_offset, random_direction)

    if index == 4:
        # 不处理
        re_backimg = img

    return re_backimg


def PIL_boxdrawNubmer_Rangdom(numberbox_size, number, font_org, fontname, fontsize):
    backimg = PIL_getbackgroundImg(numberbox_size, COLOR_WHITE)
    PIL_drawText(backimg, number, font_org, fontname, fontsize, COLOR_BLACK)
    np_backimg = np.array(backimg)
    # 随机变化
    transformtype = random.randint(1, 4)
    re_backimg = PIL_transform_rangdom(np_backimg, transformtype)
    re_backimg = Image.fromarray(re_backimg)
    minibox_img, minibox_rect = miniBox(re_backimg)
    return re_backimg, minibox_rect, transformtype  ##x1,y1  w m h


def PIL_boxdrawquetiontext_Rangdom(questiontext_one_size, text, font_org, fontname, fontsize):
    backimg = PIL_getbackgroundImg(questiontext_one_size, COLOR_WHITE)
    PIL_drawText(backimg, text, font_org, fontname, fontsize, COLOR_BLACK)
    np_backimg = np.array(backimg)
    # 随机变化
    transformtype = random.randint(1, 4)
    re_backimg = PIL_transform_rangdom(np_backimg, transformtype)
    re_backimg = Image.fromarray(re_backimg)
    minibox_img, minibox_rect = miniBox(re_backimg)  ##x1,y1  w m h
    return re_backimg, minibox_rect, transformtype


def PIL_boxdrawQuestion_Rangdom(questionBox_size, numberBox_size, number, questionTextArr, \
                                fontname, fontsize, questiontext_h_padding, questiontext_w_padding, \
                                questionnumber_w_padding, linecount):
    backimg = PIL_getbackgroundImg(questionBox_size, COLOR_WHITE)  # 题目底图
    # questiontext_h_padding 行间距,questiontext_w_padding 字间距,questionnumber_w_padding

    # number
    numberTextimg, mininumberbox_rect, transformtype = PIL_boxdrawNubmer_Rangdom(numberBox_size, number,
                                                                                 (fontsize, fontsize), fontname,
                                                                                 fontsize)
    number_righttop_x = mininumberbox_rect[0] + mininumberbox_rect[2]
    number_righttop_y = mininumberbox_rect[1]

    re = PIL_pasteImg(backimg, numberTextimg, (0, 0, numberBox_size[0], numberBox_size[1]))

    # question text
    questiontext_one_padding = fontsize  # question text内部间距
    # questiontext_one_org = (questiontext_one_padding,questiontext_one_padding)
    questiontext_one_w = questiontext_one_padding * 2 + fontsize  # question text的宽
    questiontext_one_h = questiontext_one_w  # question text的高
    questiontext_one_size = (questiontext_one_w, questiontext_one_h)

    # question main
    questiontextbegin_x = number_righttop_x + questionnumber_w_padding
    questiontextbegin_y = number_righttop_y
    #     questiontext_w = fontsize + questiontext_w_padding*2#整个题干字宽
    #     questiontext_h = fontsize + questiontext_h_padding#整个题干字高
    #     count_w = int(math.floor((questionBox_size[0]-questiontextbegin_x)/questiontext_w))

    question_rect_Arr = []
    question_text_Arr = []
    linecount = 4  # 3
    count_w = 21  # 22
    for h in range(linecount):
        for w in range(count_w):
            indextext = random.randint(0, len(questionTextArr) - 1)
            text = questionTextArr[indextext]  # 题干内容
            questionTextimg, miniquestionText_rect, transformtype = PIL_boxdrawquetiontext_Rangdom(
                questiontext_one_size, text, (questiontext_one_padding, questiontext_one_padding), fontname, fontsize)

            # showonetextwithrect(questionTextimg,miniquestionText_rect)
            cropped_re_onetext = questionTextimg.crop((miniquestionText_rect[0], miniquestionText_rect[1],
                                                       miniquestionText_rect[0] + miniquestionText_rect[2],
                                                       miniquestionText_rect[1] + miniquestionText_rect[
                                                           3]))  # (left, upper, right, lower)
            # showimg(cropped_re_onetext,"cropped_re_onetext")
            text_org_x = questiontextbegin_x + w * (questiontext_one_padding + 5)
            text_org_y = questiontextbegin_y + h * (questiontext_one_padding + 5)
            text_org = (text_org_x, text_org_y)
            re = PIL_pasteImg(re, cropped_re_onetext, text_org)
            question_rect_Arr.append((text_org_x, text_org_y, \
                                      miniquestionText_rect[2], miniquestionText_rect[3],))
            question_text_Arr.append(text)

    # pa
    return re, mininumberbox_rect, question_rect_Arr, question_text_Arr


def creat_region(page_class_id, x, y, rect):
    region_attributes = {
        "page_class_id": page_class_id
    }

    shape_attributes = {
        "name": "rect",
        "x": x + rect[0],
        "y": y + rect[1],
        "width": rect[2],
        "height": rect[3]
    }

    return {
        "region_attributes": region_attributes,
        "shape_attributes": shape_attributes
    }


def PIL_fillText_QuestionBoxfill(img, img_size, numberTextArr, questionTextArr, fontnames, \
                                 fontsizes, questionFlow, questionLineCount):
    re = img.copy()
    imgw, imgh = img_size[0:2]
    # 随机字体和字号
    fontnameindex = random.randint(0, len(fontnames) - 1)
    fontname = fontnames[fontnameindex]  # 字体
    fontsizeindex = random.randint(0, len(fontsizes) - 1)
    fontsize = fontsizes[fontsizeindex]  # 字号

    # 纸张配置
    page_padding = 20  # 纸张边缘留白
    page_centerdis = 80  # 纸张中间留白
    questiontext_h_padding = 6  # 行间距
    questiontext_w_padding = 1  # 字间距
    questionnumber_w_padding = 8  # 题号和题干间距

    # numberbox的宽高
    numberBoxpadding = fontsize  # 内部间距
    numberBox_w = numberBoxpadding * 2 + fontsize  # numberbox的宽
    numberBox_h = numberBox_w  # numberbox的高
    numberBox_size = (numberBox_w, numberBox_h)

    # flow
    # flow = questionFlow[random.randint(0,len(questionFlow)-1)]

    # questionbox的宽高
    max_linecout = max(questionLineCount) + 1
    max_qustionBox_w = int((imgw - 2 * page_padding - page_centerdis) / 2.0)
    max_qustionBox_h = int(max_linecout * fontsize + (max_linecout + 1) * questiontext_h_padding)
    questionBox_w = max_qustionBox_w  # questionbox的宽
    questionBox_h = max_qustionBox_h  # questionbox的高
    questionBox_size = (questionBox_w, questionBox_h)

    # 布局形式
    count_w = 2
    count_h = int(math.floor(imgh / questionBox_h)) - 1
    # count_h = 1
    YOLO_txt = ""

    regions = []

    for w in range(count_w):
        questionBox_org_x = page_padding + w * page_centerdis + w * questionBox_w
        for h in range(count_h):
            questionBox_org_y = page_padding + h * questionBox_h

            # 随机题号内容和题干内容
            indexnumber = random.randint(0, len(numberTextArr) - 1)
            number = numberTextArr[indexnumber]  # 题号内容

            #             indextext = random.randint(0,len(questionTextArr)-1)
            #             text = questionTextArr[indextext]#题干内容

            # 随机行数
            linecountindex = random.randint(0, len(questionLineCount) - 1)
            linecount = questionLineCount[linecountindex]

            questionBox_orgrect = (
                questionBox_org_x, questionBox_org_y, questionBox_org_x + questionBox_w,
                questionBox_org_y + questionBox_h)
            onequestionimg, mininumberbox_rect, question_rect_Arr, question_text_Arr = PIL_boxdrawQuestion_Rangdom( \
                questionBox_size, numberBox_size, number, questionTextArr, fontname, fontsize, \
                questiontext_h_padding, questiontext_w_padding, \
                questionnumber_w_padding, linecount)

            re = PIL_pasteImg(re, onequestionimg, questionBox_orgrect)
            # 数据结果
            # renumberBox_org_x = questionBox_org_x + mininumberbox_rect[0]
            # renumberBox_org_y = questionBox_org_y + mininumberbox_rect[1]
            # renumberBox_w = mininumberbox_rect[2]
            # renumberBox_h = mininumberbox_rect[3]

            regions.append(creat_region(number[:-1], questionBox_org_x, questionBox_org_y, mininumberbox_rect))

            # renumberBox = (renumberBox_org_x, renumberBox_org_y, renumberBox_w, renumberBox_h)
            # YOLO_txt = YOLO_txt + txt_yolo(number, imgw, imgh, renumberBox) + "\n"

            # re = PIL_drawrect(re,(renumberBox[0],renumberBox[1],renumberBox[0]+renumberBox[2],renumberBox[1]+renumberBox[3]),'green')

            for index, question_rect in enumerate(question_rect_Arr):
                # print(index, question_rect)

                # requestiontext_org_x = questionBox_org_x + question_rect[0]
                # requestiontext_org_y = questionBox_org_y + question_rect[1]
                # requestiontext_w = question_rect[2]
                # requestiontext_h = question_rect[3]

                regions.append(creat_region("31", questionBox_org_x, questionBox_org_y, question_rect))

                # requestiontextBox = (requestiontext_org_x, requestiontext_org_y, requestiontext_w, requestiontext_h)
                # text = question_text_Arr[index]
                # YOLO_txt = YOLO_txt + txt_yolo(text, imgw, imgh, requestiontextBox) + "\n"
                # re = PIL_drawrect(re,(requestiontextBox[0],requestiontextBox[1],requestiontextBox[0]+requestiontextBox[2],requestiontextBox[1]+requestiontextBox[3]),'red')

    return re, regions  # YOLO_txt


def PIL_fillText_boxfill(img, img_size, numberTextArr, questionTextArr, fontname, fontsizes):
    re = img.copy()
    imgw, imgh = img_size[0:2]
    # --------------------------------------
    # |   |page_pading(纸张边缘留白)
    # |---0-------------------------------------------
    # |   | fontpadding |           |             |
    # |   |  |-------|  |           |             |
    # |   |  | size  |  |box_padding|             |
    # |   |  |-------|  |box_padding|             |
    # |   |             |           |             |
    # |   |-------------|           |-------------|

    # 随机字体和字号
    fontnameindex = random.randint(0, len(fontnames) - 1)
    fontname = fontnames[fontnameindex]
    fontsizeindex = random.randint(0, len(fontsizes) - 1)
    fontsize = fontsizes[fontsizeindex]
    len_numberTextArr = len(numberTextArr)

    fontpadding = fontsize * 2  # box内部留白
    page_padding = 10  # 纸张边缘留白

    # 画图box尺寸
    boxw = fontpadding * 2 + fontsize  # fontpadding 字体至box边缘留白
    boxh = boxw
    box_size = (boxw, boxh)

    # 生成box尺寸
    fontbox_w = boxw - 2 * fontpadding
    fontbox_h = boxh - 2 * fontpadding

    # 行列个数
    count_w = int(math.floor(imgw / boxw))
    count_h = int(math.floor(imgh / boxh))

    txts = ""
    infos = []
    for h in range(count_h):
        box_org_y = page_padding + h * boxh
        for w in range(count_w):
            # 随机挑选内容
            index = random.randint(0, numberTextArr - 1)
            number = numberTextArr[index]
            oneTextimg, minibox_rect, type = PIL_boxdrawNubmer_Rangdom(box_size, number, (fontpadding, fontpadding),
                                                                       fontname, fontsize)
            # infos.append(info)
            # 填充box
            box_org_x = page_padding + w * boxw
            box_org_size = (box_org_x, box_org_y, box_org_x + boxw, box_org_y + boxh)
            re = PIL_pasteImg(re, oneTextimg, box_org_size)

            # 数据结果
            rebox_org_x = box_org_x + minibox_rect[0]
            rebox_org_y = box_org_y + minibox_rect[1]
            rebox_w = minibox_rect[2]
            rebox_h = minibox_rect[3]
            # rebox_size = (rebox_org_x,rebox_org_y,rebox_org_x+rebox_w,rebox_org_y+rebox_h)
            txts = txts + txt_yolo(imgw, imgh, rebox_org_x, rebox_org_y, rebox_w, rebox_h) + "\n"

            # debug
            fontbox_org_x = box_org_x + fontpadding
            fontbox_org_y = box_org_y + fontpadding
            # re = PIL_drawrect(re,(fontbox_org_x,fontbox_org_y,fontbox_org_x+fontbox_w,fontbox_org_y+fontbox_h),'red')
            # re = PIL_drawrect(re,box_org_size,'blue')
            # re = PIL_drawrect(re,rebox_size,'green')
    re = np.array(re)
    re = cv2.cvtColor(re, cv2.COLOR_RGB2GRAY)
    re = cv2.adaptiveThreshold(re, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 185, 15)
    re = Image.fromarray(re)
    return re, txts


def PIL_saveImg(img, name):
    savepath = os.path.join(SAVE_DIR, name)
    print(savepath)
    img.save(savepath)
    return


def txt_yolo(text, imgw, imgh, box):
    # 类别  box中心x  box中心y  box宽  box高
    # 0  0.5  0.9  0.03  0.02

    # text <-> classid
    classid = ClassIDDIC[text]
    x, y, w, h = box[:4]
    centerx = (x + w / 2.0) / (imgw * 1.0)
    centery = (y + h / 2.0) / (imgh * 1.0)
    pw = w / (imgw * 1.0)
    ph = h / (imgh * 1.0)
    re = str(classid) + " " + str(centerx) + " " + str(centery) + " " + str(pw) + " " + str(ph)
    return re


# 保存txt
def save_txt(path, data):
    print(path)
    with open(path, 'w') as f:
        f.write(data)

    return


def save_dic(path, dic):
    print(path)
    txt = ""
    for index in range(len(dic)):
        values = dic.values()
        values = list(values)
        keys = dic.keys()
        keys = list(keys)
        saveone = str(values[index]) + "," + str(keys[index])
        txt = txt + str(saveone) + "\n"
    with open(path, 'w') as f:
        f.write(txt)
    return


# test minibox
def miniBox(img):
    re = img.copy()
    re = np.array(re)

    gray = cv2.cvtColor(re, cv2.COLOR_RGBA2GRAY)
    threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 1)
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #     showimg(gray,"gray")
    #     showimg(threshold,"threshold")

    box_xs = []
    box_ys = []
    for i in range(0, len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        #         if DEBUG:
        #             cv2.rectangle(re, (x,y), (x+w,y+h), (153,153,0), 1)
        box_xs.append(x)
        box_xs.append(x + w)
        box_ys.append(y)
        box_ys.append(y + h)

    padding = 2
    minbox_minx = min(box_xs)
    minbox_maxx = max(box_xs)
    minbox_miny = min(box_ys)
    minbox_maxy = max(box_ys)

    expand_minbox_x1 = minbox_minx - padding
    expand_minbox_y1 = minbox_miny - padding
    expand_minbox_x2 = minbox_maxx + padding
    expand_minbox_y2 = minbox_maxy + padding
    # x1,y1  w m h
    box_rect = (
        expand_minbox_x1, expand_minbox_y1, expand_minbox_x2 - expand_minbox_x1, expand_minbox_y2 - expand_minbox_y1)

    return re, box_rect


# main 10W = 10gb 100W=100GB
ImgBegin = 1
ImgCount = 2  # 100000

# 生成白色背景图
pagesize = PAGE_SIZE_YOLO
backimg = PIL_getbackgroundImg(pagesize, COLOR_WHITE)

# 字体文件名
fontnames = ["simfang.ttf", "SIMLI.TTF", "simsun.ttc"]

questionfontnames = ["batang.ttc", "CALISTI.TTF", "GARA.TTF", "himalaya.ttf", "kaiu.ttf", "MONBAITI.TTF",
                     "msmincho.ttc", "Shonar.ttf", "simfang.ttf", "SIMLI.TTF", "simsun.ttc", "simsunb.ttf",
                     "times.ttf"]

# 字号14-18
fontsizes = [14, 16, 18]

# 题号填充内容
numberTextArr = ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.",
                 "11.", "12.", "13.", "14.", "15.", "16.", "17.", "18.", "19.", "20.",
                 "21.", "22.", "23.", "24.", "25.", "26.", "27.", "28.", "29.", "30."]

# 题干填充内容
questionTextArr = []
start, end = (0x4E00, 0x9FA5)  # 汉字编码的范围
for codepoint in range(int(start), int(end)):
    questionTextArr.append(chr(codepoint))

# text number - classid 对应表
global ClassIDDIC
ClassIDDIC = dict()
AllTextArr = numberTextArr + questionTextArr
dicLen = len(numberTextArr) + len(questionTextArr)
for i in range(dicLen):  # 0 - (diclen-1)
    ClassIDDIC[AllTextArr[i]] = str(i)

# save_dic(SAVE_ClassIDDIC_PATH,ClassIDDIC)

# 题干模式
questionFlow = [1, 2]

# 题干行数
questionLineCount = [2, 3, 4, 5]


def save_json__(path, json_data):
    print(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(json_data))


def go(msg, func=None):
    # json = {}
    # savelabelpath = os.path.join(SAVE_LABELTXT_PATH, "creat_page.json")

    for i in range(ImgBegin, ImgCount):
        json = {}
        savelabelpath = os.path.join(SAVE_LABELTXT_PATH, "creat_page_{}.json".format(i))

        savename = "creat_page_" + str(i) + ".jpg"

        # fill_re,txts = PIL_fillText_boxfill(backimg,pagesize,numberTextArr,fontnames,fontsizes)
        fill_re, regions = PIL_fillText_QuestionBoxfill(backimg, pagesize, numberTextArr, questionTextArr, fontnames,
                                                        fontsizes, questionFlow, questionLineCount)
        PIL_saveImg(fill_re, savename)
        # print(YOLO_txt)
        # save_txt(savelabelpath, YOLO_txt)

        json[savename] = {
            "filename": savename,
            "regions": regions,
            "size": "",
            "file_attributes": {}
        }

        fill_re = do(fill_re)
        showimg(fill_re, str(i))
        save_json__(savelabelpath, json)

        if func:
            func()

    # save_json__(savelabelpath, json)

    return


# go(1)


# p = Pool(16)
# p.apply_async(go, args=(1,))
# p.close()
# p.join()
# print('All subprocesses done.')
# 切分数据

def cut_train_val(msg):
    result = []
    for maindir, subdir, file_name_list in os.walk(SAVE_DIR):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            result.append(apath)

    length = len(result)
    print("原图数量：", length)
    if length < 20:
        train_index_end = int(length - 4)
    else:
        train_index_end = int(length * 0.8)
    trains = result[:train_index_end]
    trainstxt = ""
    for path in trains:
        trainstxt = trainstxt + path + "\n"
    save_txt(SAVE_trainTXT_PATH, trainstxt)

    vals = result[train_index_end:length]
    valstxt = ""
    for path in vals:
        valstxt = valstxt + path + "\n"
    save_txt(SAVE_valTXT_PATH, valstxt)
    return


# cut_train_val(1)

def txt_to_json(txtpath, jsonpath):
    return
