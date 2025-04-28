#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/12/30 13:12
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import pandas as pd
import numpy as np

# 读取数据
df = pd.read_excel(r"E:\PaperAgent\结果\客观评估数据\跑完的结果/our.xlsx") # ai_researcher.xlsx our.xlsx research_agent.xlsx

# 生成摘要年份为2024年
current_year = 2024

# 将论文按年份分类
historical_papers = df[df['Year'] <= current_year - 5]
contemporary_papers = df[df['Year'] > current_year - 5]


# 计算历史不相似性 HD (历史论文)
# 对于历史不相似性，我们需要找出五年以前论文最相似的5篇论文
def calculate_historical_dissimilarity(historical_papers):
    # # 计算与历史论文的欧式距离
    # historical_papers['distance'] = historical_papers['ed']
    # historical_papers_sorted = historical_papers.sort_values(by='distance')
    # return historical_papers_sorted.head(5)['ed'].sum()/5
    # 计算与历史论文的欧式距离
    historical_papers['distance'] = historical_papers['ed']
    historical_papers_sorted = historical_papers.sort_values(by='distance')

    # 获取前五篇论文或所有论文（如果少于五篇）
    top_five_or_less = historical_papers_sorted.head(5)

    # 如果论文数量不足五篇，补充缺失的值为0.5
    num_papers = len(top_five_or_less)
    if num_papers < 5:
        missing_values_sum = (5 - num_papers) * 0.5
        sum_of_distances = top_five_or_less['ed'].sum() + missing_values_sum
    else:
        sum_of_distances = top_five_or_less['ed'].sum()

    # 返回平均值
    return sum_of_distances / 5

# .mean()


# 计算当代相似性 CD (近五年论文)
def calculate_contemporary_dissimilarity(contemporary_papers):
    # 计算与当代论文的欧式距离
    contemporary_papers['distance'] = contemporary_papers['ed']
    contemporary_papers_sorted = contemporary_papers.sort_values(by='distance')

    # 获取前五篇论文或所有论文（如果少于五篇）
    top_five_or_less = contemporary_papers_sorted.head(5)

    # 如果论文数量不足五篇，补充缺失的值为0.9
    num_papers = len(top_five_or_less)
    if num_papers < 5:
        missing_values_sum = (5 - num_papers) * 0.9
        sum_of_distances = top_five_or_less['ed'].sum() + missing_values_sum
    else:
        sum_of_distances = top_five_or_less['ed'].sum()

    # 返回平均值
    return sum_of_distances / 5

    # return contemporary_papers_sorted.head(5)['ed'].sum()/5


# 计算当代影响 CI (引用量)
def calculate_contemporary_impact(contemporary_papers):
    # 计算与当代论文的相似性，取前五篇的引用量
    contemporary_papers['distance'] = contemporary_papers['ed']
    contemporary_papers_sorted = contemporary_papers.sort_values(by='distance')

    # 获取前五篇论文或所有论文（如果少于五篇）
    top_five_or_less = contemporary_papers_sorted.head(5)

    # 如果论文数量不足五篇，补充缺失的值为0
    num_papers = len(top_five_or_less)
    if num_papers < 5:
        missing_values_sum = (5 - num_papers) * 0
        sum_of_distances = top_five_or_less['cite'].sum() + missing_values_sum
    else:
        sum_of_distances = top_five_or_less['cite'].sum()

    # 返回平均值
    return sum_of_distances / 5

    # return contemporary_papers_sorted.head(5)['cite'].sum()/5


# 按照主题分组并计算指标
def calculate_metrics_by_topic(df):
    result = []

    # 遍历每个主题
    for topic, group in df.groupby('topic'):
        # 获取该主题的所有历史和当代论文
        historical_papers_topic = group[group['Year'] <= current_year - 5]
        contemporary_papers_topic = group[group['Year'] > current_year - 5]


        # 计算 HD、CD 和 CI
        hd = calculate_historical_dissimilarity(historical_papers_topic)
        cd = calculate_contemporary_dissimilarity(contemporary_papers_topic)
        ci = calculate_contemporary_impact(contemporary_papers_topic)

        # 保存结果
        result.append({
            'Topic': topic,
            'Historical Dissimilarity (HD)': hd,
            'Contemporary Dissimilarity (CD)': cd,
            'Contemporary Impact (CI)': ci
        })
        # break

    return pd.DataFrame(result)


# 计算每个主题的指标
metrics_by_topic = calculate_metrics_by_topic(df)
# 将结果保存为Excel文件
metrics_by_topic.to_excel(r'E:\PaperAgent\结果\客观评估数据\跑完的结果/result.xlsx', index=False)
# 输出结果
print(metrics_by_topic)
