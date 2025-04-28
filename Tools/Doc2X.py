#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/11/12 18:20
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import base64
import json
import time
import requests as rq

base_url = "https://v2.doc2x.noedgeai.com"
secret = "sk-si892b4hpe0v5o6r2rxxqlwbs7crudii"

def preupload():
    url = f"{base_url}/api/v2/parse/preupload"
    headers = {
        "Authorization": f"Bearer {secret}"
    }
    res = rq.post(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data["code"] == "success":
            return data["data"]
        else:
            raise Exception(f"get preupload url failed: {data}")
    else:
        raise Exception(f"get preupload url failed: {res.text}")

def put_file(path: str, url: str):
    with open(path, "rb") as f:
        res = rq.put(url, data=f) # body为文件二进制流
        if res.status_code != 200:
            raise Exception(f"put file failed: {res.text}")

def get_status(uid: str):
    url = f"{base_url}/api/v2/parse/status?uid={uid}"
    headers = {
        "Authorization": f"Bearer {secret}"
    }
    res = rq.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data["code"] == "success":
            return data["data"]
        else:
            raise Exception(f"get status failed: {data}")
    else:
        raise Exception(f"get status failed: {res.text}")

def pdf2md_docx2(file_path=r""):
    upload_data = preupload()
    print(upload_data)
    url = upload_data["url"]
    uid = upload_data["uid"]

    put_file(path=file_path, url=url)

    while True:
        status_data = get_status(uid)
        print(status_data)
        if status_data["status"] == "success":
            result = status_data["result"]
            contents=""
            for content in result["pages"]:
                try:
                    contents+=content["md"]
                except:
                    print(f"Erro: {file_path}:下载MD缺页！！！")

            # print(contents)

            with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\markdown/{uid}.md", 'w',encoding='utf-8') as f:
                f.write(contents)
            print("File downloaded and saved successfully.")
            return uid
                # json.dump(result, f)
            # break
        elif status_data["status"] == "failed":
            detail = status_data["detail"]
            raise Exception(f"parse failed: {detail}")

            return 0
        elif status_data["status"] == "processing":
            # processing
            progress = status_data["progress"]
            print(f"progress: {progress}")
            time.sleep(3)
