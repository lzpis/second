import csv
import jieba
import json
from collections import Counter

# 读取CSV文件
with open('金陵历朝诗歌.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    dynasty_data = {}

    # 遍历CSV文件
    for row in reader:
        dynasty = row['dynasty']
        content = row['content']

        # 合并同一个朝代的诗作内容
        if dynasty not in dynasty_data:
            dynasty_data[dynasty] = []

        dynasty_data[dynasty].extend(jieba.lcut(content))

# 分词处理并生成词云数据
word_data = {}
for dynasty, content in dynasty_data.items():
    # 假设stop_words列表包含了所有要排除的词
    stop_words = ['，', ' ', '。', '！', '？', '：', '；', '“', '”', '‘', '’', '(', ')', '&#8203;``【oaicite:0】``&#8203;', '[',
                  ']', '《', '》', '亦', '何',
                  '乎', '乃', '之', '也', '于', '云', '而', '则', '者', '若', '自', '所', '其', '即', '矣', '焉', '以', '且', '尔', '耳',
                  '哉', '如', '如何', '若何', '何如', '不', '无', '莫', '勿', '毋', '未', '岂', '却', '故', '因', '果', '为', '令', '使', '以',
                  '于', '我', '谁', '他', '与', '则', '乃', '皆', '虽', '既', '尚', '呜呼', '呼哉', '矣哉', '矣乎', '矣矣', '乎哉', '乎乎',
                  '矣哉矣',
                  '哉矣', '乎矣', '乎乎矣', '矣矣矣', '之而', '之兮', '之乎', '之哉', '兮哉', '也而', '也兮', '也乎', '也哉', '也也', '以而', '以兮',
                  '以乎', '以哉', '以也', '若而', '若兮', '若乎', '若哉', '若也', '而而', '而兮', '而乎', '而哉', '而也', '乃而', '乃兮', '乃乎', '乃哉',
                  '乃也', '皆而', '皆兮', '皆乎', '皆哉', '皆也', '虽而', '虽兮', '虽乎', '虽哉', '虽也', '既而', '既兮', '既乎', '既哉', '既也', '尚而',
                  '尚兮', '尚乎', '尚哉', '尚也', '呜呼哉', '呼哉矣', '呜呼矣哉', '呜呼矣矣', '呼哉矣哉', '矣哉矣哉', '呼哉矣矣', '矣哉矣矣', '哉矣矣矣', '矣矣矣矣']

    words = [word for word in content if word not in stop_words]

    # 筛选频数大于等于3的词语（条件根据朝代的诗歌数量决定）
    if len(words) >= 100:
        word_counter = Counter(words)
        filtered_word_data = {word: count for word, count in word_counter.items() if count >= 3}
    else:
        filtered_word_data = {word: count for word, count in Counter(words).items()}

    word_data[dynasty] = filtered_word_data

# 构造词云数据
word_cloud_data = {dynasty: {"dynasty": dynasty, "data": data} for dynasty, data in word_data.items()}

# 保存为JSON文件
with open('word_cloud_data_chaodai.json', 'w', encoding='utf-8') as json_file:
    json.dump(word_cloud_data, json_file, ensure_ascii=False, indent=4)

print("词云数据已保存为word_cloud_data.json文件")
