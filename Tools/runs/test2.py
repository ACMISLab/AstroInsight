#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/12/11 18:03
# @Author : 桐
# @QQ:1041264242
# 注意事项：
groups = ['Novelty', 'Feasibility', 'Rationale', 'Technical', 'Dataset', 'Methodology', 'Experimental','Experience']
Astro=[[6, 2, 6, 18, 23, 4, 2],
[5, 3, 8, 20, 15, 10, 0],
[7, 3, 7, 17, 20, 7, 0],
[4, 1, 9, 12, 19, 16, 0],
[5, 3, 1, 17, 23, 10, 2],
[7, 3, 2, 25, 14, 10, 0],
[5, 2, 16, 24, 8, 5, 1],
[1, 1, 9, 23, 15, 12, 0]]

Res=[[13, 11, 25, 9, 2, 1, 0],
[21, 3, 6, 16, 14, 1, 0],
[18, 8, 9, 22, 4, 0, 0],
[21, 8, 14, 15, 3, 0, 0],
[26, 14, 11, 7, 3, 0, 0],
[24, 7, 2, 20, 8, 0, 0],
[27, 15, 17, 2, 0, 0, 0],
[2, 1, 16, 24, 8, 10, 0],
]

AI=[[10, 6, 11, 25, 9, 0, 0],
[11, 2, 18, 13, 12, 5, 0],
[11, 6, 16, 17, 9, 2, 0],
[12, 4, 16, 19, 8, 2, 0],
[13, 7, 20, 14, 3, 4, 0],
[13, 8, 16, 15, 6, 3, 0],
[12, 4, 25, 15, 2, 3, 0],
[1, 1, 5, 31, 11, 12, 0],
]


for i in range(len(Astro)):
    string = ""
    for j in range(len(Astro[i])):
        string+= '{'+f" product: 'Rank {j}', AstroInsight: {Astro[i][j]}, ResearchAgent: {Res[i][j]}, 'AI Research': {AI[i][j]} "+'},\n'
    print(groups[i])
    print(string+'\n')