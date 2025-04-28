#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/12/11 9:24
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import pandas as pd
import matplotlib.pyplot as plt
def read_excel_skip_rows(file_path, sheet_name=0, start_row=0, skip_n=0):
    """
    从Excel文件中读取数据，从指定的起始行开始，并每隔n行读取一行。

    参数:
    - file_path: Excel文件路径。
    - sheet_name: 要读取的工作表名称或索引（默认是第一个工作表）。
    - start_row: 开始读取的行号（0索引）。
    - skip_n: 每隔多少行跳过（例如，1表示读取一行跳过一行）。

    返回:
    - 包含所选行数据的DataFrame。
    """
    # 创建一个空的列表来保存需要读取的行号
    use_rows = []

    # 确定要读取哪些行
    for i in range(start_row, 10 ** 6, skip_n + 1):  # 假设最大行数为10^6
        use_rows.append(i)

    # 使用pandas读取Excel文件，只保留我们感兴趣的行
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

    # 过滤出我们需要的行
    filtered_df = df[df.index.isin(use_rows)]

    return filtered_df.reset_index(drop=True)


def check_sum_and_weighted_average(lst):
    # 检查列表内元素之和是否等于61
    total_sum = sum(lst)
    print(f"列表内元素之和: {total_sum}")
    is_sum_61 = total_sum == 61

    # 计算加权和
    weighted_sum = sum(index * value for index, value in enumerate(lst))

    # 计算加权平均值
    weighted_average = weighted_sum / total_sum if lst else 0

    return weighted_average

def draw():
    file_path = r'E:\PaperAgent\结果\客观评估数据/副本ACMIS_RAG增补实验.xlsx'
    skip_n = 3  # 例如，每三行中读取一行

    group=[1,2,3,0]

    draw_data=[]

    for i in group:
        start_row=i

        df = read_excel_skip_rows(file_path, start_row=start_row, skip_n=skip_n)
        Novelty_Score = [0, 0, 0, 0, 0, 0, 0]
        Feasibility_Score = [0, 0, 0, 0, 0, 0, 0]
        Rationale_Score = [0, 0, 0, 0, 0, 0, 0]
        Technical_Depth_Score = [0, 0, 0, 0, 0, 0, 0]
        Dataset_Relevance_Score = [0, 0, 0, 0, 0, 0, 0]
        Methodology_Suitability_Score = [0, 0, 0, 0, 0, 0, 0]
        Experimental_Design_Score = [0, 0, 0, 0, 0, 0, 0]
        Experience = [0, 0, 0, 0, 0, 0, 0]
        # 可选：标签列表，如果没有具体的分类名称，可以简单地用数字或字母表示
        labels = ['0', '1', '2', '3', '4', '5', '6']  # 这里只是用字母作为示例

        for data in df['Novelty Score']:
            Novelty_Score[data] += 1
        for data in df['Feasibility Score']:
            Feasibility_Score[data] += 1
        for data in df['Rationale Score']:
            Rationale_Score[data] += 1
        for data in df['Technical Depth Score']:
            Technical_Depth_Score[data] += 1
        for data in df['Dataset Relevance Score']:
            Dataset_Relevance_Score[data] += 1
        for data in df['Methodology Suitability Score']:
            Methodology_Suitability_Score[data] += 1
        for data in df['Experimental Design Score']:
            Experimental_Design_Score[data] += 1
        for data in df['Experience']:
            Experience[data] += 1

        ###
        draw_data.append(Methodology_Suitability_Score)

    print(draw_data)
    transposed_matrix = list(map(list, zip(*draw_data)))
    print(transposed_matrix)

    string=""
    for index,row in enumerate(transposed_matrix):
        temp="{"+f"product: 'Rank {index}', 'ResearchAgent': {row[0]}, 'AI Researcher': {row[1]}, 'RAG': {row[2]}, 'AstroInsight':{row[3]}  "+"},"
        string = string+"\n"+temp
    print(string)

draw()
#####开始
# # 使用示例
# # file_path = r'E:\PaperAgent\结果/待评估数据（国台使用）.xlsx'  # 将此替换为您的文件路径
# file_path = r'E:\PaperAgent\结果\客观评估数据/副本国台评估_RAG增补实验.xlsx'
# # 副本国台评估_RAG增补实验.xlsx
# start_row = 1  # 例如，从第3行开始（因为是从0开始计数）
# skip_n = 3  # 例如，每三行中读取一行
#
# df = read_excel_skip_rows(file_path, start_row=start_row, skip_n=skip_n)
# print(df)
# Novelty_Score=[0,0,0,0,0,0,0]
# Feasibility_Score=[0,0,0,0,0,0,0]
# Rationale_Score=[0,0,0,0,0,0,0]
# Technical_Depth_Score=[0,0,0,0,0,0,0]
# Dataset_Relevance_Score=[0,0,0,0,0,0,0]
# Methodology_Suitability_Score=[0,0,0,0,0,0,0]
# Experimental_Design_Score=[0,0,0,0,0,0,0]
# Experience=[0,0,0,0,0,0,0]
# # 可选：标签列表，如果没有具体的分类名称，可以简单地用数字或字母表示
# labels = ['0', '1', '2', '3', '4', '5', '6']  # 这里只是用字母作为示例
#
# for data in df['Novelty Score']:
#     Novelty_Score[data]+=1
# print(Novelty_Score)
# for data in df['Feasibility Score']:
#     Feasibility_Score[data]+=1
# print(Feasibility_Score)
# for data in df['Rationale Score']:
#     Rationale_Score[data]+=1
# print(Rationale_Score)
# for data in df['Technical Depth Score']:
#     Technical_Depth_Score[data]+=1
# print(Technical_Depth_Score)
# for data in df['Dataset Relevance Score']:
#     Dataset_Relevance_Score[data]+=1
# print(Dataset_Relevance_Score)
# for data in df['Methodology Suitability Score']:
#     Methodology_Suitability_Score[data]+=1
# print(Methodology_Suitability_Score)
# for data in df['Experimental Design Score']:
#     Experimental_Design_Score[data]+=1
# print(Experimental_Design_Score)
# for data in df['Experience']:
#     Experience[data]+=1
# print(Experience)
#
# print(f'Novelty_Score:{check_sum_and_weighted_average(Novelty_Score)} Feasibility_Score:{check_sum_and_weighted_average(Feasibility_Score)} Rationale_Score:{check_sum_and_weighted_average(Rationale_Score)} Technical_Depth_Score:{check_sum_and_weighted_average(Technical_Depth_Score)} Dataset_Relevance_Score:{check_sum_and_weighted_average(Dataset_Relevance_Score)} Methodology_Suitability_Score:{check_sum_and_weighted_average(Methodology_Suitability_Score)} Experimental_Design_Score:{check_sum_and_weighted_average(Experimental_Design_Score)} Experience:{check_sum_and_weighted_average(Experience)}')
#
# matrix=[]
# matrix=[Novelty_Score,Feasibility_Score,Rationale_Score,Technical_Depth_Score,Dataset_Relevance_Score,Methodology_Suitability_Score,Experimental_Design_Score,Experience]
# transposed_matrix = list(map(list, zip(*matrix)))
# print('\n')
# for row in transposed_matrix:
#     print(row)

####结束

# # 创建饼图
# plt.figure(figsize=(8, 6))  # 设置图表大小
# plt.pie(score, labels=labels, autopct='%1.1f%%', startangle=140)
# # 显示图表标题
# plt.title('Pie Chart Based on Novelty Score')
# # 显示图形
# plt.show()
# print(df['Novelty Score'])
#Novelty Score	Feasibility Score	Rationale Score	Technical Depth Score	Dataset Relevance Score	Methodology Suitability Score	Experimental Design Score	Experience

