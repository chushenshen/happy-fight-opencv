#!/usr/bin/python
# coding:utf-8

"""
@author: css
@software: PyCharm
@file: main.py
@time: 2021/3/3 16:32:04
"""
from vo.Poker import Poker
from util.screen import *
from view.Window import (Window, QThread, pyqtSignal, time, QtWidgets)
import sys

hWnd = win32gui.FindWindow(None, "欢乐斗地主")
continueGame = cv2.imread('templete/continue_game.png', 0)
# 0 没有出牌，1第一次检测到，2第二次检测到
isUpOut = 0
isDownOut = 0
isSelfOut = 0
# 0 结束，1 第一次开局，2 记牌中
status = 0
PokerList = [
    Poker('王', cv2.imread('templete/dawang.png', 0), 2),
    Poker('2', cv2.imread('templete/fangkuai_2.png', 0)),
    Poker('A', cv2.imread('templete/fangkuai_a_b.png', 0)),
    Poker('K', cv2.imread('templete/fangkuai_k_1.png', 0)),
    Poker('Q', cv2.imread('templete/fangkuai_q_b.png', 0)),
    Poker('J', cv2.imread('templete/fangkuai_j_b.png', 0)),
    Poker('10', cv2.imread('templete/fangkuai_10_b.png', 0)),
    Poker('9', cv2.imread('templete/fangkuai_9_b.png', 0)),
    Poker('8', cv2.imread('templete/fangkuai_8_b.png', 0)),
    Poker('7', cv2.imread('templete/fangkuai_7.png', 0)),
    Poker('6', cv2.imread('templete/fangkuai_6_b.png', 0)),
    Poker('5', cv2.imread('templete/fangkuai_5.png', 0)),
    Poker('4', cv2.imread('templete/fangkuai_4.png', 0)),
    Poker('3', cv2.imread('templete/fangkuai_3_b.png', 0))
    # Poker('王', cv2.imread('templete/dawang.png', 0), 2),
    # Poker('2', cv2.imread('templete/fangkuai_2_b.png', 0)),
    # Poker('A', cv2.imread('templete/fangkuai_a_b.png', 0)),
    # Poker('K', cv2.imread('templete/fangkuai_k_b.png', 0)),
    # Poker('Q', cv2.imread('templete/fangkuai_q_b.png', 0)),
    # Poker('J', cv2.imread('templete/fangkuai_j_b.png', 0)),
    # Poker('10', cv2.imread('templete/fangkuai_10_b.png', 0)),
    # Poker('9', cv2.imread('templete/fangkuai_9_b.png', 0)),
    # Poker('8', cv2.imread('templete/fangkuai_8_b.png', 0)),
    # Poker('7', cv2.imread('templete/fangkuai_7_b.png', 0)),
    # Poker('6', cv2.imread('templete/fangkuai_6_b.png', 0)),
    # Poker('5', cv2.imread('templete/fangkuai_5_b.png', 0)),
    # Poker('4', cv2.imread('templete/fangkuai_4_b.png', 0)),
    # Poker('3', cv2.imread('templete/fangkuai_3_b.png', 0))
]


class MyThread(QThread):
    breakSignal = pyqtSignal(list, list)
    statusSignal = pyqtSignal(int)

    # 子类的构造函数必须先调用其父类的构造函数，重写run()方法。
    def __init__(self):
        super().__init__()

    def matchImgNum(self, bgImg, templeteImg, threshold=0.92, save=False):
        res = cv2.matchTemplate(bgImg, templeteImg, cv2.TM_CCOEFF_NORMED)
        # tt = bgImg.copy()
        # w, h = templeteImg.shape[::-1]
        loc = np.where(res >= threshold)
        num = 0
        if len(loc[0]) != 0:
            last = 0
            # 排序
            loc[1].sort()
            for point in loc[1]:
                if abs(last - point) > 5:
                    num += 1
                    # if save:
                    # print(save)
                    # for pt in zip(*loc[::-1]):
                    #     cv2.rectangle(tt, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    # cv2.imwrite('res22.png', tt)
                last = point

        return num

    def main(self):

        global isUpOut
        global isDownOut
        global isSelfOut
        global status
        templates = PokerList
        img_rgb = screen(hWnd)

        if img_rgb is None:
            return
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        selfCard = img_gray[350:622, 10:1042]
        upotherCard = img_gray[150:290, 10:550]
        downotherCard = img_gray[150:290, 520:1040]
        selfOutCard = img_gray[280:390, 200:900]
        handCard = img_gray[50:110, 450:570]
        # cv2.imwrite('res33.png', handCard)
        num = self.matchImgNum(img_gray, continueGame, 0.74)
        if (num > 0):
            '''判断结束'''
            print('结束')
            status = 0
            self.statusSignal.emit(status)
            return
        selfList = []
        upotherList = []
        downotherList = []
        # 自家出牌列表
        selfOutList = []
        handList = []
        for pokerObj in templates:
            if status > 0:
                # 判断手牌
                if status == 1:
                    num = self.matchImgNum(selfCard, pokerObj.selfImg)
                    pokerObj.num = pokerObj.num - num
                    if (num > 0):
                        print(pokerObj.name, num, end='|')
                    # cv2.imwrite('aaa.png', selfCard)

                selfList.append(pokerObj.num)

                # 判断上家出牌，
                num = self.matchImgNum(upotherCard, pokerObj.otherImg, 0.85)
                # cv2.imwrite('bgImgu.png', upotherCard)
                if num > 0:
                    upotherList.append({'name': pokerObj.name, 'num': num})
                # 下家出牌
                num = self.matchImgNum(downotherCard, pokerObj.otherImg, 0.85)
                if num > 0:
                    downotherList.append({'name': pokerObj.name, 'num': num})

                # 自家出牌
                num = self.matchImgNum(selfOutCard, pokerObj.otherImg, 0.85)
                # cv2.imwrite('bgImgSelf.png', selfOutCard)
                if num > 0:
                    selfOutList.append({'name': pokerObj.name, 'num': num})
            # 判断底牌
            num = self.matchImgNum(handCard, pokerObj.handImg, 0.8)
            if num > 0:
                for ind in range(num):
                    handList.append(pokerObj.name)

        if status == 1:
            status = 2
            self.statusSignal.emit(status)
        if len(handList) > 0 and status == 0:
            print("开始")
            status = 1
            self.statusSignal.emit(status)
            print("底牌")
            print(handList)
            for pokerObj in templates:
                pokerObj.init()

        if len(upotherList) != 0:
            if isUpOut == 1:
                isUpOut = 2
            elif isUpOut == 2:
                print("上家：", end='')
                print(upotherList)
                for i, pokerObj in enumerate(templates):
                    for out in upotherList:
                        if pokerObj.name == out.get('name'):
                            pokerObj.num = pokerObj.num - out.get('num')
                            selfList[i] = pokerObj.num
                isUpOut = 3
            elif isUpOut == 3:
                pass
            else:
                isUpOut = 1
        else:
            isUpOut = 0

        if len(downotherList) != 0:
            if isDownOut == 1:
                isDownOut = 2
            elif isDownOut == 2:
                print("下家：", end='')
                print(downotherList)
                for i, pokerObj in enumerate(templates):
                    for out in downotherList:
                        if pokerObj.name == out.get('name'):
                            pokerObj.num = pokerObj.num - out.get('num')
                            selfList[i] = pokerObj.num
                isDownOut = 3
            elif isDownOut == 3:
                pass
            else:
                isDownOut = 1
        else:
            isDownOut = 0

        if len(selfOutList) != 0:
            if isSelfOut == 1:
                isSelfOut = 2
            elif isSelfOut == 2:
                print("自家：", end='')
                print(selfOutList)
                # 自家出牌不减少牌
                # for i, pokerObj in enumerate(templates):
                #     for out in selfOutList:
                #         if pokerObj.name == out.get('name'):
                #             pokerObj.num = pokerObj.num - out.get('num')
                #             selfList[i] = pokerObj.num
                isSelfOut = 3
            elif isSelfOut == 3:
                pass
            else:
                isSelfOut = 1
        else:
            isSelfOut = 0

        self.breakSignal.emit(selfList, handList)

    def run(self):
        while True:
            time.sleep(0.5)
            self.main()


def main():
    app = QtWidgets.QApplication([])
    window = Window(hWnd)
    th1 = MyThread()
    th1.breakSignal.connect(window.setNum)
    th1.statusSignal.connect(window.setStatus)
    th1.start()
    # window.setStyleSheet('background-color: rgba(0, 0, 0, 0); border-radius:25px; border:2px solid;')
    window.showWin()
    # window.setNum(1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
