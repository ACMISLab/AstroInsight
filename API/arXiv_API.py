#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/21 23:07
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import arxiv
import datetime
import json
import os
import requests
import re


proxies ={
'http': 'http://localhost:7890',
'https': 'http://localhost:7890'
}

def read_markdown_file(file_path):
    """
    读取指定Markdown文件的内容，并将其打印到控制台。

    参数:
    file_path (str): Markdown文件的路径。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
            return content
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except IOError as e:
        print(f"读取文件时出错: {e}")

def download_pdf(url, save_dir, file_name):
    # 检查保存目录是否存在，如果不存在则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

        # 完整的文件路径
    file_path = os.path.join(save_dir, file_name)

    try:
        # 发送HTTP GET请求来获取PDF文件
        response = requests.get(url, stream=True,proxies=proxies)
        # response = requests.get(url, stream=True)

        # 检查请求是否成功
        response.raise_for_status()

        # 以二进制模式写入文件
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"文件已成功下载并保存至: {file_path}")
        return file_path

    except requests.RequestException as e:
        print(f"下载失败: {e}")
        return False

def sanitize_folder_name(folder_name):
    # 定义需要替换的违规字符集
    illegal_chars = r'<>:"/\\|\?*'
    # 使用正则表达式替换违规字符为下划线 _
    sanitized_name = re.sub(f'[{illegal_chars}]', '_', folder_name)
    return sanitized_name

def get_authors(authors, first_author=False):
    output = str()
    if first_author == False:
        output = ", ".join(str(author) for author in authors)
    else:
        output = authors[0]
    return output

def sort_papers(papers):
    output = dict()
    keys = list(papers.keys())
    keys.sort(reverse=True)
    for key in keys:
        output[key] = papers[key]
    return output

def get_daily_papers(query="astronomy", max_results=2):
    """
    @param topic: str
    @param query: str
    @return paper_with_code: dict
    """

    paper_list=[]

    search_engine = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    for result in search_engine.results():

        paper_id = result.entry_id
        paper_title = result.title
        paper_pdf = result.pdf_url
        paper_doi = result.doi
        paper_abstract = result.summary.replace("\n", " ")
        paper_authors = get_authors(result.authors)
        primary_category = result.primary_category
        publish_time = result.published.date().isoformat()
        # paper_first_author = get_authors(result.authors, first_author=True)

        # print("Time = ", publish_time,
        #       " title = ", paper_title,
        #       " author = ", paper_first_author)

        # eg: 2108.09112v1 -> 2108.09112

        # ver_pos = paper_id.find('v')
        # if ver_pos == -1:
        #     paper_key = paper_id
        # else:
        #     paper_key = paper_id[0:ver_pos]

        # content[paper_key] = f"|**{publish_time}**|**{paper_title}**|{paper_first_author} et.al.|[{paper_id}]({paper_url})|\n"

        data = {"topic": query,
                "title": paper_title,
                "id" : paper_id,
                "doi": paper_doi,
                "pdf": paper_pdf,
                "abstract": paper_abstract,
                "authors": paper_authors,
                "category": primary_category,
                "time": publish_time}

        paper_list.append(data)

    return paper_list

def update_json_file(filename, data_all):
    with open(filename, "r") as f:
        content = f.read()
        if not content:
            m = {}
        else:
            m = json.loads(content)

    json_data = m.copy()

    # update papers in each keywords
    for data in data_all:
        for keyword in data.keys():
            papers = data[keyword]

            if keyword in json_data.keys():
                json_data[keyword].update(papers)
            else:
                json_data[keyword] = papers

    with open(filename, "w") as f:
        json.dump(json_data, f)

def json_to_md(filename):
    """
    @param filename: str
    @return None
    """

    DateNow = datetime.date.today()
    DateNow = str(DateNow)
    DateNow = DateNow.replace('-', '.')

    with open(filename, "r") as f:
        content = f.read()
        if not content:
            data = {}
        else:
            data = json.loads(content)

    md_filename = "README.md"

    # clean README.md if daily already exist else create it
    with open(md_filename, "w+") as f:
        pass

    # write data into README.md
    with open(md_filename, "a+") as f:

        f.write("## Updated on " + DateNow + "\n\n")

        for keyword in data.keys():
            day_content = data[keyword]
            if not day_content:
                continue
            # the head of each part
            f.write(f"## {keyword}\n\n")
            f.write("|Publish Date|Title|Authors|PDF|\n" + "|---|---|---|---|\n")
            # sort papers by date
            day_content = sort_papers(day_content)

            for _, v in day_content.items():
                if v is not None:
                    f.write(v)

            f.write(f"\n")
    print("finished")

def search_paper(keywords,limit=2):
    data_collector = []

    for keyword in keywords:
        try:
            print(f"Info: retrieve papers related to technical entities...")
            data_collector += get_daily_papers(query=keyword, max_results=limit)
            print(json.dumps(data_collector, indent=4))
            print(f"Info: retrieve papers related to technical entities: {keyword} State:OK!")
        except:
            print(f"Info: retrieve papers related to technical entities: {keyword} Sate: Miss")
            pass

    return data_collector

# if __name__ == "__main__":
#     data=search_paper(keywords = ["Pulsar Candidate Classification"],limit=5)
#     print(json.dumps(data, indent=4))
    # print("\n")
#
#
#     # # update README.md file
#     # json_file = "cv-arxiv-daily.json"
#     # if ~os.path.exists(json_file):
#     #     with open(json_file, 'w') as a:
#     #         print("create " + json_file)
#     # # update json data
#     # update_json_file(json_file, data_collector)
#     # # json data to markdown
#     # json_to_md(json_file)
