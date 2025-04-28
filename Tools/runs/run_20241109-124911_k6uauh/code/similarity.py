#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/11/3 20:37
# @Author : 桐
# @QQ:1041264242
# 注意事项：
from FlagEmbedding import FlagAutoModel

# 计算核心论文摘要与相关论文摘要的相似度
def calculate_similarity(related,target):

    # 加载模型
    model = FlagAutoModel.from_finetuned(r'E:\PaperAgent/BAAI/bge-larhe-en-v1.5',
                                         query_instruction_for_retrieval="Represent this sentence for searching relevant passages:",
                                         use_fp16=True)
    # 计算嵌入
    embeddings_1 = model.encode(related)
    embeddings_2 = model.encode(target)

    # 计算相似度
    similarity = embeddings_1 @ embeddings_2.T

    return similarity