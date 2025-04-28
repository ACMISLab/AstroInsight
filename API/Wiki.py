#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/7/7 18:39
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import os
import json
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from wikidataintegrator import wdi_core
import zhconv
from tqdm import tqdm
from wikidata.client import Client

proxies = {
    'http': 'http://localhost:7890',
    'https': 'http://localhost:7890'
}

def findLabel(q_code):
    client = Client()
    entity = client.get(q_code, load=True)
    label = entity.label
    return label

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def traditional_to_simplified(traditional_text):
    simplified_text = zhconv.convert(traditional_text, 'zh-hans')
    return simplified_text

def process_aliases(aliases):
    if isinstance(aliases, str):
        return aliases
    elif isinstance(aliases, list):
        values = [alias['value'] for alias in aliases]
        return ','.join(values)
    else:
        return "错误的输入格式"

def getPlabel(pcode):
    with open('../props.json', 'r', encoding='utf-8') as f:
        relation_entities = json.load(f)
        for entity in relation_entities:
            if entity['id'] == pcode:
                return entity['label']
    return "Unknown"

def process_qcode(value):
    try:
        WdID = value
        wikidataItem = wdi_core.WDItemEngine(wd_item_id=WdID)
        result = wikidataItem.get_wd_json_representation()
        labels_zh = ""
        labels_en = ""
        aliases_zh = ""
        aliases_en = ""
        description_zh = ""
        description_en = ""

        if 'labels' in result:
            labels_zh = (
                result['labels']['zh-cn']['value'] if 'zh-cn' in result['labels'] else
                result['labels']['zh-hans']['value'] if 'zh-hans' in result['labels'] else
                result['labels']['zh']['value'] if 'zh' in result['labels'] else
                ''
            )
            labels_zh = traditional_to_simplified(labels_zh)
            if 'en' in result['labels']:
                labels_en = result['labels']['en']['value']
            else:
                labels_en = ""
        else:
            return None, None

        if 'descriptions' in result:
            description_zh = (
                result['descriptions']['zh-cn']['value'] if 'zh-cn' in result['descriptions'] else
                result['descriptions']['zh-hans']['value'] if 'zh-hans' in result['descriptions'] else
                result['descriptions']['zh']['value'] if 'zh' in result['descriptions'] else
                ''
            )
            description_zh = traditional_to_simplified(description_zh)

            if 'en' in result['descriptions']:
                description_en = result['descriptions']['en']['value']
            else:
                description_en = ""

        if 'aliases' in result:
            if 'zh' in result['aliases']:
                aliases_zh = (
                    [alias['value'] for alias in result['aliases']['zh-cn']] if 'zh-cn' in result['aliases'] else
                    [alias['value'] for alias in result['aliases']['zh-hans']] if 'zh-hans' in result['aliases'] else
                    [alias['value'] for alias in result['aliases']['zh']] if 'zh' in result['aliases'] else
                    []
                )
                aliases_zh = process_aliases(traditional_to_simplified(aliases_zh))
            if 'en' in result['aliases']:
                aliases_en = process_aliases(result['aliases']['en'])

        entity = {
            "Qcode": WdID,
            "label_en": labels_en,
            "label_zh": labels_zh,
            "description_en": description_en,
            "description_zh": description_zh,
            "aliases_en": aliases_en,
            "alias_zh": aliases_zh
        }

        claims = result.get('claims', [])

        for idx in claims:
            claim = claims[idx]
            for item in claim:
                PCode = ""
                dataValue = ""
                dataType = ""
                if 'mainsnak' in item:
                    if 'property' in item['mainsnak']:
                        PCode = item['mainsnak']['property']
                    if 'datatype' in item['mainsnak']:
                        dataType = item['mainsnak']['datatype']
                    if 'datavalue' in item['mainsnak']:
                        if 'value' in item['mainsnak']['datavalue']:
                            dataValue = str(item['mainsnak']['datavalue']['value'])
                            if dataType == "wikibase-item":
                                dataValue = str(item['mainsnak']['datavalue']['value']['id'])
                            if dataType == "time":
                                mytime = str(item['mainsnak']['datavalue']['value']['time'])
                                timezone = str(item['mainsnak']['datavalue']['value']['timezone'])
                                dataValue = "time:" + mytime + " " + "timezone:" + timezone
                            if dataType == "quantity":
                                amount = str(item['mainsnak']['datavalue']['value']['amount'])
                                unit = str(item['mainsnak']['datavalue']['value']['unit'])
                                if unit != "1":
                                    match = re.search(r'Q\d+', unit)
                                    unitCode = match.group(0)
                                    if unitCode:
                                        unit_label = findLabel(unitCode)
                                        unit = str(unit_label) if unit_label else ""
                                    else:
                                        unit = ""
                                dataValue = amount + unit
                            if dataType == "monolingualtext":
                                text = str(item['mainsnak']['datavalue']['value']['text'])
                                language = str(item['mainsnak']['datavalue']['value']['language'])
                                dataValue = "text:" + text + "  " + "language:" + language
                            if dataType == "commonsMedia":
                                fileName = str(item['mainsnak']['datavalue']['value'])
                                reurl = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{fileName}&prop=imageinfo&iiprop=url&format=json"
                                response = requests.get(reurl)
                                data = json.loads(response.text)
                                pages = data['query']['pages']
                                first_page_id = next(iter(pages))
                                url = pages[first_page_id]['imageinfo'][0]['url']
                                dataValue = url
                            if dataType == "globe-coordinate":
                                latitude = str(item['mainsnak']['datavalue']['value']['latitude'])
                                longitude = str(item['mainsnak']['datavalue']['value']['longitude'])
                                precision = str(item['mainsnak']['datavalue']['value']['precision'])
                                dataValue = "lat:" + latitude + ",lon:" + longitude + ",precision:" + precision
                            if dataType == "wikibase-property":
                                dataValue = str(item['mainsnak']['datavalue']['value']['id'])
                            if dataType == "geo-shape":
                                dataValue = "https://commons.wikimedia.org/w/index.php?title=" + str(
                                    item['mainsnak']['datavalue']['value'])
                            if dataType == "wikibase-item":
                                dataValue = findLabel(dataValue)
                            label = getPlabel(PCode)
                            entity[label] = dataValue
        return entity
    except Exception as e:
        print(e)
        return None

def search(query, language='en', limit=3):
    url = "https://www.wikidata.org/w/api.php"

    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'search': {query},  # 搜索文本
        'language': {language},  # 查询语言（英文）
        'type': 'item',
        'limit': {limit}  # 返回最大数目
    }

    # 访问
    get = requests.get(url=url, params=params, proxies=proxies)
    # 转为json数据
    re_json = get.json()
    #print(json.dumps(re_json, indent=2))
    return re_json["search"]

def process_and_save(value,pbar):
    entity = process_qcode(value)
    print(entity)
    pbar.update(1)


# def main():
#     search_result = search("CNN",limit=3)
#     qcodes = [item['id'] for item in search_result]
#
#     with tqdm(total=len(qcodes), desc="Processing QCodes", unit="QCode") as pbar:
#         with ThreadPoolExecutor(max_workers=64) as executor:
#             futures = {executor.submit(process_and_save, value, pbar): value for value in qcodes}
#             for future in as_completed(futures):
#                 future.result()

# if __name__ == "__main__":
#     main()