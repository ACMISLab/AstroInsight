#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/12/25 21:08
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


# 使用示例
# file_path = r'C:\Users\10412\Desktop\实验数据\评估/待评估数据（Acmis） (2).xlsx'  # 将此替换为您的文件路径
file_path = r'E:\PaperAgent\结果/待评估数据_LLM_Ablation_Score.xlsx'  # 将此替换为您的文件路径
start_row = 0  # 例如，从第3行开始（因为是从0开始计数）
skip_n = 3  # 例如，每三行中读取一行


Idea_Draft_Technical_Iteration=0
Idea_Draft_MoAIteration=0
Human_Agent_Cooperation_Iteration=0
pos=0
neg=0

df = read_excel_skip_rows(file_path, start_row=start_row, skip_n=skip_n)

print(len(df['iteration_1_Positive score[-5-5]']))
for data in df['iteration_1_Positive score[-5-5]']:
    if data>0:
        pos+=1
    else:
        neg+=1
    Idea_Draft_Technical_Iteration+=data

Idea_Draft_Technical_Iteration/=61
print(f'Human Overall:{Idea_Draft_Technical_Iteration}    Positive evaluation:{pos}    Negative evaluation:{neg}')
pos=0
neg=0

print(len(df['iteration_2_Positive score[-5-5]']))
for data in df['iteration_2_Positive score[-5-5]']:
    if data>0:
        pos+=1
    else:
        neg+=1
    Idea_Draft_MoAIteration+=data

Idea_Draft_MoAIteration/=61
print(f'Human Overall:{Idea_Draft_MoAIteration}    Positive evaluation:{pos}    Negative evaluation:{neg}')
pos=0
neg=0

print(len(df['iteration_3_Positive score[-5-5]']))
for data in df['iteration_3_Positive score[-5-5]']:
    if data>0:
        pos+=1
    else:
        neg+=1
    Human_Agent_Cooperation_Iteration+=data

Human_Agent_Cooperation_Iteration/=61
print(f'Human Overall:{Human_Agent_Cooperation_Iteration}    Positive evaluation:{pos}    Negative evaluation:{neg}')
pos=0
neg=0

