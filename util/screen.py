#!/usr/bin/python
# coding:utf-8

"""
@author: css
@software: PyCharm
@file: screen.py
@time: 2021/3/3 21:50:29
"""
import win32api
import win32gui, win32ui, win32con
import cv2
import numpy as np


def screen(hWnd):
    # print(hWnd)
    # hWndDC = win32gui.FindWindow("Chrome_WidgetWin_0", "欢乐斗地主")
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 窗口隐藏，无法截图
    if top < 0:
        return None
    r = win32gui.GetWindowRect(hWnd)
    hwin = win32gui.GetDesktopWindow()
    # 图片最左边距离主屏左上角的水平距离
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    # 图片最上边距离主屏左上角的垂直距离
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(srcdc, r[2] - r[0], r[3] - r[1])
    memdc.SelectObject(saveBitMap)
    memdc.BitBlt((-r[0], top - r[1]), (r[2], r[3] - top), srcdc, (left, top), win32con.SRCCOPY)
    # bmp.SaveBitmapFile(memdc, bmpFileName)

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    # 保存bitmap到内存设备描述表
    img = cv2.resize(img, (1040, 629), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    # cv2.imwrite('screen.png', img)
    return img
# 欢乐斗地主记牌器