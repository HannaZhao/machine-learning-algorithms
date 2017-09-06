# -*- coding: utf-8 -*-

import math

# ***** 创建kdtree *****
# 思路：
# 1、首先选取第一个维度，在该维度上选取中位数对应的坐标作为根结点，小于中位数的划分到左子区域，大于中位数划分到右边
# 2、循环选取下一个维度（也可以选方差最大的那个维度，方差最大数据波动越大，越不属于同一空间），对子区域进行相同操作
# 3、重复2直到两个子区域都没有实例为止
class kdnode(object):
    def __init__(self, point=None, left=None, right=None, split_axis=None):
        self.point = point
        self.left = left
        self.right = right
        self.split_axis = split_axis
def create(points, axis=0):
    # 为空判断
    if len(points) == 0:
        return None

    # check dimension略过
    dim = len(points[0])

    # 切分维度选下一个维度
    # 结点为切分维度上的中位数对应坐标
    point_list = list(points)
    point_list.sort(key=lambda point:point[axis])
    median = len(point_list)/2
    next_axis = (axis+1)%dim
    left = create(point_list[:median], next_axis)
    right = create(point_list[median+1:], next_axis)
    return kdnode(point_list[median], left, right, axis)

# ***** kdtree搜索 *****
# 思路：
# 1、递归遍历到叶结点，当前维度小于切分点往左，大于切分点往右
# 2、递归过程：若k近邻列表不足k个则加入列表；若有k个，若当前结点比列表中任一点距离目标点近，则将列表中最远点替换
# 3、回溯：若k近邻列表不足k个，则递归搜索另一区域；若有k个，查看当前结点划分的区域当中，目标结点不在的区域是否与当前k近邻区域相交，相交则递归搜索该区域
def search_nearest(kdnode, point, min=[], k=1):
    # 树为空判断
    if kdnode is None:
        return min
    # 加入list原则：当前点距离小于list中最大距离；len(list)<k
    if len(min) < k:
        min.append(kdnode.point)
    elif cal_dist(kdnode.point, point) < max_dist(min, point):
        index = max_index(min, point)
        min[index] = kdnode.point

    # 从根结点递归访, 当前维度小于划分点则左移，大于则右移
    axis = kdnode.split_axis
    if point[axis] < kdnode.point[axis]:
        min = search_nearest(kdnode.left, point, min, k)
    else:
        min = search_nearest(kdnode.right, point, min, k)

    # 判断另一区域是否需要遍历：另一区域是否与当前k近邻区域相交; len(list)<k
    if abs(kdnode.point[axis] - point[axis]) < max_dist(min, point) or len(min) < k:
        if point[axis] < kdnode.point[axis]:
            min = search_nearest(kdnode.right, point, min, k)
        else:
            min = search_nearest(kdnode.left, point, min, k)
    return min
def cal_dist(p1, p2):
    distance = 0
    for i in range(len(p1)):
        distance += (p1[i] - p2[i])**2
    return math.sqrt(distance)
def max_index(mins, point):
    tmp = mins
    tmp.sort(key=lambda p:cal_dist(p, point), reverse=True)
    return mins.index(tmp[0])
def max_dist(mins, point):
    distances = []
    for p in mins:
        distances.append(cal_dist(p, point))
    return max(distances)

# ***** 测试 *****
# 前序遍历,检查树是否创建正确
def pre_print(kdtree):
    if kdtree is None:
        return
    print(kdtree.point)
    pre_print(kdtree.left)
    pre_print(kdtree.right)
# 原始版本KNN, 找出k近邻点
def KNN_without_kd(points, point, k=1):
    distances = {}
    for p in points:
        distances[p] = cal_dist(p, point)
    sorteddist = sorted(distances.items(), key=lambda d:d[1])
    kmins = []
    for i in range(k):
        kmins.append(sorteddist[i][0])
    return kmins

if __name__ == '__main__':
    ps = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7,2)]
    kdtree = create(ps)
    pre_print(kdtree)
    point = (4, 4)
    min = search_nearest(kdtree, point, k=4)
    print('the nearest point in kd tree')
    print(min)
    print('the nearest point in knn')
    print(KNN_without_kd(ps, point, 4))