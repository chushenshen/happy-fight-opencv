#!/usr/bin/python
# coding:utf-8

"""
@author: css
@software: PyCharm
@file: Poker.py
@time: 2021/3/3 16:45:02
"""
import cv2


class Poker:
    '所有员工的基类'

    def __init__(self, name, img, num=4):
        self.num = num
        self.name = name
        h, w = img.shape

        # 手牌
        self.selfImg = img
        self.isUpOut = False
        self.isDownOut = False
        # 出牌
        if name == '王':
            self.otherImg = cv2.resize(img, (int(w / 1.8), int(h / 1.8)))
            # 底牌
            self.handImg = cv2.resize(img, (int(w / 4.1), int(h / 4.1)))
        elif name == '8' or name == '9':
            self.otherImg = cv2.resize(img, (int(w / 1.3), int(h / 1.3)))
            # 底牌
            self.handImg = cv2.resize(img, (int(w / 1.9), int(h / 1.9)))
        else:
            self.otherImg = cv2.resize(img, (int(w / 1.3), int(h / 1.3)))
            # 底牌
            self.handImg = cv2.resize(img, (int(w / 1.8), int(h / 1.8)))

    def setNum(self, num):
        self.num = num

    def init(self):
        if self.name == '王':
            self.num = 2
        else:
            self.num = 4
