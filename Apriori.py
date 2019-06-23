# !/usr/bin/env python
# -*-coding: utf-8
from itertools import combinations
import time


# 生成频繁项集
def frequent_item(C, items_length, support):
    L = {}
    for k, v in C.items():
        if v / items_length >= support:
            L[k] = v
    return L


# 有剪枝算法的候选项集的生成
def candidate_item(L, text, item_num):
    C = {}
    # 初始化候选项集
    for k1 in L.keys():
        k1_split = k1.split()
        for k2 in L.keys():
            k2_split = k2.split()
            if k1 == k2:
                continue
            if k1_split[0:-1] == k2_split[0:-1]:
                if ' '.join(k2_split + k1_split[-1:]) in C.keys():
                    continue
                k = ' '.join(k1_split + k2_split[-1:])
                C[k] = 0
    # 剪枝
    delete_list = []
    for items in C.keys():
        items_split = items.split()
        for com in combinations(items_split, item_num):
            com = ' '.join(com)  # 求组合之后是一个集合，将其转换为字符串
            if com not in L.keys():
                for de_items in C.keys():
                    de_items_split = de_items.split()
                    if set(de_items_split) > set(com.split()):
                        if de_items_split not in delete_list:
                            delete_list.append(de_items_split)
    for de in delete_list:
        de = ' '.join(de)
        C.pop(de)
    # 遍历数据库
    for text_line in text:
        # 以空格分割为两个list，是否是包含关系
        text_split = text_line.split(' ')
        for C_key in C.keys():
            key_split = C_key.split(' ')
            if set(key_split) <= set(text_split):
                C[C_key] += 1
    return C


# 没有剪枝算法的候选项集生成
def no_cut_candidate_item(L, text):
    C = {}
    # 初始化候选项集
    for k1 in L.keys():
        for k2 in L.keys():
            if k1 != k2:
                if k2 + ' ' + k1 in C.keys():
                    continue
                C[k1 + ' ' + k2] = 0
    # 遍历数据库，每个key如果存在于数据库中对应的value就加一
    for text_line in text:
        # 以空格分割为两个list，是否是包含关系
        text_split = text_line.split(' ')
        for C_key in C.keys():
            key_split = C_key.split(' ')
            if set(key_split) <= set(text_split):
                C[C_key] += 1
    return C


if __name__ == '__main__':
    time_start = time.time()
    count=0
    with open("retail.dat", 'r', encoding='ANSI') as f:
        text = f.read()
        f.close()
    text = text.split('\n')
    #print(text)
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
    # 生成频繁项集
    L = frequent_item(C, items_length, support)
    count+=len(L)
    print('C1:', C, sep='')
    print('L1:', L, sep='')
    item_num = 1
    while L != {}:
        if (item_num == 1):
            C = no_cut_candidate_item(L, text)
        else:
            C = candidate_item(L, text, item_num)
        item_num += 1
        print('C', item_num, ':', C, sep="")
        print("C的长度：", len(C))
        L = frequent_item(C, items_length, support)
        print('L', item_num, ':', L, sep="")
        count+=len(L)
        print('L的长度：', len(L))
    time_end = time.time()
    print("sum:",count)
    print(time_end - time_start)
