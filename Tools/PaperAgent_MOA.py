#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/11/2 19:08
# @Author : 桐
# @QQ:1041264242
# 注意事项：
import agentscope
from agentscope import msghub
from agentscope.agents import DialogAgent, UserAgent
from agentscope.message import Msg
from agentscope.pipelines.functional import sequentialpipeline
import os
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

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
"""
Reviewer_prompt="""# Task Definition
You are a rigorous and demanding research reviewer with a keen eye for novelty and impact in research. You are required to evaluate the provided Idea draft, and typically, you do not easily give high scores. However, if the Idea draft truly demonstrates exceptional innovation, a solid theoretical foundation, or potential for significant impact, you will not hesitate to award it a high rating.

# Scoring Criteria
Each scoring item (with a maximum of 5 points, in increments of 0.5) corresponds to more detailed scoring instructions:

- Scoring:
  - Novelty: X/5
    - 5: Highly innovative, introducing entirely new technologies or significantly improving existing ones, potentially leading to new directions.
    - 3: Somewhat innovative, utilizing a few new technologies or making minor improvements to existing ones.
    - 1: Essentially replicating existing methods, lacking innovation.
  - Feasibility: X/5
    - 5: Highly feasible, with both technical requirements and resource conditions being met.
    - 3: Fairly feasible, with technical challenges that can be overcome but require effort.
    - 1: Low feasibility, with significant technical obstacles or resource constraints.
  - Problem clarity: X/5
    - 5: The problem statement is clear, specific, and practically relevant, resonating with the target audience.
    - 3: The problem is described fairly clearly but may lack some details or background.
    - 1: The problem is unclear or vague, lacking sufficient background support or difficult to understand.
  - Rationale: X/5
    - 5: Strong and reasonable motivation, with clear theoretical or practical value.
    - 3: Some motivation and value but lacking specific research background or application support.
    - 1: Insufficient or unreasonable motivation, lacking clear academic or practical significance.
  - Technical depth: X/5
    - 5: Comprehensive technical details, covering important assumptions, methods, and key parameters, with depth.
    - 3: Basically complete technical details but missing some important information or lacking specificity.
    - 1: Technical description is not detailed, lacking descriptions of key methods or implementation details.
  - Dataset relevance: X/5
    - 5: The choice of dataset is clear, sufficiently large, and highly relevant to the research question.
    - 3: The dataset is appropriate but slightly deficient in size or diversity.
    - 1: The dataset is irrelevant or too small, potentially unsuitable for the research.
  - Title effectiveness: X/5
    - 5: The title highly summarizes the research topic and is attractive.
    - 3: The title is clear but lacks sufficient attractiveness or is incompletely summarized.
    - 1: The title is too general or inappropriate, failing to accurately reflect the research content.
  - Abstract clarity and completeness: X/5
    - 5: The abstract comprehensively outlines the research background, methods, results, and significance.
    - 3: The abstract basically covers the main content but lacks some key information.
    - 1: The abstract is unclear or incomplete, making it difficult to understand the research content and significance.
  - Methodology suitability: X/5
    - 5: The chosen methods are reasonable and applicable, with high innovation.
    - 3: The methods are applicable but with moderate innovation, or slightly lower applicability.
    - 1: The methods are inappropriate or do not match the research question.
  - Experimental design rigor: X/5
    - 5: The experimental design is scientific and rigorous, including sufficient comparison and validation steps.
    - 3: The experimental design is basically reasonable but lacks validation or comparison.
    - 1: The experimental design lacks scientific rigor, failing to validate key assumptions or research objectives.

- Comments:

"""
model_configs = [
    {
        "config_name": "qwen-max-0919",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max",
        "api_key": "sk-586f6f96d2704df6901e31de27fda2fe",
    },
    {
        "config_name": "qwen-plus",
        "model_type": "dashscope_chat",
        "model_name": "qwen-plus",
        "api_key": "sk-586f6f96d2704df6901e31de27fda2fe",
    },
    {
        "config_name": "glm-4-long",
        "model_type": "openai_chat",
        "model_name": "glm-4-long",
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
    },
    {
        "config_name": "moonshot-v1-8k",
        "model_type": "openai_chat",
        "model_name": "moonshot-v1-8k",
        "api_key": "sk-u66x82yZ6tMcjRMOwkKouZDHrhrLmLGl3ghjOlxOBUuvw6MD",
        "client_args": {
            "base_url": "https://api.moonshot.cn/v1",
        },
    },
    {
        "config_name": "gemini-1.5-flash",
        "model_type": "gemini_chat",
        "model_name": "gemini-1.5-flash",
        "api_key": "AIzaSyCRuZMYqpQZAt7wlSsqXGjXcwxUekrrH4s",
    },
    {
        "config_name": "hunyuan-large",
        "model_type": "openai_chat",
        "model_name": "hunyuan-large",
        "api_key": "sk-O5wisGpuwAS6FM7ICWtOM049vWYyEGq3opa4wSf920zeimW4",
        "client_args": {
            "base_url": "https://api.hunyuan.cloud.tencent.com/v1",
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

test='''### Problem:
The identification and classification of pulsar candidates in modern astronomical surveys is a challenging task due to the vast volumes of data, the complexity of the features involved, and the presence of missing data. Existing methods, such as Bayesian networks, automated feature engineering, and deep learning models, have shown promise individually, but their integration has not been thoroughly explored. This integration could enhance the overall efficiency and accuracy of pulsar candidate classification, addressing the limitations of current methods, such as the inability to handle missing data effectively and the reliance on large labeled datasets.

### Rationale:
The proposed integrated framework leverages the strengths of Bayesian networks, automated feature engineering, and transformer-based deep learning models. Bayesian networks can model the complex probabilistic relationships between features, while automated feature engineering identifies critical synergistic feature pairs. Transformer-based models, known for their ability to handle sequential and multi-dimensional data, can further improve classification accuracy by leveraging the rich, multi-modal data typical of pulsar candidates. Additionally, time series imputation techniques and semisupervised learning methods are incorporated to handle missing data and leverage unlabeled data effectively. This integrated approach aims to provide a robust and adaptable solution for pulsar candidate classification.

### Necessary technical details:
1. **Bayesian Networks**: To model the probabilistic relationships between different features in pulsar candidate data, leveraging the scalability and uncertainty quantification of Bayesian Stein Networks (BSNs).
2. **Automated Feature Engineering (AutoFE)**: Specifically, algorithms like IIFE to identify synergistic feature pairs, coupled with AutoMAN for efficient feature transform space exploration.
3. **Transformer-based Deep Learning Models**: Vision Transformer (ViT) and Convolutional Vision Transformer (CvT) for classification, integrated with MeMOT for multi-object tracking and handling long-term occlusions.
4. **Time Series Imputation Techniques**: Deep learning methods, such as those used in MeMOT, to handle missing values in the data.
5. **Semisupervised Learning**: Self-tuning pseudolabeling techniques, as discussed in the survey on semisupervised learning, to leverage unlabeled data effectively.

### Datasets:
1. **Fermi Large Area Telescope (LAT) Data**: For high-energy gamma-ray pulsar candidate data.
2. **Pulsar Arecibo L-band Feed Array (PALFA) Survey**: For radio pulsar candidate data.
3. **Green Bank North Celestial Cap (GBNCC) Survey**: For independent validation of the AI model.
4. **Commensal Radio Astronomy FasT Survey (CRAFTS)**: For additional radio pulsar candidate data.
5. **High-Time Resolution Universe (HTRU) Survey**: For testing the classification models.

### Paper title:
"Integrated Bayesian Networks, Automated Feature Engineering, and Transformer-based Deep Learning for Enhanced Pulsar Candidate Classification"

### Paper abstract:
The identification and classification of pulsar candidates in modern astronomical surveys is a challenging task due to the vast volumes of data and the complexity of the features involved. This paper proposes a novel integrated framework that combines Bayesian networks, automated feature engineering, and transformer-based deep learning models to enhance the accuracy and efficiency of pulsar candidate classification. Bayesian networks are used to model the probabilistic relationships between features, while automated feature engineering identifies critical synergistic feature pairs. Transformer-based deep learning models, including Vision Transformer (ViT) and Convolutional Vision Transformer (CvT), are employed to classify the candidates, leveraging the rich, multi-modal data typical of pulsar surveys. Additionally, time series imputation techniques and semisupervised learning methods are incorporated to handle missing data and leverage unlabeled data effectively. The proposed framework is validated using data from the Fermi LAT, PALFA, GBNCC, CRAFTS, and HTRU surveys, demonstrating significant improvements in classification accuracy and efficiency. This integrated approach represents a significant advancement in the automated identification of pulsar candidates, with potential applications in both current and future astronomical surveys.

### Methods:
1. **Data Preprocessing**:
   - **Bayesian Networks**: Construct Bayesian networks using Bayesian Stein Networks (BSNs) to model the probabilistic relationships between different features in the pulsar candidate data.
   - **Automated Feature Engineering**: Apply IIFE algorithms to identify synergistic feature pairs and integrate AutoMAN for efficient feature transform space exploration.
   - **Time Series Imputation**: Use deep learning-based imputation techniques, similar to those in MeMOT, to handle missing values in the time series data.

2. **Modeling**:
   - **Transformer-based Deep Learning Models**: Implement Vision Transformer (ViT) and Convolutional Vision Transformer (CvT) models for the classification of pulsar candidates. These models are trained on the enhanced feature sets generated from the Bayesian networks and AutoFE.
   - **Semisupervised Learning**: Apply self-tuning pseudolabeling techniques to leverage the large volume of unlabeled data, improving the model's generalization capabilities.

3. **Evaluation**:
   - **Validation**: Use cross-validation techniques to assess the performance of the integrated model.
   - **Independent Testing**: Validate the model using independent datasets from the GBNCC, CRAFTS, and HTRU surveys.

### Experiments:
1. **Data Preparation**:
   - **Bayesian Network Construction**: Build Bayesian networks on the Fermi LAT and PALFA datasets to model feature relationships.
   - **Feature Engineering**: Apply IIFE algorithms to the PALFA and GBNCC datasets to identify synergistic feature pairs.
   - **Imputation**: Use deep learning-based imputation techniques on the HTRU dataset to handle missing values.

2. **Model Training**:
   - **Transformer Models**: Train ViT and CvT models on the enhanced feature sets from the Bayesian networks and AutoFE.
   - **Semisupervised Learning**: Apply self-tuning pseudolabeling techniques to the unlabeled data from the CRAFTS survey.

3. **Evaluation Metrics**:
   - **Classification Accuracy**: Assess the accuracy of the model using standard classification metrics (precision, recall, F1 score).
   - **Ranking Performance**: Evaluate the model's ability to rank pulsar candidates accurately using the GBNCC and HTRU datasets.

### Reference:
1. "Constraints on the Galactic Population of TeV Pulsar Wind Nebulae Using Fermi Large Area Telescope Observations"
2. "Searching for Pulsars Using Image Pattern Recognition"
3. "Millisecond pulsars phenomenology under the light of graph theory"
4. "Pulsar candidate identification using advanced transformer-based models"
5. "Enhancing Pulsar Candidate Identification with Self-tuning Pseudolabeling Semisupervised Learning"'''

def moa_idea_iteration(model_configs=model_configs,topic="",user_prompt=""):
    # 读取模型配置
    agentscope.init(model_configs=model_configs)

    system_prompt = "You are a research expert in astronomy and computer whose primary goal is to identify promising, new, and key scientific problems based on existing scientific literature, in order to aid researchers in discovering novel and significant research opportunities that can advance the field."

    # 创建一个对话智能体和一个用户智能体
    dialogAgent_Gemini = DialogAgent(name="Gemini", model_config_name="gemini-1.5-flash", sys_prompt=system_prompt)
    dialogAgent_Qwen = DialogAgent(name="Qwen", model_config_name="qwen-plus", sys_prompt=system_prompt)
    dialogAgent_DeepSeek = DialogAgent(name="DeepSeek", model_config_name="deepseek-chat", sys_prompt=system_prompt)

    dialogAgent_AC = DialogAgent(name="AC", model_config_name="deepseek-chat", sys_prompt=system_prompt)

    dialogAgent_Reviewer = DialogAgent(name="Reviewer", model_config_name="deepseek-chat", sys_prompt=system_prompt)

    Gemini_message = dialogAgent_Gemini(Msg(name="User", role="user", content=user_prompt))
    Qwen_message=dialogAgent_Qwen(Msg(name="User",role="user", content=user_prompt))
    DeepSeek_message=dialogAgent_DeepSeek(Msg(name="User",role="user", content=user_prompt))

    with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/Qwen_{topic}_iteration2.md", 'w', encoding='utf-8') as f:
        f.write(Qwen_message.content)
    with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/DeepSeek_{topic}_iteration2.md", 'w', encoding='utf-8') as f:
        f.write(DeepSeek_message.content)
    with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/Kimi_{topic}_iteration2.md", 'w', encoding='utf-8') as f:
        f.write(Gemini_message.content)

    aggregation=f"""# Task Definition
You are an expert in the intersection of astronomy and computer applications with a keen eye for novelty and impact in research. Your goal is to synthesize and refine the final version of the idea draft based on the initial drafts provided by various experts.

# Important notes:
- Ensure that your final proposed idea draft has a sufficient contribution for a new Nature or Science paper.
- Avoid ideas that are overfitted to specific past work and strive for wider significance.

# Based on initial drafts, provide a comprehensive research proposal in the following format:
### Problem:
### Rationale:
### Necessary technical details:
### Datasets:
### Paper title:
### Paper abstract:
### Methods:
### Experiments:
### Reference: 1.[Title 1], 2.[Title 2], ..., n.[Title n]
### Summary of the differences in this iteration:

# Input initial drafts:
## Expert one's initial drafts
{Qwen_message.content}
## Expert two's initial drafts
{DeepSeek_message.content}
## Expert thrid's initial drafts
{Gemini_message.content}"""

    AC_message = dialogAgent_AC(Msg(name="User", role="user", content=aggregation))

    with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/AC_{topic}_iteration2.md", 'w', encoding='utf-8') as f:
        f.write(AC_message.content)

    Reviewer_message = dialogAgent_Reviewer(Msg(name="User", role="user", content=Reviewer_prompt))

    with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/Reviewer_{topic}_iteration2.md", 'w', encoding='utf-8') as f:
        f.write(Reviewer_message.content)

    # 打印模型 API 的使用情况
    agentscope.print_llm_usage()

    return AC_message.content

def moa_model(model_configs,agent_list,topic,user_prompt,systeam_prompt,ac_prompt="",ac_systeam="",stage=""):
    """
    :param model_configs:
    :param agent_list:
     {
     main:
     helper:['llm1','llm2','llm3']
     }
    :param topic:
    :param user_prompt:
    :param systeam_prompt:
    :param aggregation_prompt:
    :return:
    """
    # 读取模型配置
    agentscope.init(model_configs=model_configs)
    system_prompt = "You are an expert in the intersection of astronomy and computer applications whose primary goal is to identify promising, new, and key scientific problems based on existing scientific literature, in order to aid researchers in discovering novel and significant research opportunities that can advance the field."
    agents = {}

    for llm in agent_list['helper']:
        agent = DialogAgent(name=llm, model_config_name=llm, sys_prompt=system_prompt)
        agents[llm] = agent

    messages = {}
    for agent_key in agents:
        agent = agents[agent_key]
        message = agent(Msg(name="user", role="user", content=user_prompt))
        messages[agent_key] = message

    for message_key in messages:
        with open(
                fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/{message_key}_{topic}_{stage}.md",
                'w', encoding='utf-8') as f:
            f.write(messages[message_key].content)

    if ac_prompt!="" and agent_list['main']!="":
        AC=DialogAgent(name="AC", model_config_name=agent_list['main'], sys_prompt=ac_systeam)
        AC_message=AC(Msg(name="user", role="user", content=ac_prompt))
        with open(
                fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/AC_{topic}_{stage}.md",
                'w', encoding='utf-8') as f:
            f.write(AC_message.content)

    # 打印模型 API 的使用情况
    agentscope.print_llm_usage()

def moa_table(model_configs=model_configs,topic='',draft=test):
    # agentscope.studio.init()
    agentscope.init(model_configs=model_configs)# ,logger_level="DEBUG",save_log=True

    role="You are a seminar reviewer responsible for evaluating research idea drafts. When reviewing, take into account the content of the draft as well as feedback from other reviewers. While recognizing the value in others' comments, your focus should be on providing a unique perspective that enhances and optimizes the draft. Your feedback should be concise, consisting of a well-constructed paragraph that builds on the ongoing discussion without replicating other reviewers' suggestions. Always strive to present your distinct viewpoint."
    viewer="""Act a moderator in a seminar.  After the four reviewers have completed their evaluations, you will need to comprehensively analyze the content of the idea draft as well as the valuable review comments provided by each reviewer. Based on this, you are required to systematically summarize and integrate these review opinions, ensuring that all key feedback and suggestions are accurately and comprehensively considered. The output should strictly follow the format below:
# Overall Opinions:

# Iterative Optimization Search Keywords:
- [Keyword 1] - [Search suggestion]
- [Keyword 2] - [Search suggestion]
- ..."""

    dialogAgent_Qwen = DialogAgent(name="Reviewer 1", model_config_name="qwen-plus", sys_prompt=role) #"qwen-max-0919"
    dialogAgent_Gemini = DialogAgent(name="Reviewer 2", model_config_name="gemini-1.5-flash",sys_prompt=role)  # "gemini-1.5-flash"
    dialogAgent_DeepSeek = DialogAgent(name="Reviewer 3", model_config_name="deepseek-chat", sys_prompt=role)
    userAgent = UserAgent(name="Reviewer 4")

    dialogAgent_Viewer= DialogAgent(name="Viewer", model_config_name="deepseek-chat", sys_prompt=viewer)

    # # 在Pipeline结构中执行对话循环
    # x = None
    # while x is None or x.content != "exit":
    #     x = sequentialpipeline([userAgent,dialogAgent_Gemini, dialogAgent_Qwen,dialogAgent_DeepSeek])
    #     print(x.content)

    with msghub(participants=[dialogAgent_Gemini, dialogAgent_Qwen, dialogAgent_DeepSeek,userAgent,dialogAgent_Viewer]) as hub:
        # Broadcast a message to all participants
        hub.broadcast(Msg(name="Host",role="user", content=f"Welcome to join the seminar chat! Now, The idea draft we need to discuss as follows:\n{draft}"))

        dialogAgent_Qwen()
        dialogAgent_Gemini()
        dialogAgent_DeepSeek()
        userAgent()
        viewer_message=dialogAgent_Viewer()

    with open(fr"C:\Users\10412\Desktop\多模态大语言模型\Code\天文Code\PaperAgent\Paper_Ori\moa/{topic}_review_moa.md", 'w', encoding='utf-8') as f:
        f.write(viewer_message.content)

    # 打印模型 API 的使用情况
    agentscope.print_llm_usage()

# if __name__ == "__main__":
#
#     moa_table(model_configs=model_configs,topic='photometric classification (stars and calaxies,stars and quasars,supernovas)',draft='')

    # moa_idea_iteration(model_configs=model_configs, topic="Pulsar Candidate Classification", user_prompt="hello")
    # # 来自Alice的简单文本消息示例
    # message_from_alice = Msg("Alice", "Hi!")

    # dict={
    #  'main':'deepseek-chat',
    #  'helper':['deepseek-chat','qwen-max-0919']
    # }
    #
    # moa_model(model_configs=model_configs, agent_list=dict, topic='', user_prompt='hello', systeam_prompt='', aggregation_prompt="")

