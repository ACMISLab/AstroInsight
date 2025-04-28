#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/24 11:29
# @Author : 桐
# @QQ:1041264242
# 注意事项：
# 10.1088/0004-637X/697/2/1071
import os
import re

import requests
from bs4 import BeautifulSoup
import urllib.parse
from scihub_cn.scihub import SciHub


def check_pdf(file_path):
    """
    检查PDF文件是否能正常打开。

    参数:
    file_path (str): PDF文件路径。

    返回:
    bool: 如果文件能正常打开则返回True，否则返回False。
    """
    try:
        with open(file_path, 'rb') as f:
            # 读取文件的前5个字节，PDF文件通常以"%PDF-"开头
            # 这里我们读取5个字节是因为"%PDF-"是5个字节（包括百分号）
            header = f.read(5)
            # 检查文件开头是否为"%PDF-"（PDF文件的魔数）
            if header != b'%PDF-':
                # 如果不是PDF开头，则抛出异常
                print("File does not start with PDF header.")
                return False
            # 如果需要，可以在这里添加更多的检查逻辑
            return True
    except Exception as e:
        print(f"Error opening PDF file {file_path}: {e}")
        return False

def sanitize_folder_name(folder_name):
    # 定义需要替换的违规字符集
    illegal_chars = r'<>:"/\\|\?*'
    # 使用正则表达式替换违规字符为下划线 _
    sanitized_name = re.sub(f'[{illegal_chars}]', '_', folder_name)
    return sanitized_name

def search_google_scholar(doi):
    proxies = {
        'http': 'http://localhost:7890',
        'https': 'http://localhost:7890'
    }

    # Google Scholar的搜索URL
    search_url = f"https://scholar.google.com/scholar?q={urllib.parse.quote(doi)}"

    print(search_url)
    # 模拟请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers , proxies=proxies)

    # print(response)

    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup)

    # 查找包含[PDF]文本的链接
    pdf_links = []
    for link in soup.find_all('a'):
        if '[PDF]' in link.get_text():
            pdf_links.append(link['href'])


    # 输出找到的链接
    for pdf_link in pdf_links:
        print(pdf_link)
        return pdf_link

def download_pdf_google(pdf_url,title,output_path):
    proxies = {
        'http': 'http://localhost:7890',
        'https': 'http://localhost:7890'
    }

    save_path=f"{output_path}/{title}.pdf"

    # 发送HTTP GET请求来获取PDF文件
    response = requests.get(pdf_url, stream=True, proxies=proxies)
    # response = requests.get(url, stream=True)
    # 检查请求是否成功
    response.raise_for_status()
    # 以二进制模式写入文件
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"文件已成功下载并保存至: {save_path}")

    return save_path

def download_pdf_scihub(doi,output_path):
    proxies = "http://localhost:7890"

    sh = SciHub(proxy=proxies)

    # 设置is_translate_title可将paper's title进行翻译后下载存储
    save_path = sh.download({"doi": doi}, destination=output_path, is_translate_title=False)

    # print(result)
    return save_path

def getdown_pdf_google_url(doi,title,output_path):
    pdf_url = search_google_scholar(doi)

    if pdf_url:
        print("找到PDF链接:", pdf_url)
        save_path=download_pdf_google(pdf_url,title,output_path)
        return save_path
    else:
        print("未找到PDF链接。")
        return False

def download_pdf(doi,title,output_path):
    """
    尝试通过两个方法下载一个PDF文件。

    参数:
    doi (str): 需要下载的PDF文件的DOI。

    返回:
    str or None: 成功下载时返回文件路径，否则返回None或错误信息。
    """
    # 尝试使用 Google 下载 PDF
    result = getdown_pdf_google_url(doi,title,output_path)

    if result and check_pdf(result):  # 假设 check_pdf 函数用于验证PDF文件能否正常打开
        return result

    else:
        # 若 Google 下载失败，则尝试使用 Sci-Hub 下载 PDF
        result = download_pdf_scihub(doi,output_path)

        if result and check_pdf(result):
            return result
        else:
            # 若两者都失败，则返回错误信息
            return False

def download_all_pdfs(dois ,title,topic,):
    """
    下载给定DOI列表中的PDF文件。

    参数:
    dois (list): 包含若干个DOI的列表。

    返回:
    list: 包含所有下载结果的列表，每个元素是对应DOI的下载结果信息。
    """
    output_path = fr"xxxx"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for doi in dois:

        result = download_pdf(doi,sanitize_folder_name(title),output_path)

        print(result)

        if result != False:
            break


    return result


#
# 示例调用
# dois = []
# result = download_all_pdfs(dois)
# print(result)

# download_pdf_scihub(doi="10.1088/0004-637X/697/2/1071",output_path=r"xxxx")

# print(check_pdf(r"xxxx"))


