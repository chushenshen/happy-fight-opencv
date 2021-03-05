#!/usr/bin/python
# coding:utf-8

"""
@author: css
@software: PyCharm
@file: screen.py
@time: 2021/3/3 21:50:29
"""
import win32gui, win32ui, win32con
import cv2
import numpy as np


def screen(hWnd):
    # print(hWnd)
    # hWnd = win32gui.FindWindow("Chrome_WidgetWin_0", "欢乐斗地主")
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 窗口隐藏，无法截图
    if top < 0:
        return None
    # win32gui.SetWindowPos(QQWin,win32con.HWND_TOPMOST,x, y, 300, 300, win32con.SWP_SHOWWINDOW)
    # print(width, height)
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")

    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    # 保存bitmap到内存设备描述表
    img = cv2.resize(img, (1040, 629), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    # cv2.imwrite('screen.png', img)
    return img
# 欢乐斗地主记牌器