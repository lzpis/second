import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score

# 加载数据集（示例）
# 假设X为特征，y为标签
# X, y = load_data()

# 将文本数据转换为TF-IDF特征
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

# 选择分类模型
model = MultinomialNB()

# 定义十折交叉验证
kf = KFold(n_splits=10, shuffle=True, random_state=42)

# 定义评估指标
scoring = {
    'accuracy': make_scorer(accuracy_score),
    'precision': make_scorer(precision_score, average='macro'),
    'recall': make_scorer(recall_score, average='macro'),
    'f1': make_scorer(f1_score, average='macro')
}

# 进行十折交叉验证并计算每个指标
scores = cross_val_score(model, X_tfidf, y, cv=kf, scoring=scoring)

# 打印结果
print(f"Accuracy: {np.mean(scores['test_accuracy'])}")
print(f"Macro Precision: {np.mean(scores['test_precision'])}")
print(f"Macro Recall: {np.mean(scores['test_recall'])}")
print(f"Macro F1 Score: {np.mean(scores['test_f1'])}")
