#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/11/2 12:27
# @Author : 桐
# @QQ:1041264242
# 注意事项：
# -*- coding: utf-8 -*-
# pylint: disable=C0301
""" 混合模型回答的工具模块 """

from typing import Union, List, Sequence, Tuple
import concurrent.futures
from loguru import logger

from agentscope.manager import ModelManager
from agentscope.message import Msg
from agentscope.models import ModelWrapperBase

with open(r"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\idea/Pulsar Candidate Classification_input_iteration2.md", 'r', encoding='utf-8') as file:
    IDEA_IMPROVEMENT_PROMPT = file.read()

DEFAULT_AGGREGATOR_PROMPT = """
You are an ambitious AI PhD student with a keen eye for novelty and impact in research. Your goal is to synthesize and refine ideas to produce a groundbreaking paper worthy of publication in top-tier journals like Nature or Science.

Based on Input Ideas, provide a comprehensive research proposal in the following format:

1. Reflection:
   a) Novelty Assessment: [Analyze how each idea compares with existing literature. Identify any significant overlaps or unique aspects.]
   b) Impact Evaluation: [Discuss the potential impact and wider significance of each idea. Consider how they might advance the field of AI and machine learning.]
   c) Technical Feasibility: [Evaluate the technical feasibility of each idea and consider the resources required for implementation. Identify any potential challenges or limitations.]
   d) Synthesis Process: [Explain how you synthesized the most promising elements from all ideas into a cohesive, innovative research proposal. Describe your decision-making process and rationale.]

2. Problem:
   [Clearly state the research problem or question being addressed]

3. Rationale:
   [Explain why this problem is important and how it advances the field]

4. Necessary technical details:
   [Outline the key technical approaches, methodologies, or algorithms needed]

5. Datasets:
   [Specify any datasets that would be required or beneficial for this research]

6. Paper title:
   [Propose a concise, engaging title for the research paper]

7. Paper abstract:
   [Write a compelling abstract (150-250 words) summarizing the proposed research, its novelty, methodology, and potential impact]

Important notes:
- Be a harsh critic for novelty in your evaluation.
- Ensure that your final proposed idea has a sufficient contribution for a new Nature or Science paper.
- Avoid ideas that are overfitted to specific past work and strive for wider significance.
- The Reflection section should provide a comprehensive overview of your critical thinking process.
- The rest of the sections should present a clear and concise research proposal.

Input Ideas:
"""  # noqa

# IDEA_IMPROVEMENT_PROMPT = """You are an AI assistant specialized in improving and refining research ideas for technical papers. Your task is to enhance the given idea or generate new impactful and creative ideas based on the user's interested topic and directions. Consider the following guidelines:
#
# 1. Focus solely on idea improvement and refinement.
# 2. Assume you don't have access to additional resources or datasets.
# 3. Ensure the idea is not overfitted to specific past work and has wider significance.
# 4. With each iteration, strive to make the idea more innovative, feasible, and impactful.
#
# For each iteration, provide your response in the following format:
#
# THOUGHT:
# <Your analysis and reasoning>
#
# IMPROVED IDEA:
# <The improved or new idea>
#
# In the THOUGHT section:
# - Briefly discuss your intuitions and motivations for the improvements.
# - Detail your high-level plan, necessary design choices, and ideal outcomes of the experiments.
# - Justify how the improved idea differs from and enhances the previous version or existing ideas.
#
# In the IMPROVED IDEA section, include the following fields:
# - "Name": A shortened descriptor of the idea (lowercase, no spaces, underscores allowed).
# - "Title": A title for the idea, to be used for report writing.
# - "Experiment": An outline of the implementation (e.g., which functions need to be added or modified, how results will be obtained).
# - "Interestingness": A rating from 1 to 10 (lowest to highest).
# - "Feasibility": A rating from 1 to 10 (lowest to highest).
# - "Novelty": A rating from 1 to 10 (lowest to highest).
#
# Be cautious and realistic in your ratings. As you progress through iterations, aim to incrementally improve these ratings while maintaining a balance between innovation and practicality.
#
# Remember, your goal is to refine and enhance the research idea with each iteration, making it more robust, innovative, and valuable to the field of study.
# """


class MixtureOfAgents:
    """
    MoA 模型，采用多个模型并汇总它们的响应，
    利用多个语言模型（LLMs）的集体优势来增强性能。
    """

    def __init__(
            self,
            main_model: Union[str, ModelWrapperBase],
            reference_models: List[Union[str, ModelWrapperBase]],
            rounds: int = 1,
            aggregator_prompt: str = DEFAULT_AGGREGATOR_PROMPT,
            show_internal: bool = False,
    ) -> None:
        """
        参数:
            main_model (`Union[str, ModelWrapperBase]`):
                主模型将在最后一轮进行最终汇总，
                概述所有先前模型的响应。
                输入可以是模型配置名称或模型实例。
            reference_models (`List[Union[str, ModelWrapperBase]]`):
                在每轮中用于生成不同响应的参考模型。
                输入可以是模型配置名称或模型实例。
                我们鼓励使用不同的模型以获得更好的多样性。
                经验上，异质模型产生的响应比同质模型更有贡献。
            rounds (`int`):
                用于细化响应的处理轮次。
                范围可以从 0 到无穷大。
            aggregator_prompt (`str`):
                用于汇总响应的提示。
                默认使用 MoA 论文中的提示。
            show_internal (`bool`):
                是否显示 MoA 的内部处理过程。
        """
        model_manager = ModelManager.get_instance()

        # 初始化主模型
        if isinstance(main_model, str):
            self.main_model = model_manager.get_model_by_config_name(main_model)
        elif isinstance(main_model, ModelWrapperBase):
            self.main_model = main_model
        else:
            raise ValueError("main_model 必须是字符串或 ModelWrapperBase 实例")

        # 初始化参考模型
        self.reference_models: List[ModelWrapperBase] = []
        for ref_model in reference_models:
            if isinstance(ref_model, str):
                self.reference_models.append(
                    model_manager.get_model_by_config_name(ref_model)
                )
            elif isinstance(ref_model, ModelWrapperBase):
                self.reference_models.append(ref_model)
            else:
                raise ValueError(
                    "reference_models 必须是字符串列表或 ModelWrapperBase 实例列表"
                )
        self.references: List[str] = ["" for _ in range(len(self.reference_models))]
        self.rounds = rounds
        self.aggregator_prompt = aggregator_prompt
        self.show_internal = show_internal
        self.idea_improvement_prompt = IDEA_IMPROVEMENT_PROMPT  # 假设 IDEA_IMPROVEMENT_PROMPT 已在其他地方定义

    def _get_res_with_aggregate_model(
            self,
            aggre_model: ModelWrapperBase,
    ) -> str:
        messages = []
        messages.append(
            Msg(role="system", content=self.aggregator_prompt, name="system"),
        )
        for i, ref in enumerate(self.references, start=0):
            messages.append(
                Msg(
                    role="user",
                    content=ref,
                    name=f"Model_{i}",
                ),
            )
        aggre_format_msg = aggre_model.format(messages)
        aggre_res = aggre_model(aggre_format_msg)
        return aggre_res.text

    def __call__(
            self,
            *args: Union[Msg, Sequence[Msg]],
    ) -> str:
        """
        根据消息获取模型响应。
        等同于调用模型:
            ```
            format_msg = model.format(messages)
            return model(format_msg)
            ```

        参数:
            *args (`Union[Msg, Sequence[Msg]]`):
                需要发送到模型的消息。
        """

        def _process_reference(
                i: int,
                ref_model: ModelWrapperBase,
                *args: Union[Msg, Sequence[Msg]],
        ) -> Tuple[int, str]:
            system_msg = Msg(role="system", content=self.idea_improvement_prompt, name="system")
            user_msg = Msg(role="user",
                           content="Please generate an initial research idea based on the following context:",
                           name="user")

            if isinstance(args[0], Msg):
                messages = [system_msg, user_msg] + list(args)
            else:
                messages = [system_msg, user_msg] + list(args[0])

            format_msg = ref_model.format(*messages)  # 注意这里使用了解包操作符 *
            ref_model_res = ref_model(format_msg)
            return i, ref_model_res.text

        def _process_new_refs(
                i: int,
                ref_model: ModelWrapperBase,
        ) -> Tuple[int, str]:
            system_msg = Msg(role="system", content=self.idea_improvement_prompt, name="system")
            user_msg = Msg(role="user", content=f"Current idea:\n{self.references[i]}\n\nPlease improve this idea.",
                           name="user")

            messages = [system_msg, user_msg]

            format_msg = ref_model.format(*messages)  # 注意这里使用了解包操作符 *
            new_res = ref_model(format_msg)
            return i, new_res.text

        # 获取所有参考响应
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(_process_reference, i, ref_model, *args)
                for i, ref_model in enumerate(self.reference_models, start=0)
            ]
            for future in concurrent.futures.as_completed(futures):
                i, result = future.result()
                self.references[i] = result
                if self.show_internal:
                    logger.info(f"第 0 轮, Model_{i}: {result}")

        for r in range(self.rounds):
            if self.show_internal:
                logger.info("=" * 20)
            new_refs = ["" for _ in range(len(self.reference_models))]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(_process_new_refs, i, ref_model)
                    for i, ref_model in enumerate(
                        self.reference_models,
                        start=0,
                    )
                ]
                for future in concurrent.futures.as_completed(futures):
                    i, result = future.result()
                    new_refs[i] = result
                    if self.show_internal:
                        print(f"第 {r + 1} 轮, Model_{i}: {result}")
            self.references = new_refs

        final_res = self._get_res_with_aggregate_model(self.main_model)
        return final_res