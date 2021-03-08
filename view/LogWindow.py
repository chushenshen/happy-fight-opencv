#!/usr/bin/python
# coding:utf-8

"""
@author: css
@software: PyCharm
@file: LogWindow.py
@time: 2021/3/8 13:18:41
"""
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QWidget, QLabel)
import time
import win32gui, win32con


class LogWindow(QWidget):
    isTopWin = True
    selfWnd = None
    height = 400
    width = 200

    def __init__(self, hWnd):
        super().__init__()
        self.setGeometry(500, 0, self.width, self.height)
        # Qt.WindowStaysOnTopHint |
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)

        self.hWnd = hWnd
        self.setWindowTitle("CV记牌器日志")
        pokerLabel = QLabel(self)
        pokerLabel.setText("出牌日志")
        # 设置标签的左边距，上边距，宽，高
        pokerLabel.setGeometry(QRect(0, 0, 800, 30))
        # 设置文本标签的字体和大小，粗细等
        pokerLabel.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))
        self.pokerNumLabel = QLabel(self)
        # 设置标签的左边距，上边距，宽，高
        self.pokerNumLabel.setGeometry(QRect(0, 25, 800, 30))
        # 设置文本标签的字体和大小，粗细等
        self.pokerNumLabel.setFont(QtGui.QFont("Roman times", 15, QtGui.QFont.Bold))

    def windowListener(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hWnd)
        fgWnd = win32gui.GetForegroundWindow()

        self.move(left - self.width, top - 80)
        if fgWnd != self.hWnd and fgWnd != self.selfWnd:  # 不是顶层
            if not self.isTopWin:
                # 隐藏
                win32gui.SetWindowPos(self.selfWnd, win32con.HWND_BOTTOM, left - self.width, top - 80, self.width,
                                      self.height,
                                      win32con.SWP_SHOWWINDOW)
                self.isTopWin = True
        else:
            if self.isTopWin:
                self.isTopWin = False
                # 置顶
                win32gui.SetWindowPos(self.selfWnd, win32con.HWND_TOPMOST, left - self.width, top - 80, self.width,
                                      self.height,
                                      win32con.SWP_SHOWWINDOW)

    def showWin(self):
        self.show()
        self.selfWnd = win32gui.FindWindow(None, "CV记牌器日志")
