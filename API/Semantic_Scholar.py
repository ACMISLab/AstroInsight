#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/7/5 20:14
# @Author : 桐
# @QQ:1041264242
# 注意事项：

import requests
import json

# Define a separate function to make a request to the paper details endpoint using a paper_id. This function will be used later on (after we call the paper search endpoint).
def get_paper_data(paper_id):
  url = 'https://api.semanticscholar.org/graph/v1/paper/' + paper_id

  # Define which details about the paper you would like to receive in the response
  paper_data_query_params = {'fields': 'title,year,abstract,authors.name'}

  # Send the API request and store the response in a variable
  response = requests.get(url, params=paper_data_query_params)
  if response.status_code == 200:
    return response.json()
  else:
    return None

def get_paper_ID(query,limit=3):
    # Define the API endpoint URL
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'

    # Define the required query parameter and its value (in this case, the keyword we want to search for)
    query_params = {
        'query': {query},
        'limit': {limit}
    }
    # Make the GET request to the paper search endpoint with the URL and query parameters
    search_response = requests.get(url, params=query_params)

    # Check if the request was successful (status code 200)
    if search_response.status_code == 200:
        search_response = search_response.json()

        print(json.dumps(search_response, indent=2))
        # Retrieve the paper id corresponding to the 1st result in the list
        paper_id = search_response['data'][0]['paperId']

        # Retrieve the paper details corresponding to this paper id using the function we defined earlier.
        paper_details = get_paper_data(paper_id)

        # Check if paper_details is not None before proceeding
        if paper_details is not None:
            print(paper_details)
        else:
            print("Failed to retrieve paper details.")
    else:
        # Handle potential errors or non-200 responses
        print(f"Relevance Search Request failed with status code {search_response.status_code}: {search_response.text}")
    return paper_id

def get_paper_All(paper_id):
    # 构造请求的URL
    url = f"https://api.semanticscholar.org/v1/paper/{paper_id}"
    # 发起请求
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        paper_info = response.json()
        print(paper_info)  # 打印文章信息
    else:
        print(f"请求失败，状态码：{response.status_code}")

def get_paper_recommendations(paper_id,limit=10):
    #获取该篇论文的10篇推荐论文
    # 设置 API 的基础 URL
    base_url = "https://api.semanticscholar.org/recommendations/v1"

    # 指定要请求的论文推荐的 API 路径和参数
    path = f"/papers/forpaper/{paper_id}"
    params = {
        "limit": {limit},  # 请求返回的推荐论文数量
        "fields": "title,authors,year"  # 请求返回的字段
    }

    # 发起 GET 请求
    response = requests.get(f"{base_url}{path}", params=params)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析响应内容
        recommendations = response.json()
        print(json.dumps(recommendations, indent=2))
    else:
        print(f"Error: {response.status_code}")

# # Directly define the API key (Reminder: Securely handle API keys in production environments)
# api_key = 'your api key goes here'  # Replace with the actual API key
#
# # Define headers with API key
# headers = {'x-api-key': api_key}

# # Send the API request
# response = requests.get(url, params=query_params, headers=headers)
# response = requests.get(url, params=query_params)

# get_paper_ID(query="Pulsar",limit=10)
# print(get_paper_data(paper_id="0efac5ee88d0f0a50f2e5dbb8e7688a3b5643070"))
# print(get_paper_All(paper_id="0efac5ee88d0f0a50f2e5dbb8e7688a3b5643070"))
# print(get_paper_recommendations(paper_id="0efac5ee88d0f0a50f2e5dbb8e7688a3b5643070"))
