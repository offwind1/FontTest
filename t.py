from PaperMaker.paper import Paper
from PaperMaker.setting import Singleton


def PIL_saveImg(img):
    savepath = "123.jpg"
    print(savepath)
    img.save(savepath)
    return


setting = Singleton().block_setting
# setting.font_color = (0, 0, 0)

p = Paper()
p.addQuestions()

PIL_saveImg(p.img)
