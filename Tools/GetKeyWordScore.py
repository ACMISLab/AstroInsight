#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/10/17 19:50
# @Author : 桐
# @QQ:1041264242
# 注意事项：
from py2neo import Graph

def SearchKeyWordScore(Keywords):

    print(f"Info: calculate Keyword score...")

    # 连接到你的 Neo4j 数据库
    graph = Graph("bolt://210.40.16.12:24437", auth=("neo4j", "12345678"))

    # print(Keywords)

    for index,keyword in enumerate(Keywords):
        entity=keyword['entity']

        # 定义Cypher查询语句
        query = f"""
        MATCH (n:Words)
        WHERE n.other CONTAINS '\\'{entity}\\'' OR n.name = '{entity}'
        RETURN n.count,n
        ORDER BY n.count DESC
        LIMIT 1
        """

        # 执行查询并获取结果
        nodes = graph.run(query).data()

        # print(nodes)

        if len(nodes) != 0:
            Keywords[index]['count']=nodes[0]['n.count']
        else:
            Keywords[index]['count'] = 0

    # print(Keywords)

    # 计算最小和最大count值
    min_count = min(item['count'] for item in Keywords)
    max_count = max(item['count'] for item in Keywords)

    # 权重分配
    weight_importance = 0.4
    weight_count = 0.6

    # 计算综合得分
    for item in Keywords:
        normalized_count = (item['count'] - min_count) / (max_count - min_count)
        composite_score = (item['importance_score'] * weight_importance) + (normalized_count * weight_count)
        item['composite_score'] = composite_score

        # 排序并输出结果（可选）
    sorted_data = sorted(Keywords, key=lambda x: x['composite_score'], reverse=True)

    # for item in sorted_data:
    #     print(f"{item['entity']}: {item['composite_score']:.4f}")

    print(f"Info: calculate Keyword score:OK!\n{sorted_data}")
    # print(sorted_data)

    return sorted_data

# SearchKeyWordScore(Keywords="LLM")
# Keywords=[    {
#       "entity": "Bayesian networks",
#       "importance_score": 0.9
#     },
#     {
#       "entity": "automated feature engineering",
#       "importance_score": 0.85
#     },
#     {
#       "entity": "transformer-based deep learning models",
#       "importance_score": 0.9
#     },
#     {
#       "entity": "Vision Transformer (ViT)",
#       "importance_score": 0.8
#     },
#     {
#       "entity": "Convolutional Vision Transformer (CvT)",
#       "importance_score": 0.8
#     },
#     {
#       "entity": "time series imputation techniques",
#       "importance_score": 0.75
#     },
#     {
#       "entity": "semisupervised learning methods",
#       "importance_score": 0.75
#     },
#     {
#       "entity": "Fermi LAT",
#       "importance_score": 0.7
#     },
#     {
#       "entity": "PALFA",
#       "importance_score": 0.7
#     },
#     {
#       "entity": "GBNCC",
#       "importance_score": 0.7
#     },
#     {
#       "entity": "CRAFTS",
#       "importance_score": 0.7
#     },
#     {
#       "entity": "HTRU",
#       "importance_score": 0.7
#     }]
# SearchKeyWordScore(Keywords)
#
# # 准备一个关键词列表
# keywords = ['LLM', 'pulsar']  # 替换为你的实际关键词