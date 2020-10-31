# -*- coding: utf-8 -*-


def show(* imgs):
    """
    :param imgs: 若干个np.array或者一个仅包含np.array的tuple, list, set等
    :return: None
    """

    import matplotlib.pyplot as plt

    if isinstance(imgs[0], (tuple, list, set)):
        from functools import reduce
        imgs = reduce(lambda x, y: x + y, imgs)

    rows = int(len(imgs) / 10 + 1)
    cols = len(imgs) if rows == 1 else 10

    plt.figure()
    for n in range(1, len(imgs) + 1):
        plt.subplot(rows, cols, n)
        plt.imshow(imgs[n - 1], cmap='gray')
        plt.xticks([n])
        plt.yticks([])
    plt.show()


# 打印日志
def run_log(f):
    def subf():
        print(__name__ + ':  ' + f.__name__ + '\n')
        return f()
    return subf


if __name__ == '__main__':
    import os
    os.system('python main.py')


