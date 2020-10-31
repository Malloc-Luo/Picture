# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np
import imageio as imgio
import math
from numpy import fft
from os import system
from show import show, run_log



_ImgPath = {'2-1': 'SrcImgs/blur3.jpg',
            '2-2': 'SrcImgs/sadhna_53_45.bmp',
            '2-3': 'SrcImgs/telescope.bmp' }


def inverse(input, PSF, eps): 
    """
     逆滤波
    :param input: np.array, image array
    :param PSF: np.array, point spread function
    :param eps: float, 平均噪声功率
    :return: np.array
    """      
    input_fft = fft.fft2(input) - eps
    PSF_fft = fft.fft2(PSF)
    result = fft.ifft2(input_fft / PSF_fft) #计算F(u,v)的傅里叶反变换
    result = np.abs(fft.fftshift(result))
    return result


# 维纳滤波
def Wiener(src,  PSF, esp, K=0.01):

    src_fft = np.fft.fft2(src) - esp
    PSF_fft = np.fft.fft2(PSF)
    PSF_fft_1 = np.conj(PSF_fft) / np.abs(PSF_fft)
    dst = np.fft.fft2(src_fft * PSF_fft_1)

    return np.abs(np.fft.fftshift(dst))


def normal(arr):
    arr = np.where(arr < 0, 0, arr)
    arr = np.where(arr > 255, 255, arr)
    return arr.astype(np.int16)



def get_motion_dsf(image_size, motion_angle, motion_dis, center=(-1, -1)):
    """
    生成针对运动失焦的Point spread function
    :param image_size: tuple, size of image
    :param motion_angle: float, angle of motion
    :param motion_dis: int, distance
    :param center: reference center point
    :return: np.array
    """
    assert isinstance(center, (tuple, list, set)) and len(center) == 2
    assert isinstance(center[0], (int, float)) and isinstance(center[1], (int, float))

    PSF = np.zeros(image_size)

    if center == (-1, -1):
        x_center, y_center = (image_size[0] - 1) / 2, (image_size[1] - 1) / 2
    else:
        x_center, y_center = center
 
    sin_val = math.sin(motion_angle * math.pi / 180)
    cos_val = math.cos(motion_angle * math.pi / 180)
 
    # 将对应角度上motion_dis个点置成1
    for i in range(motion_dis):
        x_offset = round(sin_val * i)
        y_offset = round(cos_val * i)
        PSF[int(x_center - x_offset), int(y_center + y_offset)] = 1
 
    return PSF / PSF.sum()


def fix_image(src, angle, dis, mode=0):
    """
    修复运动失焦图像
    :param src: input image, np.array
    :param angle: motion angle, float
    :param dis: motion distance, int
    :param mode: 0, reverse(); 1, Wiener()
    :return: np.array
    """
    psf = get_motion_dsf(src.shape, angle, dis)

    if mode == 0:
        dst = inverse(src, psf, 1e-4)
        dst = normal(dst)
    else:
        dst = Wiener(src, psf, 1e-4)
    
    return dst


@run_log
def _topic1():

    src = cv.imread(_ImgPath['2-1'], cv.IMREAD_GRAYSCALE)
    dst = fix_image(src, 1, 23, 1)
    
    #cv.imwrite('DstImgs/' + _ImgPath['2-1'].split('/')[1], dst)
    imgio.imwrite('DstImgs/' + _ImgPath['2-1'].split('/')[1], dst)
    show(src, dst)


@run_log
def _topic2():

    src = cv.imread(_ImgPath['2-2'], cv.IMREAD_GRAYSCALE)
    dst = fix_image(src, 54, 46)

    rows, cols = src.shape
    # 傅里叶变换
    f = np.fft.fft2(dst)
    fshift = np.fft.fftshift(f)
    fimg = np.log(np.abs(fshift))

    imgio.imwrite('DstImgs/' + 'fft' + _ImgPath['2-3'].split('/')[1], fimg)
    fftimg = cv.imread('DstImgs/' + 'fft' + _ImgPath['2-3'].split('/')[1], 0)
    # 构造滤波器（类似陷阱滤波器，过滤一些高频点）
    mask = cv.threshold(fftimg, 155, 255, cv.THRESH_BINARY_INV)[1]
    cv.circle(mask, (int(cols / 2), int(rows / 2)), 15, (255, 255, 255), -1)
    # 傅里叶反变换
    ishift = np.fft.ifftshift(fshift * mask)
    iimg = np.fft.ifft2(ishift)
    dst = np.abs(iimg)

    imgio.imwrite('DstImgs/' + _ImgPath['2-2'].split('/')[1], dst)
    show(src, dst)



@run_log
def _topic3():
    
    src = cv.imread(_ImgPath['2-3'], cv.IMREAD_GRAYSCALE)
    dst = fix_image(src, 42, 19, 0)

    rows, cols = src.shape

    f = np.fft.fft2(dst)
    fshift = np.fft.fftshift(f)
    fimg = np.log(np.abs(fshift))

    imgio.imwrite('DstImgs/' + 'fft' + _ImgPath['2-3'].split('/')[1], fimg)
    fftimg = cv.imread('DstImgs/' + 'fft' + _ImgPath['2-3'].split('/')[1], 0)

    mask = cv.threshold(fftimg, 175, 255, cv.THRESH_BINARY_INV)[1]
    
    cv.circle(mask, (int(cols / 2), int(rows / 2)), 14, (255, 255, 255), -1)
    #show(fimg, mask)

    ishift = np.fft.ifftshift(fshift * mask)
    iimg = np.fft.ifft2(ishift)
    dst = np.abs(iimg)

    imgio.imwrite('DstImgs/' + _ImgPath['2-3'].split('/')[1], dst)

    show(src, dst)



def main():
    _topic1()
    _topic2()
    _topic3()


if __name__ == '__main__':
    main()

