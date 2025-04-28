#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/11/3 20:37
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import numpy as np
from FlagEmbedding import FlagAutoModel

# 计算核心论文摘要与相关论文摘要的相似度
def calculate_similarity(related,target,open_eu=False):

    # 加载模型
    model = FlagAutoModel.from_finetuned(r'E:\PaperAgent\bge-large-en-v1.5',
                                         # query_instruction_for_retrieval="Represent this sentence for searching relevant passages:",
                                         use_fp16=True)
    # 计算嵌入
    embeddings_1 = model.encode(related)
    print(len(embeddings_1))
    embeddings_2 = model.encode(target)
    print(embeddings_1)
    print(embeddings_2)

    # 计算相似度
    similarity = embeddings_1 @ embeddings_2.T

    if open_eu==True:
        # 计算欧几里得距离
        euclidean_distance = np.linalg.norm(embeddings_1 - embeddings_2)
        print(similarity)
        print(euclidean_distance)
        return similarity, euclidean_distance
    else:
        print(similarity)
        return similarity

calculate_similarity(related="hello,man",target="hello!!! man",open_eu=True)

# #另外一种方式:
# from sklearn.metrics.pairwise import euclidean_distances
# from sklearn.feature_extraction.text import CountVectorizer
#
# corpus = ['UNC played Duke in basketball','Duke lost the basketball game','I ate a sandwich']  # 文集
# vectorizer = CountVectorizer()  #
# counts = vectorizer.fit_transform(corpus).todense()  # 得到文集corpus的特征向量，并将其转为密集矩阵
# print(counts)
# for x, y in [[0, 1], [0, 2], [1, 2]]:
#     dist = euclidean_distances(counts[x], counts[y])
#     print('文档{}与文档{}的距离{}'.format(x, y, dist))