#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/7/7 17:26
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import json
import os

import tiktoken
from openai import OpenAI
from datetime import datetime
from http import HTTPStatus
import dashscope
# import datetime

DHA=r"DeepSeekV2_History.json"
Key=OpenAI(api_key="Fill in your DeepSeek API", base_url="https://api.deepseek.com/v1")
system_prompt="You are a research expert in astronomy and computer whose primary goal is to identify promising, new, " \
              "and key scientific problems based on existing scientific literature, in order to aid researchers in discovering novel and significant research opportunities that can advance the field."

# 假设DeepSeekV2模型的定价是每个token 0.0001美元
TOKEN_PRICE_USD = 0.0001
total_tokens_used = 0

def calculate_token_cost(content, model_name="gpt-3.5-turbo"):
    # 使用tiktoken库来计算token数量
    enc = tiktoken.encoding_for_model(model_name)
    tokens = enc.encode(content)
    token_count = len(tokens)

    # 计算费用
    cost_usd = token_count * TOKEN_PRICE_USD
    # print(f"Token total: {token_count}")
    # print(f"Consumption expenses: r{cost_usd:.6f}")

    global total_tokens_used
    total_tokens_used += token_count

    # 将总token数写入到文件中
    with open(r'token_usage.txt', 'a') as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{current_time} - Total tokens used: {total_tokens_used}\n")

    print(f"\033[1;32m | INFO     | Have used total tokens：{total_tokens_used} \033[0m")

    return token_count, cost_usd

def is_json_file_empty(file_path):
    """
    判断指定的 JSON 文件内容是否为空。

    参数:
    file_path (str): JSON 文件的路径。

    返回:
    bool: 如果文件为空或内容为空，则返回 True；否则返回 False。
    """

    # 检查文件是否存在以及文件大小是否为0
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 '{file_path}' 不存在。")
    if os.path.getsize(file_path) == 0:
        return True
        # 读取并解析 JSON 文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 判断 JSON 内容是否为空
        return not bool(data)  # 如果 data 是空字典或空列表，返回 True
    except json.JSONDecodeError:
        raise ValueError(f"文件 '{file_path}' 不是有效的 JSON 文件。")

def call_with_deep(question,history_adress=DHA,historyOpen=False,character="robot",system_prompt=system_prompt,temperature=0.7,cost=False):
    client = Key

    messages=[]
    temp_info=[]
    messages_info=[]

    if historyOpen == True and is_json_file_empty(history_adress) == False:
        try:
            with open(history_adress, 'r', encoding='utf-8') as file:
                messages_info = json.load(file)

            for info in messages_info:
                 for message in info["message"]:
                     messages.append(message)

            temp_info.append({"role": "user", "content": question})
            messages.append({"role": "user", "content": question})

        except:
            print(f"\033[1;32m | ERRO     | can't open the file: {history_adress} \033[0m")

    else:
        temp_info.append({"role": "system", "content": system_prompt})
        temp_info.append({"role": "user", "content": question})
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]

    # print(f"-----------------\n{messages}-------------------\n")

    # print(messages)
    response = client.chat.completions.create(
        model="deepseek-chat",
        temperature=temperature,
        messages = messages
    )

    calculate_token_cost(content=question+system_prompt+response.choices[0].message.content)

    temp_info.append({"role": "assistant", "content": response.choices[0].message.content})

    messages_info.append({
        "time:": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "character":character,
        "message":temp_info
    })

    try:
        with open(history_adress, 'w', encoding='utf-8') as file:
            json.dump(messages_info, file, indent=4,ensure_ascii=False)
    except Exception as e:
        print(f"\033[1;32m | INFO     | can't write in  the file {history_adress} - {e} \033[0m")

    print("\033[1;32m  call_with_deep ok! \033[0m")
    return response.choices[0].message.content

def call_with_deep_code(question,history):
    client = Key
    response = client.chat.completions.create(
        model="deepseek-coder",
        temperature=0.7,
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question},
        ]
    )
    return response.choices[0].message.content

def call_with_deep_jsonout(system_prompt,question):

    client = Key

    if system_prompt=="":
        system_prompt = """
        The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 
    
        EXAMPLE INPUT: 
        Which is the highest mountain in the world? Mount Everest.
    
        EXAMPLE JSON OUTPUT:
        {
            "question": "Which is the highest mountain in the world?",
            "answer": "Mount Everest"
        }
        """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    # print(response.choices[0].message.content)
    # print(json.loads(response.choices[0].message.content))
    # print("call_with_deep_jsonout ok!")
    calculate_token_cost(content=question + system_prompt + response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)

def call_with_deep_code_jsonout(question,history):
    client = Key
    system_prompt = """
    The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

    EXAMPLE INPUT: 
    Which is the highest mountain in the world? Mount Everest.

    EXAMPLE JSON OUTPUT:
    {
        "question": "Which is the highest mountain in the world?",
        "answer": "Mount Everest"
    }
    """
    messages = client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.7,
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question},
        ]
    )
    response = client.chat.completions.create(
        model="deepseek-coder",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )
    return json.loads(response.choices[0].message.content)

def call_with_qwenmax(question,history_adress=DHA,historyOpen=False,character="robot",system_prompt=system_prompt,temperature=0.7):
    messages=[]
    temp_info=[]
    messages_info=[]

    if historyOpen == True and is_json_file_empty(history_adress) == False:
        try:
            with open(history_adress, 'r', encoding='utf-8') as file:
                messages_info = json.load(file)

            for info in messages_info:
                 for message in info["message"]:
                     messages.append(message)

            temp_info.append({"role": "user", "content": question})
            messages.append({"role": "user", "content": question})

        except:
            print(f"\033[1;32m | ERRO     | can't open the file: {history_adress} \033[0m")

    else:
        temp_info.append({"role": "system", "content": system_prompt})
        temp_info.append({"role": "user", "content": question})
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]

    # print(f"-----------------\n{messages}-------------------\n")

    # messages = [{"role":"system","content":system_prompt},
    #             {"role":"user","content":question}]

    responses = dashscope.Generation.call(
        model="qwen-max-2024-09-19",
        api_key="Fill in your Qwen API",
        messages=messages,
        stream=False,
        result_format='message',  # 将返回结果格式设置为 message
        top_p=0.8,
        temperature=0.7,
        enable_search=False
    )


    if responses.status_code == HTTPStatus.OK:
        print(responses.output.choices[0].message.content)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            responses.request_id, responses.status_code,
            responses.code, responses.message
        ))


    temp_info.append({"role": "assistant", "content": responses.output.choices[0].message.content})

    messages_info.append({
        "time:": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "character":character,
        "message":temp_info
    })


    try:
        with open(history_adress, 'w', encoding='utf-8') as file:
            json.dump(messages_info, file, indent=4,ensure_ascii=False)
    except Exception as e:
        print(f"\033[1;32m | INFO     | can't write in  the file {history_adress} - {e} \033[0m")

    print("\033[1;32m  call_with_qwenmax ok! \033[0m")
    return responses.output.choices[0].message.content

def call_with_qwenplus(question,history_adress=DHA,historyOpen=False,character="robot",system_prompt=system_prompt,temperature=0.7):
    messages=[]
    temp_info=[]
    messages_info=[]

    if historyOpen == True and is_json_file_empty(history_adress) == False:
        try:
            with open(history_adress, 'r', encoding='utf-8') as file:
                messages_info = json.load(file)

            for info in messages_info:
                 for message in info["message"]:
                     messages.append(message)

            temp_info.append({"role": "user", "content": question})
            messages.append({"role": "user", "content": question})

        except:
            print(f"\033[1;32m | ERRO     | can't open the file: {history_adress} \033[0m")

    else:
        temp_info.append({"role": "system", "content": system_prompt})
        temp_info.append({"role": "user", "content": question})
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]

    # print(f"-----------------\n{messages}-------------------\n")

    # messages = [{"role":"system","content":system_prompt},
    #             {"role":"user","content":question}]

    responses = dashscope.Generation.call(
        model="qwen-plus-2024-09-19",
        api_key="Fill in your Qwen API",
        messages=messages,
        stream=False,
        result_format='message',  # 将返回结果格式设置为 message
        top_p=0.8,
        temperature=1.2,
        enable_search=False
    )


    if responses.status_code == HTTPStatus.OK:
        print(responses.output.choices[0].message.content)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            responses.request_id, responses.status_code,
            responses.code, responses.message
        ))


    temp_info.append({"role": "assistant", "content": responses.output.choices[0].message.content})

    messages_info.append({
        "time:": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "character":character,
        "message":temp_info
    })


    try:
        with open(history_adress, 'w', encoding='utf-8') as file:
            json.dump(messages_info, file, indent=4,ensure_ascii=False)
    except Exception as e:
        print(f"\033[1;32m | INFO     | can't write in  the file {history_adress} - {e} \033[0m")

    calculate_token_cost(content=question + system_prompt + responses.output.choices[0].message.content)

    print("\033[1;32m  call_with_qwenplus ok! \033[0m")
    return responses.output.choices[0].message.content

def call_with_DeepSeek_R1_250120(question,system_prompt=system_prompt):
    client = OpenAI(
        # 从环境变量中读取您的方舟API Key
        api_key="Fill in your DeepSeek API",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": question}]
    response = client.chat.completions.create(
        # 替换 <YOUR_ENDPOINT_ID> 为您的方舟推理接入点 ID
        model="ep-20250215192803-42czf",
        messages=messages,
        stream=True,
    )
    reasoning_content = ""

    content = ""
    for chunk in response:
        if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
        else:
            content += chunk.choices[0].delta.content

    calculate_token_cost(content=question + system_prompt + content)
    print(f"r1 say:{content}")
    print("\033[1;32m  call_with_DeepSeek_R1_250120 ok! \033[0m")
    return content.strip()



# call_with_DeepSeek_R1_250120(system_prompt="You are a research assistant.",question="你好")
# call_with_qwenmax(system_prompt="You are a research assistant.",question="你好")
# call_with_qwenplus(system_prompt="You are a research assistant.",question="你好")