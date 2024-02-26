from itertools import chain, combinations
from typing import List, Set, Tuple
from time import time

def subsets(arr: List[str]) -> List[Set[str]]:
    """ 返回非空子集 """
    return list(chain(*[combinations(arr, i + 1) for i in range(len(arr))]))

def get_item_support(data_set: List[List[str]], item: Set[str]) -> float:
    """ 计算项集在数据集中的支持度 """
    item_set = set(item)
    return sum(1 for transaction in data_set if item_set.issubset(transaction)) / len(data_set)

def apriori_freq_items(data_set: List[List[str]], min_support: float) -> List[List[Set[str]]]:
    """ 使用Apriori算法找到频繁项集 """
    def join_set(item_set: List[Set[str]], k: int) -> List[Set[str]]:
        return [i.union(j) for i in item_set for j in item_set if len(i.union(j)) == k]

    c1 = [frozenset([item]) for transaction in data_set for item in transaction]
    l1 = [item for item in c1 if get_item_support(data_set, item) >= min_support]
    l = [l1]
    k = 2

    while (len(l[k-2]) > 0):
        ck = join_set(l[k-2], k)
        lk = [item for item in ck if get_item_support(data_set, item) >= min_support]
        l.append(lk)
        k += 1

    return l

def generate_rules(l: List[List[Set[str]]], data_set: List[List[str]], min_confidence: float) -> List[Tuple[Set[str], Set[str], float]]:
    """ 生成关联规则 """
    rules = []
    for i in range(1, len(l)):
        for freq_set in l[i]:
            for subset in subsets(freq_set):
                confidence = get_item_support(data_set, freq_set) / get_item_support(data_set, subset)
                if confidence >= min_confidence:
                    rules.append((subset, freq_set - subset, confidence))
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
print(1)
