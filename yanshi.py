#!/usr/bin/python
# coding:utf-8

"""
@author: css
@software: PyCharm
@file: yanshi.py
@time: 2021/3/5 17:36:46
"""
import win32gui, win32ui, win32con
import cv2
import numpy as np


def screen():
    hWnd = win32gui.FindWindow(None, "欢乐斗地主")
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 窗口隐藏或最小化，无法截图
    if top < 0:
        return None
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
    # 保存截图
    # saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
    signedIntsArray = saveBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, np.uint8)
    img.shape = (height, width, 4)
    # 保存bitmap到内存设备描述表
    img = cv2.resize(img, (1040, 629), interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    # cv2.imwrite('screen.png', img)
    # 返回一张可以给opencv 使用的图片
    return img


# 模板匹配方法
def matchImgNum(bgImg, templeteImg, threshold=0.92):
    '''
    bgImg：截图出来的底片
    templeteImg；模板图片
    threshold：对比精确度
    '''
    res = cv2.matchTemplate(bgImg, templeteImg, cv2.TM_CCOEFF_NORMED)
    tt = bgImg.copy()
    w, h = templeteImg.shape[::-1]
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
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(tt, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                cv2.imwrite('res223.png', tt)
            last = point
    return num


# 调用截图方法，获取截图结果
img = screen()
# 转为灰色通道的图片，截取自己的出牌区域
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[350:622, 10:1042]

# 读取 模板， 扑克4
temp = cv2.imread('templete/fangkuai_10.png', 0)
num = matchImgNum(img, temp, 0.85)
print('匹配出结果', num)
