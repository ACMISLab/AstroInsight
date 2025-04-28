#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/24 15:26
# @Author : 桐
# @QQ:1041264242
# 注意事项：



# proxies ={
# 'http': 'http://localhost:7890',
# 'https': 'http://localhost:7890'
# }

proxies = "http://localhost:7890"
url = "10.1088/0004-637X/697/2/1071"
identifier_type = "doi"
output_path = r"PaperAgent\Paper_Ori"

from scihub_cn.scihub import SciHub

sh = SciHub(proxy=proxies)
# 设置is_translate_title可将paper's title进行翻译后下载存储
result = sh.download({"doi": '10.1088/0004-637X/697/2/1071'}, destination=output_path,is_translate_title=False)
print(result)