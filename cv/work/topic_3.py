# -*- coding: utf-8 -*-

import cv2 as cv 
import numpy as np
from show import show, run_log

_ImgPaths = {'3-1': 'SrcImgs/plane.bmp',
             '3-2': 'SrcImgs/Wirebond.tif',
             '3-3-1': 'SrcImgs/coins.png',
             '3-3-2': 'SrcImgs/Dowels.tif',
             '3-3-3': 'SrcImgs/rice.png' }

src1 = cv.imread(_ImgPaths['3-3-1'], 1)
src2 = cv.imread(_ImgPaths['3-3-2'], 1)
src3 = cv.imread(_ImgPaths['3-3-3'], 1)
 

def _process_img(src, blurKernel=2, threshold=(120, 255), cannyThre=(90, 10), dilaKernel=2, srcCopy=None):
    """
    :param src: np.array, source image
    :param blurKernel: int, blur kernel size, default is 2
    :param threshold: tuple, binary threshold
    :param cannythre: tuple, canny
    :param dilaKernel: int, dilate kernel size
    :param srcCopy: np.array, source copy image
    :return: np.array
    """

    assert isinstance(threshold, (tuple, list)) and isinstance(cannyThre, (tuple, list))
    assert len(threshold) == 2 and len(cannyThre) == 2

    if type(srcCopy) == type(None):     
        srcCopy = src
    # 掩膜
    mask = np.zeros(src.shape, np.uint8)
    # 均值滤波去噪
    dst = cv.blur(src, (blurKernel, blurKernel))
    # 阈值化图像
    ret, dst = cv.threshold(dst, threshold[0], threshold[1], cv.THRESH_BINARY_INV)
    # Canny算子边缘检测
    dst = cv.Canny(dst, cannyThre[0], cannyThre[1], 3)
    # 膨胀
    kernel = np.ones((dilaKernel, dilaKernel), np.uint8)
    dst = cv.dilate(dst, kernel)
    # 轮廓查找
    contour, hierarchy = cv.findContours(dst, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    objCnt = 0

    # 将外轮廓绘制在掩膜上，用于图像分割
    for index in range(0, len(contour)):
        if hierarchy[0][index][3] == -1:
            cv.drawContours(mask, contour, index, (255, 255, 255), cv.FILLED)
            objCnt += 1

    dst = mask * srcCopy
    cv.putText(dst, 'find ' + str(objCnt) + ' objects', (30, 40), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
    print('find ' + str(objCnt) + ' objects')

    return dst


@run_log
def topic3():
    global src1, src2, src3
    # 图一
    dst1 = _process_img(src1)
    # 图二，先对图像进行腐蚀处理，尽量分离两物体边缘交界出，便于后续边缘检测
    dst2 = cv.erode(src2, np.ones((8, 8), np.uint8))
    dst2 = _process_img(dst2, blurKernel=5, threshold=(110, 255), cannyThre=(150, 100), dilaKernel=5, srcCopy=src2)
    # 图三
    dst3 = cv.erode(src3, np.ones((3, 3), np.uint8))
    dst3 = _process_img(dst3, blurKernel=4, threshold=(110, 255), cannyThre=(90, 10), dilaKernel=2, srcCopy=src3)

    cv.imwrite('DstImgs/' + _ImgPaths['3-3-1'].split('/')[1], dst1)
    cv.imwrite('DstImgs/' + _ImgPaths['3-3-2'].split('/')[1], dst2)
    cv.imwrite('DstImgs/' + _ImgPaths['3-3-3'].split('/')[1], dst3)

    show(src1, dst1)
    show(src2, dst2)
    show(src3, dst3)


def main():
    topic3()
    

if __name__ == '__main__':
    from os import system
#    system('python main.py')
    topic3()
