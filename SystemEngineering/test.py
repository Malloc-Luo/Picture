# -*- coding: utf-8 -*-
# 仿真测试文件
# 同时开启五个进程仿真同一组数据

from multiprocessing import Process, Pool, freeze_support, Queue
from threading import Thread


def test_ga(*argv):
    from algorithm.Problem import Problem
    from algorithm.Data import Data
    import time

    print('start: ', argv)
    data = Data('data\\E-n22-k4.vrp')
    p = Problem(data, argv[0], argv[1], argv[2])
    start = time.time()
    p.solve()
    end = time.time()
    print("cost time: %.1f" % (end - start))
    print("iters: %d, popsize: %d, threshold: %d\n" %
          (argv[0], argv[1], argv[2]))



if __name__ == '__main__':
    freeze_support()
    pool = Pool(5)
    params = [(600, 200, 8), (600, 200, 8), (600, 200, 8), (600, 200, 8), (600, 200, 8)]

    for _p in params:
        pool.apply_async(test_ga, args=(_p[0], _p[1], _p[2]))

    print('start....')
    pool.close()
    pool.join()
    print('end....')
