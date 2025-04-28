#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/10/5 21:00
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import csv
import json
import pandas as pd
import openpyxl
from itertools import combinations
from collections import defaultdict, Counter
import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 测试实体列表
entities = [
    "convolutional neural networks",
    "convolutional neural network",
    "CNN",
    "Convolutional Neural Network",
    "Convolutional Neural Networks",
    "Milky Way",
    "pulsars",
    "neutron stars"
]

def first_process():
    # 读取原始xlsx文件
    input_file = r'E:\PaperAgent\archive\整合/output.xlsx'
    wb = openpyxl.load_workbook(input_file)
    ws = wb.active

    # 存储实体及其出现次数的字典
    entity_counter = Counter()
    entity_others = defaultdict(list)

    # 存储二元关系及其出现次数的字典
    pair_counter = Counter()
    num=0
    # 遍历每行数据
    for row in ws.iter_rows(min_row=2,values_only=True):
        try:
            entitys_list = json.loads(row[1].replace("'", '"'))
            # 统计实体出现次数，并收集 other 内容
            for entity_info in entitys_list:
                entity = entity_info['entity']
                other = entity_info['other']
                entity_counter[entity] += 1
                entity_others[entity].extend(other)

                # 生成二元关系并统计出现次数
            for pair in combinations(entitys_list, 2):
                pair_tuple = tuple(sorted([pair[0]['entity'], pair[1]['entity']]))
                pair_counter[pair_tuple] += 1
            num+=1
            print(num)
        except:
            pass

    print(f"收集完毕！{num}")

    # 构建实体 DataFrame 并写入 xlsx 文件
    entity_df = pd.DataFrame({
        'entity': [entity for entity, count in entity_counter.items()],
        'count': [count for count in entity_counter.values()],
        'other': [entity_others[entity] for entity in entity_counter]
    })

    # 去除 other 列中的重复项
    entity_df['other'] = entity_df['other'].apply(lambda x: list(set(x)))

    # 写入实体统计结果到 xlsx 文件
    entity_file_path = r'E:\PaperAgent\archive\整合/entity_counts.csv'
    entity_df.to_csv(r'E:\PaperAgent\archive\整合/entity_counts.csv', index=False)

    # 构建二元关系 DataFrame 并写入 xlsx 文件
    pair_df = pd.DataFrame({
        'pair': [' & '.join(pair) for pair in pair_counter.keys()],
        'count': [count for count in pair_counter.values()]
    })

    # 写入二元关系统计结果到 xlsx 文件
    pair_file_path = r'E:\PaperAgent\archive\整合/pair_counts.csv'
    pair_df.to_csv(r'E:\PaperAgent\archive\整合/pair_counts.csv', index=False)

    print(f"实体统计结果已保存到 {entity_file_path}")
    print(f"二元关系统计结果已保存到 {pair_file_path}")

def mergebysimilarity():
    results = []
    # Step 1: 读取数据
    df = pd.read_excel(r'E:\PaperAgent\archive\整合/test.xlsx')

    # 计算每一对实体之间的是否相似
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            if df.loc[i, 'entity'].lower()==df.loc[j, 'entity'].lower() or df.loc[i, 'entity'].lower()==df.loc[j, 'entity'].lower()+'s' or df.loc[i, 'entity'].lower()==df.loc[j, 'entity'][:-1].lower():

                # 合并 df.loc[i, 'other'] 和 df.loc[j, 'other'] 的内容
                combined_other = df.loc[i, 'other'] + df.loc[j, 'other'] + df.loc[j, 'entity']  # 假设 'other' 列包含列表

                # 构建实体 DataFrame 并写入 xlsx 文件
                entity_df = pd.DataFrame({
                    'entity': df.loc[i, 'entity'],
                    'count': df.loc[i, 'count']+df.loc[j, 'count'],
                    'other': [combined_other]
                })

                # 去除 other 列中的重复项
                entity_df['other'] = entity_df['other'].apply(lambda x: list(set(x)))
                results.append(entity_df)

                # 合并所有结果并写入 xlsx 文件
    final_df = pd.concat(results, ignore_index=True)
    entity_file_path = r'E:\PaperAgent\archive\整合/test2.xlsx'
    final_df.to_excel(entity_file_path, index=False)

def preprocess_entity(entity):
    return entity.lower()

def is_similar(ent1, ent2):
    ent1, ent2 = preprocess_entity(ent1), preprocess_entity(ent2)
    return ent1 == ent2 or ent1 == ent2 + 's' or ent1 == ent2[:-1]

def merge_by_similarity():
    # Step 1: 读取数据
    df = pd.read_excel(r'E:\PaperAgent\archive\整合/test.xlsx')

    # 预处理实体，降低后续比较的开销
    df['entity_lower'] = df['entity'].apply(preprocess_entity)

    # 用来存储已经合并过的索引
    merged_indices = set()

    results = []

    # 使用字典存储实体和对应的索引列表，方便查找和合并
    entity_dict = {}
    for idx, row in df.iterrows():
        print(idx)
        if idx in merged_indices:
            continue

        entity_list = []
        similar_indices = []

        for idx2, row2 in df.iterrows():
            if idx2 in merged_indices or idx == idx2:
                continue
            if is_similar(row['entity'], row2['entity']):
                entity_list.append(row2)
                similar_indices.append(idx2)

        if not entity_list:
            continue  # 没有相似的实体，跳过

        # 合并操作
        combined_other = list(set(sum([ent['other'] for ent in entity_list + [row]], [])))
        combined_count = sum([ent['count'] for ent in entity_list + [row]])

        # 构建实体 DataFrame
        entity_df = pd.DataFrame({
            'entity': [row['entity']],
            'count': [combined_count],
            'other': [combined_other]
        })

        results.append(entity_df)
        merged_indices.update(similar_indices)  # 将相似的索引标记为已合并

    # 合并所有结果并写入 xlsx 文件
    final_df = pd.concat(results, ignore_index=True)
    entity_file_path = r'E:\PaperAgent\archive\整合/test2.xlsx'
    final_df.to_excel(entity_file_path, index=False)

def split_csv(input_file, output1, output2):
    # 读取输入文件的行数
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

        # 计算行数及分割点
    total_rows = len(rows)
    split_point = total_rows // 2

    # 写入第一个输出文件
    with open(output1, 'w', newline='', encoding='utf-8') as outfile1:
        writer1 = csv.writer(outfile1)
        writer1.writerows(rows[:split_point])

        # 写入第二个输出文件
    with open(output2, 'w', newline='', encoding='utf-8') as outfile2:
        writer2 = csv.writer(outfile2)
        writer2.writerows(rows[split_point:])

def merges():
    results = []
    merge_true=[]
    # Step 1: 读取数据
    df = pd.read_excel(r'E:\PaperAgent\archive\整合\实体计数/entity_counts_2 - 副本.xlsx')

    # 计算每一对实体之间的是否相似
    for i in range(len(df)):
        print(i)

        if i in merge_true:
            continue

        for j in range(i + 1, len(df)):

            if df.loc[i, 'entity_lower'][0]!=df.loc[j, 'entity_lower'][0]:
                # print(df.loc[j, 'entity_lower'][0])
                break

            if df.loc[i, 'entity_lower'] == df.loc[j, 'entity_lower'] or df.loc[i, 'entity_lower'] == df.loc[j,'entity_lower'] + 's' or df.loc[i,'entity_lower']== df.loc[j,'entity_lower'][:-1]:

                combined_other = list(df.loc[i, 'other']) + list(df.loc[j, 'other']) + list(df.loc[j, 'entity'])  # 假设 'other' 列包含列表

                print(combined_other)

                # 构建实体 DataFrame 并写入 xlsx 文件
                entity_df = pd.DataFrame({
                    'entity': df.loc[i, 'entity'],
                    'count': int(df.loc[i, 'count'])+int(df.loc[j, 'count']),
                    'other': combined_other
                })

                results.append(entity_df)
                merge_true.append(j)

    # 合并所有结果并写入 xlsx 文件
    final_df = pd.concat(results, ignore_index=True)
    entity_file_path = r'E:\PaperAgent\archive\整合\实体计数\output_results2.xlsx'
    final_df.to_excel(entity_file_path, index=False)


def merge():
    results = []
    merge_true = set()  # 使用集合提高查找效率

    # Step 1: 读取数据
    df = pd.read_excel(r'E:\PaperAgent\archive\整合\实体计数/test - 副本.xlsx')

    # 预先提取 'entity_lower' 列
    entity_lowers = df['entity_lower'].values
    counts = df['count'].values
    entities = df['entity'].values
    others = df['other'].values  # 假设 'other' 列包含列表

    for i in range(len(df)):

        print(f"------------{i}")
        combined_other=[]
        count=0

        if i in merge_true:
            print(True)
            continue

        for j in range(i + 1, len(df)):

            if entity_lowers[i][0] != entity_lowers[j][0]:
                break

            if (entity_lowers[i] == entity_lowers[j] or
                    entity_lowers[i] == entity_lowers[j] + 's' or
                    entity_lowers[i] == entity_lowers[j][:-1]):

                combined_other +=  eval(others[j]) + [entities[j]]
                count += counts[j]
                merge_true.add(j)

        entity_df = pd.DataFrame({
            'entity': entities[i],
            'count': counts[i] + count,
            'other': [str(combined_other+eval(others[i]))]
        })

        results.append(entity_df)

    final_df = pd.concat(results, ignore_index=True)
    entity_file_path = r'E:\PaperAgent\archive\整合\实体计数\output_results2.xlsx'
    final_df.to_excel(entity_file_path, index=False)



# merge()


# split_csv(input_file=r'E:\PaperAgent\archive\整合/entity_counts.csv',output1=r'E:\PaperAgent\archive\整合/entity_counts_split1.csv',\
#           output2=r'E:\PaperAgent\archive\整合/entity_counts_split2.csv')

import pandas as pd

# 读取Excel文件
df1 = pd.read_excel(r'E:\PaperAgent\archive\整合\output_results1.xlsx')
df2 = pd.read_excel(r'E:\PaperAgent\archive\整合\output_results2.xlsx')

# 检查列名称和数据类型是否一致
assert list(df1.columns) == list(df2.columns), "两个数据框的列名称不一致"
assert df1.dtypes.equals(df2.dtypes), "两个数据框的数据类型不一致"

# 合并数据框
df_combined = pd.concat([df1, df2], ignore_index=True)

# 检查合并后数据的行数
assert len(df_combined) == len(df1) + len(df2), "合并后的数据行数不正确"

# 按照 entity_lower 列升序排序
df_sorted = df_combined.sort_values(by='entity_lower').reset_index(drop=True)

# 保存为CSV文件
df_sorted.to_csv(r'E:\PaperAgent\archive\整合\combined_output_results.csv', index=False, encoding='utf-8')

print("合并并保存为 combined_results.csv 成功!")

# # 指定 CSV 文件的路径
# file_path = r'E:\PaperAgent\archive\整合\combined_results.csv'
#
# # 读取 CSV 文件
# data = pd.read_csv(file_path)
#
# # 打印合并后数据的行数
# print(f"合并后数据的行数: {len(data)}")
#
# # # 按照 entity_lower 列升序排序
# # df_sorted = df_combined.sort_values(by='entity_lower').reset_index(drop=True)
#
# # 展示前 100 行数据
# print(data.head(100))