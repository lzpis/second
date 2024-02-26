from itertools import chain, combinations
from time import time

def subsets(arr):
    """ 返回非空子集 """
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

def get_item_support(data_set, item):
    """ 计算项集在数据集中的支持度 """
    item_set = set(item)
    return sum(1 for transaction in data_set if item_set.issubset(transaction)) / len(data_set)

def apriori_freq_items(data_set, min_support):
    """ 使用Apriori算法找到频繁项集 """
    c1 = [[item] for transaction in data_set for item in transaction]
    c1 = list(map(frozenset, set(map(tuple, c1))))

    l1 = list(filter(lambda item: get_item_support(data_set, item) >= min_support, c1))
    current_l = l1
    l = [current_l]

    while current_l != []:
        ck = [i.union(j) for i in current_l for j in current_l if len(i.union(j)) == len(i) + 1]
        ck = list(map(frozenset, set(map(tuple, ck))))

        lk = list(filter(lambda item: get_item_support(data_set, item) >= min_support, ck))
        current_l = lk
        if current_l != []:
            l.append(current_l)

    return l

def generate_rules(l, data_set, min_confidence):
    """ 生成关联规则 """
    rules = []
    for i in range(1, len(l)):
        for freq_set in l[i]:
            for subset in subsets(freq_set):
                confidence = get_item_support(data_set, freq_set) / get_item_support(data_set, subset)
                if confidence >= min_confidence:
                    rules.append((subset, freq_set - set(subset), confidence))
    return rules

# 示例数据集
data_set = [
    ["面包", "牛奶"],
    ["面包", "尿布", "啤酒", "鸡蛋"],
    ["牛奶", "尿布", "啤酒", "可乐"],
    ["面包", "牛奶", "尿布", "啤酒"],
    ["面包", "牛奶", "尿布", "可乐"]
]

# 设置不同的最小支持度和最小置信度
min_supports = [0.3, 0.5]
min_confidences = [0.7, 0.8]

# 分析结果
results = {}
for min_support in min_supports:
    for min_confidence in min_confidences:
        start_time = time()
        l = apriori_freq_items(data_set, min_support)
        rules = generate_rules(l, data_set, min_confidence)
        end_time = time()
        results[(min_support, min_confidence)] = {
            "频繁项集": l,
            "关联规则": rules,
            "运行时间": end_time - start_time
        }

print(results)
