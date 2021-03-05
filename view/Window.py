#!/usr/bin/python
# coding:utf-8

"""
@author: css
@software: PyCharm
@file: Window.py
@time: 2021/3/3 22:02:25
"""
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget, QLabel)
import time
import win32gui, win32con
from util.screen import screen
import cv2 as cv


class MyThread(QThread):
    # 定义信号,定义参数为str类型
    breakSignal = pyqtSignal(int)

    # 子类的构造函数必须先调用其父类的构造函数，重写run()方法。
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        while (True):
            time.sleep(0.2)
            self.breakSignal.emit(10)


class Window(QWidget):
    isTopWin = True
    th1 = MyThread()
    selfWnd = None
    height = 80

    def __init__(self, hWnd):
        super().__init__()
        self.setGeometry(0, 0, 800, self.height)
        # Qt.WindowStaysOnTopHint |
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)

        self.hWnd = hWnd
        self.setWindowTitle("CV记牌器")
        pokerLabel = QLabel(self)
        pokerLabel.setText("牌型： 王   2   A   K   Q   J   10   9   8   7   6   5   4   3 ")
        # 设置标签的左边距，上边距，宽，高
        pokerLabel.setGeometry(QRect(0, 0, 800, 30))
        # 设置文本标签的字体和大小，粗细等
        pokerLabel.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))
        self.pokerNumLabel = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.pokerNumLabel.setGeometry(QRect(0, 25, 800, 30))
        # 设置文本标签的字体和大小，粗细等
        self.pokerNumLabel.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))

        self.handlePokerLabel = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.handlePokerLabel.setGeometry(QRect(0, 50, 800, 30))
        # 设置文本标签的字体和大小，粗细等
        self.handlePokerLabel.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))

        self.screen = QPushButton(self)
        self.screen.setText("截图")
        self.screen.setGeometry(QRect(710, 3, 50, 20))
        self.screen.clicked.connect(self.screenshot)

        self.status = QLabel(self)
        self.status.setGeometry(QRect(230, 58, 80, 20))
        self.status.setText("未开始")
        self.status.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))
        self.status.setStyleSheet('color: orange')

        self.setPokerSizeLabel = QPushButton(self)
        self.setPokerSizeLabel.setGeometry(QRect(710, 29, 80, 20))
        self.setPokerSizeLabel.setText("调整大小")
        # self.setPokerSizeLabel.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))
        self.setPokerSizeLabel.clicked.connect(self.setPokerSize)

        line = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        line.setGeometry(QRect(0, 27, 690, 1))
        line.setAutoFillBackground(True)
        line.setStyleSheet('background-color: rgb(0, 0, 0)')
        line = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        line.setGeometry(QRect(0, 52, 690, 1))
        line.setAutoFillBackground(True)
        line.setStyleSheet('background-color: rgb(0, 0, 0)')

        line = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        line.setGeometry(QRect(690, 0, 1, self.height))
        line.setAutoFillBackground(True)
        line.setStyleSheet('background-color: rgb(0, 0, 0)')
        for index in range(13):
            line = QLabel(self)
            # 设置标签的左边距，上边距，宽，高
            line.setGeometry(QRect(index * 45 + 113, 0, 1, self.height if index < 3 else 53))
            line.setAutoFillBackground(True)
            line.setStyleSheet('background-color: rgb(0, 0, 0)')

    def setStatus(self, status):
        if (status == 0):
            self.status.setText("未开始")
        elif status == 1:
            self.status.setText("开局")
        elif status == 2:
            self.status.setText("进行中")

    def setPokerSize(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hWnd)
        win32gui.SetWindowPos(self.hWnd, None, left, top, 1040, 629, win32con.SWP_SHOWWINDOW)

    def screenshot(self):
        img = screen(self.hWnd)
        cv.imwrite('screen/screen' + str(time.time()).split('.')[0] + '.png', img)

    def color(self, num):
        if num == 0:
            return 'black'
        if num == 1:
            return 'green'
        if num == 2:
            return '#66b1ff'
        if num == 3:
            return 'orange'
        if num == 4:
            return 'red'

    def setNum(self, num, handNum):
        text = '数量：'
        if len(num) > 0:
            text += '&nbsp;'
        for index, value in enumerate(num):
            text = text + self.gText(str(value), self.color(value))
            if (index == 6):
                text += ' '
        self.pokerNumLabel.setText(text)
        self.setHandPokerNum(handNum)
        # self.setStatus(status)

    def gText(self, text, color='red'):
        return "<font style = 'font-size:21px; font-weight: bold; color:" + color + ";'>" + text + "</font> &nbsp;"

    def setHandPokerNum(self, num):
        text = '底牌：'
        if len(num) > 0:
            text += '&nbsp;'
        for index in num:
            text += self.gText(str(index), 'red')
        self.handlePokerLabel.setText(text)
        # print(num)

    def chuli(self, sss):
        left, top, right, bot = win32gui.GetWindowRect(self.hWnd)
        fgWnd = win32gui.GetForegroundWindow()

        self.move(left, top - self.height)
        if fgWnd != self.hWnd and fgWnd != self.selfWnd:  # 不是顶层
            if not self.isTopWin:
                # 隐藏
                win32gui.SetWindowPos(self.selfWnd, win32con.HWND_BOTTOM, left, top - self.height, 800, self.height,
                                      win32con.SWP_SHOWWINDOW)
                self.isTopWin = True
        else:
            if self.isTopWin:
                self.isTopWin = False
                # 置顶
                win32gui.SetWindowPos(self.selfWnd, win32con.HWND_TOPMOST, left, top - self.height, 800, self.height,
                                      win32con.SWP_SHOWWINDOW)

    def showWin(self):
        self.show()
        self.selfWnd = win32gui.FindWindow(None, "CV记牌器")
        self.th1.breakSignal.connect(self.chuli)
        self.th1.start()
