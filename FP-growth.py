# !usr/bin/env python
# -*-coding: utf-8
import time
from itertools import combinations


# 结点信息
class Node:
    # 初始化节点
    def __init__(self, name, count, parent):
        self.name = name  # 节点代表项的名字
        self.count = count  # 计算节点在数据库中出现的次数
        self.parent = parent  # 一个父节点信息，从下向上遍历需要
        self.childrens = []  # 多个子节点信息，生成树的时候最重要的条件
        self.item_next = None  # 指向下一个相同的节点

    # 展示节点的所有信息
    def display_node(self):
        print("节点的名字{0} 节点出现的次数{1}".format(self.name, self.count))
        # print(self.parent.name, self.childrens)

    # 展示该节点下的子树
    def display_tree(self):
        self.display_node()
        if self.childrens:
            for child in self.childrens:
                print("自己和该节点下的子节点：")
                child.display_tree()

    # 查找孩子节点中有没有该项
    def trav_child(self, item_check):
        if self.childrens:
            for child in self.childrens:
                if item_check == child.name.split()[-1:][0]:
                    return child
        return ""


# 生成频繁项集
def frequent_item(C, items_length, support):
    L = {}
    for k, v in C.items():
        if v / items_length >= support:
            L[k] = v
    return L


# Fp—tree生成
def FP_tree(text_adjustment):
    # 建立FP-tree
    global head, all_node
    ptr = head
    all_node.append(head)
    for text_ad in text_adjustment:
        fl = ptr.trav_child(text_ad)
        # 该节点已经存在
        if fl:
            fl.count += 1
            ptr = fl
        # 该节点不存在
        else:
            # 命名取前面的项名字加上自己的项的名字
            node_name = text_ad
            if ptr.parent:
                node_name = ptr.name + ' ' + node_name
            # 产生一个新的节点并且把它存入列表
            node_name = Node(node_name, 1, ptr)
            for it in range(len(all_node) - 1, -1, -1):
                if all_node[it].name.split()[-1:] == node_name.name.split()[-1:]:
                    all_node[it].item_next = node_name
                    break
            all_node.append(node_name)
            ptr.childrens.append(node_name)
            # 项表头结点
            global item_table
            for key, value in item_table.items():
                if all(item_table.values()):
                    break
                if node_name.name.split()[-1:][0] == key:
                    if value is None:
                        item_table[key] = node_name

                    break

            ptr = node_name


# key为项的名字，value为项表的第一个节点
# 条件模式基
def conditional_patterns_set(item__k, item__v, ):
    cpb = {}
    ptr = item__v
    count = item__v.count
    # print("count:",count)
    base = []
    if ptr.parent.childrens and ptr.parent.name != 'head':
        ptr = ptr.parent
        while ptr.name != 'head' and ptr:
            # print("ptrrr:",ptr,ptr.name)
            # print("ptr:",ptr.name,',',ptr.count)
            base.append(ptr.name)
            # print("ptr:",ptr,ptr.name)
            ptr = ptr.parent
        cpb[tuple(base)] = count
    while item__v.item_next is not None:
        # print('item_next:',item__v.item_next.name,',',item__v.item_next.count)
        base = []
        item__v = item__v.item_next
        ptr = item__v
        count = item__v.count
        if ptr.parent and ptr.parent.name != 'head':
            ptr = ptr.parent
            while ptr.name != 'head' and ptr:
                base.append(ptr.name)
                ptr = ptr.parent
            cpb[tuple(base)] = count
    return cpb


# 条件模式树
def conditional_pattern_tree(item_table_set):
    global item_table
    head = Node("head", 1, None)
    item_name = {}  # 项头表
    for item_key in item_table.keys():
        item_name[item_key] = None
    part_node = []
    for item_ta_set, value in item_table_set.items():
        ptr = head
        part_node.append(head)
        for item_ta_set_single in item_ta_set[len(item_ta_set) - 1::-1]:
            item_ta_set_single = item_ta_set_single.split()[-1]
            find = ptr.trav_child(item_ta_set_single)
            if find:
                # print("find:", find.name)
                find.count += value
                ptr = find
            else:
                node_name = Node(item_ta_set_single, value, ptr)
                for it in range(len(part_node) - 1, -1, -1):
                    if part_node[it].name.split()[-1:] == node_name.name.split()[-1:]:
                        part_node[it].item_next = node_name
                        break
                part_node.append(node_name)
                ptr.childrens.append(node_name)
                for key1, value1 in item_name.items():
                    if all(item_name.values()):
                        break
                    if node_name.name.split()[-1:][0] == key1:
                        if value1 is None:
                            item_name[key1] = node_name
                        break
                ptr = node_name
    # head.display_tree()
    # for node in part_node:
    #     print("node:", node.name, node.count)
    # 删除项头表中为空的项
    delete = []
    for key, value in item_name.items():
        if value is None:
            delete.append(key)
    for de in delete:
        item_name.pop(de)
    # for key, value in item_name.items():
    #     print(key, value.count)
    return item_name, head, part_node


def FP_growth(item_table1, paramater=None):
    global LL
    for item_k, item_v in list(item_table1.items())[::-1]:
        if paramater:
            # print("compare:", item_k, paramater.split()[0])
            if item_k != paramater.split()[0]:
                continue
        # print("item_v:", item_v.name, item_v.count)
        # 条件模式基
        item_table_set = conditional_patterns_set(item_k, item_v)
        # print("条件模式基：", item_table_set)
        # 条件模式树 
        item_table_tree, single_road, nodes = conditional_pattern_tree(item_table_set)
        # print("条件模式树：", item_table_tree)

        new_item = item_k
        # print("paramater:", paramater)
        if paramater:
            # for pre in item_table_tree.values():
            #     print("pre.name:", pre.name, paramater)
            #                 if pre.name == paramater.split()[0]:
            #                     print("para.parent:", pre.parent.name)
            new_item = paramater
        # print("new_item:", new_item)

        if item_table_set is None:
            continue
        flag = 0
        # 通过节点的孩子的个数来判断是不是单路径
        while single_road.childrens:
            if len(single_road.childrens) == 1:
                single_road = single_road.childrens[0]
            else:
                flag = 1
                break
        # 单路径
        if flag == 0:
            delete = []
            for it_k, it_v in list(item_table_tree.items())[::-1]:
                if it_v.count / items_length < support:
                    delete.append(it_k)
            for de in delete:
                item_table_tree.pop(de)
            for i in range(1, len(item_table_tree) + 1):
                # print("list:", list(item_table_tree)[::-1])
                for com in combinations(list(item_table_tree)[::-1], i):

                    pro = ' '.join(com) + ' ' + new_item
                    # print("pro:", pro)
                    mini = 0
                    for mi in list(item_table_tree)[::-1]:
                        if mi == com[0]:
                            mini = item_table_tree[mi].count
                    # print("mini:", mini)
                    for co in com:
                        if item_table_tree[co].count < mini:
                            mini = item_table_tree[co].count
                    if pro in LL.keys():
                        LL[pro] += mini
                    else:
                        LL[pro] = mini

        else:
            # 并集
            bing_set = {}
            bing_set_copy = {}
            for tr in nodes:
                if tr.name != 'head':
                    if tr.name in bing_set.keys():
                        bing_set[tr.name] += tr.count
                    else:
                        bing_set[tr.name] = tr.count
            delete = []
            for it_k, it_v in bing_set.items():
                if it_v / items_length < support:
                    delete.append(it_k)
            for de in delete:
                bing_set.pop(de)
            for ta_k in item_table_tree:
                if ta_k in bing_set.keys():
                    bing_set[ta_k] = bing_set.pop(ta_k)
            for bing_key, bing_value in bing_set.items():
                bing_key_change = bing_key + ' ' + new_item
                bing_set_copy[bing_key_change] = bing_set[bing_key]
            LL.update(bing_set_copy)

            for bing in list(bing_set_copy)[::-1]:
                # print("bing:", bing,',',bing_set_copy[bing])
                FP_growth(item_table_tree, bing)


if __name__ == '__main__':
    start = time.time()
    count = 0
    with open("retail.dat", 'r', encoding='ANSI') as f:
        text = f.read()
        f.close()
    text = text.split('\n')
    # print(text)
    items_length = len(text)
    for i in range(items_length):
        text[i] = text[i].strip(' ')
    # text里面的内容为数据库
    # 生成候选项集
    C = {}
    for item in text:
        text1 = item.split()
        for i in text1:
            if i not in C.keys():
                C[i] = 1
            else:
                C[i] += 1
    support = eval(input("请输入支持度："))
    print(items_length)
    # 生成频繁项集
    L = frequent_item(C, items_length, support)
    count += len(L)
    # 按降序重新排序物品集
    L = dict(sorted(L.items(), key=lambda item: item[1], reverse=True))
    print(L)
    text_adjustment = []
    all_node = []
    head = Node("head", 1, None)  # 头结点
    # 项头表
    item_table = {}
    for k in L.keys():
        item_table[k] = None
    LL = {}
    # 根据物品集重新调整物品清单
    for i in range(items_length):
        text_adjustment.append([])
        for single in L.keys():
            if single in text[i].split():
                text_adjustment[i].append(single)
        # 生成FP-tree
        FP_tree(text_adjustment[i])
    while [] in text_adjustment:
        text_adjustment.remove([])
    # print("text_adjustment:", text_adjustment)
    # print("table:", item_table)
    # 展示所有节点信息
    # for all_no in all_node:
    #     if all_no != head:
    #         all_no.display_node()
    FP_growth(item_table)
    print("LL", LL)
    counter = {}
    for ll_k, ll_v in LL.items():
        for i in range(1, 15):
            if len(ll_k.split()) == i:
                if i in counter.keys():
                    counter[i] += 1
                else:
                    counter[i] = 1
                break
    print("每个频繁项出现的次数：",end='')
    for co_va in counter.values():
        count += co_va
    print(counter)
    print("sum:", count)
    end = time.time()
    print(end - start)
