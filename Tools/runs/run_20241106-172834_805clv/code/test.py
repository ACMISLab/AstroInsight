#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/11/2 15:35
# @Author : 桐
# @QQ:1041264242
# 注意事项：
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
这里有一个简单的示例，展示了如何在 Agentscope 中与 MoA 进行对话。
"""
from typing import Optional, Union, Sequence

import agentscope
from agentscope.agents import AgentBase, UserAgent
from MoA import MixtureOfAgents
from agentscope.message import Msg


class DialogAgentWithMoA(AgentBase):
    """一个简单的用于执行对话的代理。
    我们将展示所有需要修改的地方以便使用 MoA 作为主要模型"""

    def __init__(
            self,
            name: str,
            moa_module: MixtureOfAgents,  # 改为传递 moa_module
            use_memory: bool = True,
    ) -> None:
        """初始化对话代理。

        参数:
            name (`str`):
                代理的名字。
            sys_prompt (`Optional[str]`):
                代理的系统提示，可以通过参数传递或硬编码在代理中。
            moa_module (`MixtureOfAgents`):
                初始化后想要作为主要模块使用的 MoA 模块。
            use_memory (`bool`, 默认为 `True`):
                代理是否具有记忆功能。
        """
        super().__init__(
            name=name,
            sys_prompt="",
            use_memory=use_memory,
        )
        self.moa_module = moa_module  # 将 model 初始化改为 moa_module

    def reply(self, x: Optional[Union[Msg, Sequence[Msg]]] = None) -> Msg:
        """代理的回复函数。处理输入数据，使用当前的对话记忆和系统提示生成一个提示，
        并调用语言模型来产生响应。然后格式化响应并将其添加到对话记忆中。

        参数:
            x (`Optional[Union[Msg, Sequence[Msg]]]`, 默认为 `None`):
                传入代理的输入消息，如果代理不需要任何输入也可以省略。

        返回:
            `Msg`: 由代理生成的输出消息。
        """
        # 如果需要，则记录输入
        if self.memory:
            self.memory.add(x)

        # 使用模块如下：
        response = self.moa_module(
            Msg("system", self.sys_prompt, role="system"),
            self.memory
            and self.memory.get_memory()
            or x,  # type: ignore[arg-type]
        )

        msg = Msg(self.name, response, role="assistant")

        # 以本代理的声音打印/说出消息
        self.speak(msg)

        # 记录消息到记忆中
        if self.memory:
            self.memory.add(msg)

        return msg

if __name__ == "__main__":
    # 填写你的 API 密钥，或者使用 vllm 或 ollama 托管本地模型。
    model_configs = [
        {
            "config_name": "qwen-max-0919",
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": "sk-586f6f96d2704df6901e31de27fda2fe",
        },
        {
            "config_name": "glm-4-plus",
            "model_type": "openai_chat",
            "model_name": "glm-4-plus",
            "api_key": "1cf7ad6057486482907576343cdfad25.Pj3NWFDgjyjNqDVK",
            "client_args": {
                "base_url": "https://open.bigmodel.cn/api/paas/v4/",
            },
        },
        {
            "config_name": "deepseek-chat",
            "model_type": "openai_chat",
            "model_name": "deepseek-chat",
            "api_key": "sk-80cc66e836004e6ca698eb35206dd418",
            "client_args": {
                "base_url": "https://api.deepseek.com/v1",
            },
        }
        # {
        #     "config_name": "chatgpt-4o-latest",
        #     "model_type": "openai_chat",
        #     "model_name": "chatgpt-4o-latest",
        #     "api_key": "sk-gT9nO93CQQKoNb1KTUuGIeV1b05DUkYF0ZJjngcDev12RiuY",
        #
        #     "client_args": {
        #         "base_url": "https://api.openai-proxy.org/v1/",
        #     },
        # },
    ]

    agentscope.init(model_configs=model_configs, project="Mixture of Agents")

    user_agent = UserAgent()

    # your_moa_module = MixtureOfAgents(
    #     main_model="qwen-max-0919",  # 使用的模型
    #     reference_models=["chatgpt-4o-latest", "glm-4-plus", "deepseek-chat"],
    #     show_internal=False,  # 设置为 True 以查看 MoA 模块的内部情况
    #     rounds=3,  # 可以从 0 到无穷大
    # )

    your_moa_module = MixtureOfAgents(
        main_model="deepseek-chat",  # 使用的模型
        reference_models=["deepseek-chat", "qwen-max-0919", "glm-4-plus"],
        show_internal=True,  # 设置为 True 以查看 MoA 模块的内部情况
        rounds=3,  # 可以从 0 到无穷大
    )
    # 初始化两个代理
    dialog_agent = DialogAgentWithMoA(
        name="Assistant",
        moa_module=your_moa_module,
        use_memory=True,  # 代理是否使用记忆功能
    )
    user_agent = UserAgent()

    # 开始用户与助手之间的对话
    while True:
        q = user_agent(None)
        if q.content == "exit":  # 输入 "exit" 以中断循环
            break
        q = dialog_agent(q)