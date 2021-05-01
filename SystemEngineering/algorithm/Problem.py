# -*- coding: utf-8 -*-
import numpy as np
import random
import deap
from deap import creator, base, tools, algorithms
import copy
import time

if __name__ == '__main__':
    from Data import Data
    from Tsp import TSP
else:
    from algorithm.Data import Data
    from algorithm.Tsp import TSP


class Problem(object):
    """ VRP问题求解类\n
    Args:
        data: Data类
        ngen: 遗传进化代数
        popsize: 种群大小
    """
    def __init__(self, data: Data, ngen=350, popsize=120, threshold=8):
        self._data = data
        self.vrp_node = data.get_pair_points()
        self.vrp_demand = data.get_demands()
        self.vrp_trucks = data.get_trucks()
        self.vrp_capacity = data.get_capacity()
        self.vrp_points = data.get_points()
        self._distanceMap = data.generate_distance_matrix()
        self.lind = data.get_dimension() + self.vrp_trucks
        self.verbose = False
        # 动态规划使用的分界
        self.threshold = threshold
        # 初始种群大小
        self.popSize = popsize
        # 迭代次数、交叉概率、突变概率 默认参数
        self.ngen, self.cxpb, self.mutpb = ngen, 0.8, 0.2
        self.resultChrom = None
        # 定义问题
        creator.create('FitnessMin', base.Fitness, weights=(-1.0, ))
        creator.create('Individual', list, fitness=creator.FitnessMin)

    def set_params(self, ngen: int, cxpb: float, mutpb: float):
        """ 设置参数：迭代次数  交叉概率  突变概率"""
        self.ngen, self.cxpb, self.mutpb = int(ngen), float(cxpb), float(mutpb)

    def set_verbose(self, verbose=True):
        self.verbose = verbose

    def genarate_chrom(self) -> list:
        """ 生成种群染色体，格式为 [0, 1, 2, 3, 0, 4, 5, 0]\n
        上述染色体表示的路径为： 0->1->2->3->0  0->4->5->0\n
        其中0代表仓库。注意染色体开头和结尾必须为0，其余的随机分布在中间，且不相连\n
        Args:
            scale: 种群规模，也就是染色体数量
        Return:
            种群组成的集合
        """
        return self._generate_single_chrom()

    def _generate_single_chrom(self) -> list:
        basePath = [i for i in range(1, self._data.get_dimension())]
        random.shuffle(basePath)
        # 首位插入0
        basePath.insert(0, 0), basePath.append(0)
        while len(basePath) < self.lind:
            pos = random.randint(2, len(basePath) - 2)
            if basePath[pos] != 0 and basePath[pos - 1] != 0:
                basePath.insert(pos, 0)
        return basePath

    def decode_chrom(self, chrom: list) -> list:
        _path = np.array(chrom, dtype=np.int32)
        depot = [val[0] for val in np.argwhere(_path == 0)]
        return [chrom[depot[i]: depot[i + 1] + 1] for i in range(len(depot) - 1)]

    def encode_chrom(self, path: list) -> list:
        """ decode_chrom的逆过程 """
        chrom = []
        for _path in path:
            _path.pop()
            chrom.extend(_path)
        chrom.append(0)
        return chrom

    def calc_path_cost(self, _path: list) -> float:
        """ 计算给定路径的长度\n
        Args:
            _path: 解码得到的路径，例如[0, 1, 2, 3, 0]
        Return:
            路径的总长度，查表得到的
        """
        cost = 0
        for index in range(len(_path) - 1):
            cost += self.calc_point_distance(_path[index], _path[index + 1])
        return cost

    def calc_point_distance(self, _p1: int, _p2: int) -> float:
        return self._distanceMap[_p1][_p2]

    def calc_punishment(self, _path: list) -> float:
        """ 计算超重惩罚，给一个比较大的值筛选下去
        """
        # 惩罚系数，非常非常大
        punishmentRatio = 1000000
        demand = sum([self.vrp_demand[_p] for _p in _path])
        return punishmentRatio * max(demand - self.vrp_capacity, 0)

    def eval_func(self, chrom: list) -> float:
        """ 适度函数，Reference:\n
        评价函数由 cost和punsihment组成，cost是每条路径的花费，punishment是惩罚，
        如果需求量大于一辆汽车的容量就给予惩罚
        """
        evaluateValue = 0
        path = self.decode_chrom(chrom)
        evaluateValue = sum([self.calc_path_cost(_path) + self.calc_punishment(_path) for _path in path])
        return (evaluateValue),

    def generate_child(self, chrom1: list, chrom2: list, iters=10) -> list:
        """ 交叉，生成子个体\n
        参考《基于电动汽车的带时间窗的路径优化问题研究》\n
        Args:
            chrom1: 父染色体1
            chrom2: 父染色体2
            iters: 生成的个体数量，在个体里面选择代价最小的
        Return:
            最佳子代
        """
        path1 = self.decode_chrom(chrom1)
        # 作为子代的头部
        subPathHead = path1[random.randint(0, len(path1) - 1)]
        unvisited = set(chrom1) - set(subPathHead)
        unvisitedPoint = [digit for digit in chrom2 if digit in unvisited]
        # numOfPath = len(path1) - 1
        # 被选中的子代路径
        selectedSubPath = None
        # 评估函数的评估值，默认为无限大
        fitness = np.inf
        # 生成10组子路径，选择最优的一组
        for _ in range(iters):
            subPathBody = copy.deepcopy(unvisitedPoint)
            subPathBody.insert(0, 0), subPathBody.append(0)
            # 随机插入0
            while len(subPathBody) < len(chrom1) - len(subPathHead) + 1:
                pos = random.randint(2, len(subPathBody) - 2)
                if subPathBody[pos] != 0 and subPathBody[pos - 1] != 0:
                    subPathBody.insert(pos, 0)
            _subPathFitness = self.eval_func(subPathBody)[0]
            # 更新最适路径和最适值
            if _subPathFitness < fitness:
                selectedSubPath = copy.deepcopy(subPathBody)
                fitness = _subPathFitness
        # 删除开头的0，与选中的头拼接
        selectedSubPath.pop(0)
        selectedSubPath = subPathHead + selectedSubPath
        return selectedSubPath

    def crossover(self, chrom1: list, chrom2: list) -> tuple:
        """ 交叉
        """
        chrom1[:], chrom2[:] = self.generate_child(chrom1, chrom2), self.generate_child(chrom2, chrom1)
        return chrom1, chrom2

    def sub_problem_tsp_slover(self, path: list) -> list:
        """ 对于子问题TSP问题的动态规划求解
        参数为输入的path，输出为优化求解后的path
        """
        # 将所有的点打包成一个字典作为参数
        _pointd = {}
        for _p in path:
            _pointd[str(_p)] = self.vrp_points[str(_p)][:2]
        return TSP.opt(_pointd, self.threshold)

    def mutation(self, chrom: list) -> list:
        """ 突变操作
        """
        path = self.decode_chrom(chrom)
        optimized = []
        for _path in path:
            optimized.append(self.sub_problem_tsp_slover(_path))
        chrom[:] = self.encode_chrom(optimized)
        return chrom,

    def solve(self):
        """ 问题求解使用deap库，参考：
        https://deap.readthedocs.io/en/master/
        """
        self._toolbox = base.Toolbox()
        self._toolbox.register('individual', tools.initIterate, creator.Individual, self.genarate_chrom)
        self._toolbox.register('population', tools.initRepeat, list, self._toolbox.individual)
        self._toolbox.register('evaluate', self.eval_func)
        self._toolbox.register('select', tools.selTournament, tournsize=2)
        self._toolbox.register('mate', self.crossover)
        self._toolbox.register('mutate', self.mutation)
        # 初始种群大小
        self._toolbox.popSize = self.popSize
        self._pop = self._toolbox.population(self._toolbox.popSize)
        # 迭代数据
        self._statistic = tools.Statistics(key=lambda individ: individ.fitness.values)
        self._statistic.register('Minimize', np.min)
        self._statistic.register('Average', np.mean)
        self._hall = tools.HallOfFame(maxsize=1)
        # 迭代次数
        self._toolbox.ngen, self._toolbox.cxpb, self._toolbox.mutpb = self.ngen, self.cxpb, self.mutpb
        pop, logbook = algorithms.eaMuPlusLambda(self._pop, self._toolbox,
            mu=self._toolbox.popSize,
            lambda_=self._toolbox.popSize,
            cxpb=self._toolbox.cxpb,
            mutpb=self._toolbox.mutpb,
            ngen=self._toolbox.ngen,
            stats=self._statistic,
            halloffame=self._hall,
            verbose=self.verbose)
        self._data.plot_path(self._hall.items[0])
        self.display_result()
        return pop, logbook

    def display_result(self):
        bestChrom = self._hall.items[0]
        path = self.decode_chrom(bestChrom)
        cost = bestChrom.fitness.values[0]
        print(path)
        print([self.calc_load(_path) for _path in path])
        print('最小花费：', cost, "\t误差：", (cost - self._data.get_optimize_value()) * 100 / self._data.get_optimize_value(), '%')

    def calc_load(self, _path: list) -> float:
        return sum([self.vrp_demand[_p] for _p in _path])


if __name__ == "__main__":
    p = Problem(Data('../A-n32-k5.vrp'))
    p.set_params(ngen=500)
    p.solve()
