#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/9/22 13:41
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import base64
import os
import re

import requests
import asyncio
import time
import zipfile
import pandas as pd
# 下载文件的URL
download_url_template = "http://210.40.16.12:24442/download/{task_id}"
key_token="Fill in your MinerU API"

# # 假设上传文件后获得的task_id
# task_id = "your_task_id_here"

def extract_pdf_name(path):
    # 使用正则表达式提取 PDF 文件名称
    match = re.search(r"([^\\/]+)\.pdf$", path, re.IGNORECASE)

    if match:
        pdf_name = match.group(1)
        print("提取的 PDF 文件名称:", pdf_name)
    else:
        print("未找到 PDF 文件名称")
    return pdf_name

def upload(file_path):
    # 上传文件的URL
    upload_url = "http://210.40.16.12:24442/upload"

    user_name = "zfy"

    # 读取文件
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'user_name': user_name}

        # 发送POST请求上传文件
        response = requests.post(upload_url, files=files, data=data)

    # 打印响应内容
    # print(response)
    return response.json()

def download_zip_file(url, zip_save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(zip_save_path, 'wb') as file:
            file.write(response.content)
        print(f"ZIP 文件已下载到: {zip_save_path}")
    else:
        print(f"无法下载 ZIP 文件，状态码: {response.status_code}")

def find_md_files_in_zip(zip_path,copy_path,batch_id):
    md_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.md'):
                md_files.append(file)
        if md_files:
            print("找到的 MD 文件:")
            for md_file in md_files:
                # print(md_file)
                # 提取文件到指定目录
                extracted_path =zip_ref.extract(md_file, copy_path)
                # 重命名文件
                new_file_path = os.path.join(copy_path, batch_id)
                os.rename(extracted_path, new_file_path)
                print(f"已提取并重命名为: {new_file_path}")
        else:
            print("ZIP 文件中没有找到 MD 文件")
    return md_files


# 异步函数用于轮询下载状态
async def download_file(task_id,topic):
    while True:
        download_url = download_url_template.format(task_id=task_id)
        response = requests.get(download_url)
        data = response.json()

        if data['message'] == "success":
            # 文件转换成功，保存base64编码的数据到文件
            # with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\markdown/{task_id}.md", 'wb') as f:
            #     f.write(base64.b64decode(data['data']))
            directory = fr"E:\PaperAgent\paper\{topic}\markdown"

            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(fr"{directory}/{task_id}.md", 'wb') as f:
                f.write(base64.b64decode(data['data']))

            print("File downloaded and saved successfully.")
            break
        elif data['message'] == "processing" or data['message'] == "waiting":
            print("File is still processing or waiting. Retrying in 5 seconds...")
            time.sleep(5)  # 等待5秒后重试
        else:
            print("Error downloading file:", data['message'])
            break

        # 运行异步下载函数

def pdf2md(file_path,topic):

    respons=upload(file_path=file_path)

    try:
        if respons["message"]=='success':
            print("----------------------")
            asyncio.run(download_file(task_id=respons['task_id'],topic=topic))
            # print(respons['task_id'])
            # download_file(task_id="1dbc18d694dc1fb7d9b997c9b6b749b1")
            return respons['task_id']
        else:
            print(f"Erro: {file_path}:上传PDF解析失败！！！")
    except:
        print(f"Erro: {file_path}:下载MD失败！！！")

    return 0


def download_file_mineruapi(batch_id,topic):
    while True:
        url = f'https://mineru.net/api/v4/extract-results/batch/{batch_id}'
        header = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIzMzEwNjUwNyIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTczOTYyMzEyNCwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwidXVpZCI6IjcxZTY1NGZhLTQ5MmYtNGJjNS04MThmLTgxZmUyMDBmZWFjMiIsImVtYWlsIjoiIiwiZXhwIjoxNzQwODMyNzI0fQ.XyGTHXyDOCbSjIkxR68vBE9kdvn22BifOSIhR7_2iAvdeRUJYEyt82mMnuvORGj-43_6nQryH8WVl1HUAp6qng"
        }
        res = requests.get(url, headers=header)
        print(res.json())

        if res.json()["data"]["extract_result"][0]["state"] == "done":
            # 文件转换成功，保存base64编码的数据到文件
            # with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\markdown/{task_id}.md", 'wb') as f:
            #     f.write(base64.b64decode(data['data']))
            directory = fr"E:\PaperAgent\paper\{topic}\markdown"
            zip_dir=fr"E:\PaperAgent\paper\{topic}\zip"
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(zip_dir):
                os.makedirs(zip_dir)

            print(res.json()["data"]["extract_result"][0]["full_zip_url"])
            print(zip_dir+fr"/{batch_id}.zip")

            download_zip_file(url=res.json()["data"]["extract_result"][0]["full_zip_url"], zip_save_path=zip_dir+fr"/{batch_id}.zip")
            find_md_files_in_zip(zip_path=zip_dir+f"/{batch_id}.zip",copy_path=directory,batch_id=f"{batch_id}.md")
            break

        elif res.json()["data"]["extract_result"][0]["state"] == "waiting-file" or res.json()["data"][0]["state"] == "running":
            print("File is still processing or waiting. Retrying in 5 seconds...")
            time.sleep(5)  # 等待5秒后重试
        else:
            print("Error downloading file:", res.json()["data"]["state"],"batch_id:",batch_id)
            break

def pdf2md_mineruapi(file_path,topic):
    # 读取 Excel 文件
    pdf_history = 'E:\PaperAgent\paper/History.xlsx'  # 替换为你的文件路径
    df = pd.read_excel(pdf_history)
    pdf_name=extract_pdf_name(path=file_path)
    # 遍历每一行
    for index, row in df.iterrows():
        if row['Paper']==pdf_name:
            download_file_mineruapi(batch_id=row['Batch_ID'], topic=topic)
            return row['Batch_ID']

    url = 'https://mineru.net/api/v4/file-urls/batch'
    header = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIzMzEwNjUwNyIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTczOTYyMzEyNCwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwidXVpZCI6IjcxZTY1NGZhLTQ5MmYtNGJjNS04MThmLTgxZmUyMDBmZWFjMiIsImVtYWlsIjoiIiwiZXhwIjoxNzQwODMyNzI0fQ.XyGTHXyDOCbSjIkxR68vBE9kdvn22BifOSIhR7_2iAvdeRUJYEyt82mMnuvORGj-43_6nQryH8WVl1HUAp6qng"
    }
    data = {
        "enable_formula": True,
        "language": "en",
        "layout_model": "doclayout_yolo",
        "enable_table": True,
        "files": [
            {"name": file_path, "is_ocr": True, "data_id": "abcd"}
        ]
    }

    try:
        response = requests.post(url, headers=header, json=data)
        if response.status_code == 200:
            result = response.json()
            # print('response success. result:{}'.format(result))
            if result["code"] == 0:
                batch_id = result["data"]["batch_id"]
                urls = result["data"]["file_urls"]
                # print('batch_id:{},urls:{}'.format(batch_id, urls))

                with open(file_path, 'rb') as f:
                    res_upload = requests.put(urls[0], data=f)

                if res_upload.status_code == 200:
                    print("upload success")
                else:
                    print("upload failed")

                download_file_mineruapi(batch_id=batch_id,topic=topic)

                # 创建新行的数据（假设你要添加一行数据）
                new_row = {'Paper': pdf_name, 'Batch_ID': batch_id}  # 替换为你的新行数据
                # 将新行添加到 DataFrame 中
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                # 保存修改后的 DataFrame 回原始文件
                df.to_excel(pdf_history, index=False)

                return batch_id
            else:
                print('apply upload url failed,reason:{}'.format(result.msg))
        else:
            print('response not success. status:{} ,result:{}'.format(response.status_code, response))
    except Exception as err:
        print(err)

    return 0


# pdf2md_mineruapi(file_path=r"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\test2.pdf",topic="pulsar")
# print(pdf2md_mineruapi(file_path=r"E:\PaperAgent\paper\Pulsar Candidate Classification\pdf/Fifty Years of Pulsar Candidate Selection_ From simple filters to a new principled real-time classification approach.pdf",topic="Pulsar Candidate Classification"))
# pdf2md_mineruapi(file_path=r"E:\PaperAgent\paper\Pulsar Candidate Classification\pdf/test.pdf", topic="Pulsar Candidate Classification")
# download_zip_file(url="https://cdn-mineru.openxlab.org.cn/pdf/607146aa-4f95-413f-ad5e-60f53ac68389.zip",save_path="E:\PaperAgent\paper\pulsar\zip/1.zip")
# download_file_mineruapi(task_id,topic)
# asyncio.run(download_file(task_id="ae72cc0779737e0d133a88c2dfc57c65"))
# pdf2md(file_path=r"E:\PaperAgent\paper\Optical counterpart of gravitational waves\pdf/Characterization of thermal effects in the Enhanced LIGO Input Optics.pdf",topic="Optical counterpart of gravitational waves")