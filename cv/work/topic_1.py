# -*- coding : utf-8 -*-
# 第一题脚本文件
import cv2 as cv
import numpy as np
from show import show, run_log
from os import system

_ImgPath = {'1-1': 'SrcImgs/Circuit_noise.jpg', 
            '1-2': 'SrcImgs/boy_noisy.gif',
            '1-3': 'SrcImgs/california_22_13.bmp'}


@run_log
def _topic1():
    ## 中值滤波
    src = cv.imread(_ImgPath['1-1'], cv.IMREAD_COLOR)
    dst = cv.medianBlur(src, 5)
    cv.imwrite('DstImgs/' + _ImgPath['1-1'].split('/')[1], dst)
    show(src, dst)



# 陷阱滤波器去除正弦噪声
@run_log
def _topic2():
    from PIL import Image, ImageSequence
    import imageio
    # 读取GIF格式图片，转换成numpy数组
    src = [cv.cvtColor(np.array(frame), cv.COLOR_RGB2BGR) for frame in ImageSequence.Iterator(Image.open(_ImgPath['1-2']))]
    src = [cv.cvtColor(sub, cv.COLOR_BGR2GRAY) for sub in src]

    dst = []
    dft_shift = []
    mask = []

    # 对每一帧图像进行傅里叶变换
    for img in src:
        dft = np.fft.fft2(img)
        fshift = np.fft.fftshift(dft)
        dft_shift.append(fshift)
        mask.append(np.log(np.abs(fshift)))

    rows, cols = src[0].shape
    # 滤波器半径
    R = 30
    # 设置滤波器
    for index in range(len(mask)):

        imageio.imwrite('DstImgs/fft' + str(index) + '.jpg', mask[index])
        mask[index] = cv.imread('DstImgs/fft' + str(index) + '.jpg', 0)
        # 频域图谱二值化，找出频率最高的几个点，变换后的图像作为滤波器
        mask[index] = cv.threshold(mask[index], 200, 255, cv.THRESH_BINARY_INV)[1]
        # 覆盖图像固有区域，保留细节部分
        cv.circle(mask[0], (int(rows / 2), int(cols / 2)), R, (255, 255, 255), -1)
    
    # 傅里叶反变换
    for f_s in dft_shift:
        ishift = np.fft.ifftshift(f_s * mask[0])
        iimg = np.fft.ifft2(ishift)
        dst.append(np.abs(iimg))

    imageio.mimsave('DstImgs/' + _ImgPath['1-2'].split('/')[1], dst, duration=0.1)
    show(dst)



@run_log
def _topic3():
    ## 高斯滤波
    src = cv.imread(_ImgPath['1-3'], cv.IMREAD_COLOR)
    dst = cv.GaussianBlur(src, (3, 3), 0)
    #dst = cv.bilateralFilter(src, 9, 75, 95)
    cv.imwrite('DstImgs/' + _ImgPath['1-3'].split('/')[1], dst)
    show(src, dst)
    cv.waitKey(0)


def main():
    _topic1()
    _topic2()
    _topic3()
    
    
if __name__ == '__main__':
#    print('跳转到main.py\n')
#    system('python main.py')
    main()    
