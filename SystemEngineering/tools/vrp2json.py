# -*- coding: utf-8 -*-
# 读取.vrp文件提取关键信息，转换成json文件
import json, os, re


def save_json_name(fname: str) -> str:
    if os.path.exists(fname) is True:
        split = fname.split('.')
        split[-1] = 'json'
        return '.'.join(split)
    else:
        raise FileExistsError('%s 文件不存在')


def load_json(fname: str) -> dict:
    if os.path.exists(fname) is True:
        with open(fname, 'r', encoding='utf-8') as f:
            return json.load(f)


def write_into_json(fname: str, _json: dict):
    with open(fname, 'w') as f:
        json.dump(_json, f, indent=4)


def vrp2json(fname: str) -> str:
    _jsonf = save_json_name(fname)
    _json = {'points': {}}
    vrpf = open(fname, 'r')
    line = 'vrp'
    while re.search(r'EOF', line) is None:
        line = vrpf.readline()
        # 获取需求点数量
        if re.match(r'DIMENSION\s*\:\s*(\d+)', line) is not None:
            match = re.match(r'DIMENSION\s*\:\s*(\d+)', line)
            _json['dimension'] = int(match.groups()[0])
        # 车的数量、最优值等
        elif re.search(r'COMMENT', line) is not None:
            match = re.search(r'trucks\s*\:\s*(\d+)\,\s*Optimal\s*value\s*\:\s*(\d+)', line)
            _json['trucks'] = int(match.groups()[0])
            _json['Optimal value'] = int(match.groups()[1])
        # 车辆容量
        elif re.search(r'CAPACITY', line) is not None:
            match = re.match(r'CAPACITY\s*\:\s*(\d+)', line)
            _json['capacity'] = int(match.groups()[0])
        # 记录坐标
        elif re.search(r'NODE_COORD_SECTION', line) is not None:
            for index in range(_json['dimension']):
                line = vrpf.readline()
                val = re.match(r'\s*(\d+)\s+(\d+)\s+(\d+)', line).groups()
                _json['points'][str(index)] = [int(val[1]), int(val[2])]
        # 记录需求量
        elif re.search(r'DEMAND_SECTION', line) is not None:
            for index in range(_json['dimension']):
                line = vrpf.readline()
                val = re.match(r'\s*(\d+)\s+(\d+)', line).groups()
                _json['points'][str(index)].append(int(val[1]))
    vrpf.close()
    write_into_json(_jsonf, _json)
    return _json


if __name__ == '__main__':
    vrp2json('..\\A-n32-k5.vrp')
