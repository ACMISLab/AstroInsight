import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# 示例数据
groups = ['Novelty', 'Feasibility', 'Rationale', 'Technical', 'Dataset', 'Methodology', 'Experimental','Experience']

subgroups = ['0','1','2','3','4','5','6']
# 'AstroInsight', 'ResearchAgent','AI Research'
# 每个子组中堆叠的数据
stack1 = [
    [6, 5, 7, 4, 5, 7, 5, 1],
    [2, 3, 3, 1, 3, 3, 2, 1],
    [6, 8, 7, 9, 1, 2, 16, 9],
    [18, 20, 17, 12, 17, 25, 24, 23],
    [23, 15, 20, 19, 23, 14, 8, 15],
    [4, 10, 7, 16, 10, 10, 5, 12],
    [2, 0, 0, 0, 2, 0, 1, 0]
]
stack2 = [
    [13, 21, 18, 21, 26, 24, 27, 2],
    [11, 3, 8, 8, 14, 7, 15, 1],
    [25, 6, 9, 14, 11, 2, 17, 16],
    [9, 16, 22, 15, 7, 20, 2, 24],
    [2, 14, 4, 3, 3, 8, 0, 8],
    [1, 1, 0, 0, 0, 0, 0, 10],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

stack3 = [
    [10, 11, 11, 12, 13, 13, 12, 1],
    [6, 2, 6, 4, 7, 8, 4, 1],
    [11, 18, 16, 16, 20, 16, 25, 5],
    [25, 13, 17, 19, 14, 15, 15, 31],
    [9, 12, 9, 8, 3, 6, 2, 11],
    [0, 5, 2, 2, 4, 3, 3, 12],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

# 设置柱状图的参数
n_groups = len(groups)
width = 0.2  # 每个组的宽度
x = np.arange(n_groups)  # x 轴上的组位置

patterns = ['','..', '//']  # 斜线型图案
colors = ['#5b68c1', '#82cf7e', '#fccd68', '#f86a69', '#6abddb','#00a376','#ff895a','#a35ab0']  # 每个子组的数据颜色

fig, ax = plt.subplots(figsize=(8, 6))

# 绘制堆叠柱状图
for i, subgroup in enumerate(subgroups):
    if i == 0:
        ax.bar(x - 2*width, stack1[i], width, color=colors[i],  bottom=(np.sum(stack1[:i], axis=0) if i > 0 else 0))
        ax.bar(x - width, stack2[i], width, color=colors[i], hatch=patterns[1], bottom=(np.sum(stack2[:i], axis=0) if i > 0 else 0))
        ax.bar(x, stack3[i], width, color=colors[i], hatch=patterns[2],bottom=(np.sum(stack3[:i], axis=0) if i > 0 else 0))

    else:
        ax.bar(x - 2*width, stack1[i], width, color=colors[i],  bottom=(np.sum(stack1[:i], axis=0) if i > 0 else 0))
        ax.bar(x - width, stack2[i], width, color=colors[i], hatch=patterns[1], bottom=(np.sum(stack2[:i], axis=0) if i > 0 else 0))
        ax.bar(x, stack3[i], width, color=colors[i], hatch=patterns[2],bottom=(np.sum(stack3[:i], axis=0) if i > 0 else 0))



# 添加标签和标题
ax.set_xlabel('Groups')
# ax.set_ylabel('Values')
ax.set_title('Grouped Stacked Bar Chart')
ax.set_xticks(x)
ax.set_xticklabels(groups)
ax.legend()

# 定义图例的颜色和标签
legend_elements = [
    mpatches.Patch(facecolor=colors[0], label='Rank 0'),
    mpatches.Patch(facecolor=colors[1], label='Rank 1'),
    mpatches.Patch(facecolor=colors[2], label='Rank 2'),
    mpatches.Patch(facecolor=colors[3], label='Rank 3'),
    mpatches.Patch(facecolor=colors[4], label='Rank 4'),
    mpatches.Patch(facecolor=colors[5], label='Rank 5'),
    mpatches.Patch(facecolor=colors[6], label='Rank 6'),
    # 如果有更多的堆叠层，继续添加更多的图例元素
]

# 添加图例到图表
ax.legend(handles=legend_elements)

# 显示图表
plt.tight_layout()
plt.show()
