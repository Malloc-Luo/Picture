# -*- coding: utf-8 -*-
from algorithm.Problem import Problem
from algorithm.Data import Data


# 读取VRP问题数据，参数为标准实例库的.vrp文件
data = Data('data\\E-n22-k4.vrp')

# 初始化VRP问题求解器对象，参数为Data
ngen, popsize = 400, 200
problem = Problem(data, ngen=ngen, popsize=popsize)
# 打印日志
problem.set_verbose(True)

# 调用solve求解
problem.solve()
