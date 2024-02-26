#
# from flask import Flask, request, jsonify, render_template
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import pandas as pd
# import jieba
# import os
# import time
#
# app = Flask(__name__)
# @app.route('/favicon.ico')
# def favicon():
#     return ''
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
#
# @app.route('/generate_wordcloud', methods=['POST'])
# def generate_wordcloud():
#     data1 = pd.read_csv("123.csv")
#
#     # 合并同一作者的诗词内容
#     data_grouped = data1.groupby('author')['content'].apply(lambda x: ' '.join(x)).reset_index()
#
#     # 分词处理
#     data_grouped['分词结果'] = data_grouped['content'].apply(lambda x: ' '.join(jieba.cut(x)))
#
#     poet_name = request.get_json()['poetName']
#
#     # 根据诗人名称获取对应的词云图
#     poet_data = data_grouped[data_grouped['author'] == poet_name]
#     if poet_data.empty:
#         return jsonify({'error': '找不到该诗人的数据'})
#
#     content = poet_data.iloc[0]['分词结果']
#
#     wordcloud = WordCloud(font_path='C:/Windows/Fonts/simkai.ttf', width=800, height=400).generate(content)
#
#     plt.figure(figsize=(10, 6))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis('off')
#     plt.savefig('static/wordcloud.png')  # 保存为PNG图片
#     plt.close()
#
#     image_path = f'/static/wordcloud.png?t={int(time.time())}'
#     return jsonify({'imagePath': image_path})
#
# if __name__ == '__main__':
#     app.run(debug=True)
import json
from flask import Flask, request, jsonify, render_template
import pandas as pd
import jieba
from wordcloud import WordCloud

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return ''

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    data = pd.read_csv("123.csv")

    # 合并同一作者的诗词内容
    data_grouped = data.groupby('author')['content'].apply(lambda x: ' '.join(x)).reset_index()

    # 分词处理
    data_grouped['分词结果'] = data_grouped['content'].apply(lambda x: ' '.join(jieba.cut(x)))

    poet_name = request.get_json()['poetName']

    # 根据诗人名称获取对应的词云图
    poet_data = data_grouped[data_grouped['author'] == poet_name]
    if poet_data.empty:
        return jsonify({'error': '找不到该诗人的数据'})

    content = poet_data.iloc[0]['分词结果']

    # 生成词云图
    wordcloud = WordCloud(font_path='./font/simkai.ttf', width=800, height=400)
    wordcloud.generate(content)

    # 获取词云图数据
    word_list = wordcloud.words_

    return jsonify({'words': json.dumps(word_list)})

if __name__ == '__main__':
    app.run(debug=True)