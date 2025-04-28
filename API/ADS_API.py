#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/7/24 21:18
# @Author : 桐
# @QQ:1041264242
# 注意事项：

# import the requests package and set your token in a variable for later use
import json
import requests
from urllib.parse import urlencode, quote_plus

token="Fill in your ADS API"
proxies ={
'http': 'http://localhost:7890',
'https': 'http://localhost:7890'
}

def search_title(query,max_results=10,sort="citation_count desc"):
    #sort:"citation_count desc" or "date desc"
    print(f"Info: Using ADS to retrieve relevant papers...")
    encoded_query = urlencode({"q": f"title:{query}",
                               "fl": "citation_count,title,abstract,comment,keyword,doi",
                               "rows": max_results,
                               "sort":sort
                               })
    results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + token},proxies=proxies)

    # format the response in a nicely readable format
    # 使用json.dumps来格式化输出
    formatted_json = json.dumps(results.json()["response"], indent=4)

    print(formatted_json)

    print(f"Info: Using ADS to retrieve relevant papers. State: OK!")

    return results.json()["response"]

def search_title_DataAndCite(query,max_results=10):
    #sort:"citation_count desc" or "date desc"

    print(f"\033[1;32m  | INFO     | Using ADS to retrieve relevant papers... \033[0m")

    cite_num=max_results//2

    date_num=max_results-cite_num

    # print(cite_num)
    # print(date_num)

    #get cite paper
    encoded_query = urlencode({"q": f"title:{query}",
                               "fl": "citation_count,title,abstract,comment,keyword,doi",
                               "rows": int(cite_num),
                               "sort": "citation_count desc"
                               })
    cite_results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + token},proxies=proxies)

    # get date paper
    encoded_query = urlencode({"q": f"title:{query}",
                               "fl": "citation_count,title,abstract,comment,keyword,doi",
                               "rows": int(date_num),
                               "sort":"date desc"
                               })

    date_results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + token},proxies=proxies)

    # format the response in a nicely readable format
    # 使用json.dumps来格式化输出
    results=cite_results.json()["response"]

    for message in date_results.json()["response"]["docs"]:
        results["docs"].append(message)

    # cite_formatted_json = json.dumps(cite_results.json()["response"], indent=4)
    # date_formatted_json = json.dumps(date_results.json()["response"], indent=4)
    formatted_json = json.dumps(results, indent=4)

    # print(cite_formatted_json)
    # print("--------------------------------------------")
    # print(date_formatted_json)

    print(formatted_json)

    print(f"\033[1;32m  | INFO     | Using ADS to retrieve relevant papers. State: OK! \033[0m")
    return results

def search_abs(query,max_results=10):
    encoded_query = urlencode({"q": f"abs:{query}",
                               "fl": "citation_count,title,abstract,doi",
                               "rows": {max_results},
                               "sort":"citation_count desc"
                               })
    results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + token})

    # format the response in a nicely readable format
    # 使用json.dumps来格式化输出
    formatted_json = json.dumps(results.json()["response"], indent=4)
    print(formatted_json)

def search_full(query,max_results=10):
    encoded_query = urlencode({"q": f"full:{query}",
                               "fl": "citation_count,title,abstract,doi",
                               "rows": {max_results},
                               "sort":"citation_count desc"
                               })
    results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + token})

    # format the response in a nicely readable format
    # 使用json.dumps来格式化输出
    formatted_json = json.dumps(results.json()["response"], indent=4)
    print(formatted_json)


# results = search_ads("black holes")
# if results:
#     print(json.dumps(results, indent=2))
# else:
#     print("Failed to retrieve data")

# print(search_title_DataAndCite(query="A Blueprint for Public Engagement Appraisal_ Supporting Research Careers",max_results=4))

# search_abs(query="pulsar")
# search_full(query="pulsar")
# result=search_title_DataAndCite(query="Pulsar Candidate Classification",max_results=10)

# print(result)