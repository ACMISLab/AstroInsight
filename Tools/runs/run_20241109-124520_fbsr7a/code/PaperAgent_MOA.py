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


system_prompt="You are an expert in the intersection of astronomy and computer applications whose primary goal is to identify promising, new, and key scientific problems based on existing scientific literature, in order to aid researchers in discovering novel and significant research opportunities that can advance the field."
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

def moa_idea_iteration(model_configs,topic,user_prompt):
    # 读取模型配置
    agentscope.init(model_configs=model_configs)

    # 创建一个对话智能体和一个用户智能体
    dialogAgent_Gemini = DialogAgent(name="Gemini", model_config_name="gemini-1.5-flash", sys_prompt=system_prompt)
    dialogAgent_Qwen = DialogAgent(name="Qwen", model_config_name="qwen-max-0919", sys_prompt=system_prompt)
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
### Reference: [Title 1], [Title 2], ..., [Title n]

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

def moa_table(model_configs,topic=''):
    # agentscope.studio.init()
    agentscope.init(model_configs=model_configs)# ,logger_level="DEBUG",save_log=True

    role="You are a seminar reviewer responsible for evaluating research idea drafts. When reviewing, take into account the content of the draft as well as feedback from other reviewers. While recognizing the value in others' comments, your focus should be on providing a unique perspective that enhances and optimizes the draft. Your feedback should be concise, consisting of a well-constructed paragraph that builds on the ongoing discussion without replicating other reviewers' suggestions. Always strive to present your distinct viewpoint."
    viewer="""Act a moderator in a seminar.  After the four reviewers have completed their evaluations, you will need to comprehensively analyze the content of the idea draft as well as the valuable review comments provided by each reviewer. Based on this, you are required to systematically summarize and integrate these review opinions, ensuring that all key feedback and suggestions are accurately and comprehensively considered. The output should include the following:
# Overall opinions:

# Iterative Optimization Search Keywords:
- [Keyword 1] - [Search suggestion]
- [Keyword 2] - [Search suggestion]
- ..."""

    dialogAgent_Qwen = DialogAgent(name="Reviewer 1", model_config_name="deepseek-chat", sys_prompt=role) #"qwen-max-0919"
    dialogAgent_Gemini = DialogAgent(name="Reviewer 2", model_config_name="deepseek-chat",sys_prompt=role)  # "gemini-1.5-flash"
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
        hub.broadcast(Msg(name="Host",role="user", content=f"Welcome to join the seminar chat! Now, The idea draft we need to discuss as follows:\n{test}"))

        dialogAgent_Qwen()
        dialogAgent_Gemini()
        dialogAgent_DeepSeek()
        userAgent()
        dialogAgent_Viewer()

    # 打印模型 API 的使用情况
    agentscope.print_llm_usage()

if __name__ == "__main__":
    user_prompt="""# Task Definition
You have received a idea draft, which outlines the core problem and rationale of an innovative idea and its preliminary technical details. To further enhance the feasibility, efficiency, or innovation of this idea, you need to refer to the provided "# Next Steps for Optimization", "# Optimization Keywords" and conduct in-depth analysis and optimization by integrating the several related technical articles provided. In addition, you also need to provide a reference.

# Next Steps for Optimization:

1. **Objective 1**: Provide detailed technical specifications for data preprocessing, model architecture, interpretability, scalability, and evaluation metrics.
   - **Plan**: Conduct a thorough review of existing techniques and select the most appropriate methods for each aspect of the research.
2. **Objective 2**: Clarify the unique contributions of the proposed method and its alignment with user needs and field trends.
   - **Plan**: Engage with astronomers and astrophysicists to understand their needs and incorporate their feedback into the research design.
3. **Objective 3**: Conduct a detailed analysis of the scalability and future application prospects of the proposed method.
   - **Plan**: Simulate large-scale data scenarios and explore potential applications in other astronomical surveys.

# Optimization Keywords：

1. **Bayesian Networks**:Search for recent advancements in Bayesian network structure learning and parameter estimation methods, particularly in the context of astronomical data analysis.
2. **Automated Feature Engineering**:Search for recent advancements in automated feature engineering techniques, particularly those that can handle multi-modal data and are scalable to large datasets.
3. **Transformer-based Deep Learning Models**:Search for recent advancements in transformer-based models, particularly those that can handle multi-modal data and are scalable to large datasets.
4. **Time Series Imputation Techniques**:Search for recent advancements in time series imputation techniques, particularly those that use deep learning methods and are validated on astronomical datasets.
5. **Semisupervised Learning**:Search for recent advancements in semisupervised learning techniques, particularly those that use self-tuning pseudolabeling methods and are validated on astronomical datasets.

# The provided the related papers as follows:

# The 1 related paper
## title
Probabilistic Inferences in Bayesian Networks
## abstract
Bayesian network is a complete model for the variables and their relationships, it can be used to answer probabilistic queries about them. A Bayesian network can thus be considered a mechanism for automatically applying Bayes' theorem to complex problems. In the application of Bayesian networks, most of the work is related to probabilistic inferences. Any variable updating in any node of Bayesian networks might result in the evidence propagation across the Bayesian networks. This paper sums up various inference techniques in Bayesian networks and provide guidance for the algorithm calculation in probabilistic inference in Bayesian networks.
## content
### Introduction
Bayesian networks are comprehensive models for variables and their relationships, enabling probabilistic queries. The primary application of Bayesian networks involves probabilistic inference, where any variable update can propagate evidence across the network. This paper summarizes various inference techniques in Bayesian networks, focusing on discrete event characteristics.

### Methods
#### Bayesian Network Semantics
Bayesian networks decompose probability distributions into local distributions, combining them to form the complete joint probability distribution. This factorization reduces the number of required values exponentially compared to a naive table specification. The joint distribution is given by the product:

\[
P(x_{1},...,x_{n}) = \prod_{i} P(x_{i}|\pi(x_{i}))
\]

where \( x_{i} \) denotes a value of variable \( X_{i} \) and \( \pi(x_{i}) \) denotes values of \( X_{i} \)'s parents.

#### Reasoning Structures
Bayesian networks support various reasoning types:
1. **Serial Connections**: Evidence propagates unless a variable is instantiated.
2. **Diverging Connections**: Influence passes between children unless the parent is instantiated.
3. **Converging Connections**: Parents are independent unless evidence on the child is known, leading to the "explaining away" effect.

#### Inference Types
1. **Forward Inference**: Predictive inference from causes to effects.
2. **Backward Inference**: Diagnostic inference from effects to causes.
3. **Intercausal Inference**: Explaining away between parallel variables.
4. **Mixed Inference**: Combinations of the above types.

#### Inference Algorithms
1. **Polytree Algorithm**: Exact, polynomial complexity for singly connected networks.
2. **Loop Cutset Conditioning**: Converts multiple connected networks to singly connected by instantiating a subset of nodes.
3. **Clique-Tree Propagation**: Transforms the network into a clique tree for message propagation.

### Experiments/Results
#### Basic Models
- **Serial Connections**: Forward and backward inferences are straightforward, with evidence blocking or propagating based on instantiation.
- **Diverging Connections**: Forward inference is natural; backward and intercausal inferences require conditional probabilities.
- **Converging Connections**: Forward inference is direct; backward and intercausal inferences involve summing over possible states.

#### Complex Models
Complex networks can be simplified into polytrees using methods like Triangulated Graphs and Clustering. Inference in polytrees involves:
- **Forward Inference**: Nodes send \( \pi \) messages to children.
- **Backward Inference**: Nodes send \( \lambda \) messages to parents.

### Conclusions
Bayesian networks enable efficient probabilistic inference, though exact inference is NP-hard. Techniques like simplifying network structures, pruning unrelated nodes, and using approximate methods are essential for large-scale Bayesian networks.

### Future Work
Future research should focus on developing more efficient algorithms for exact inference in complex networks and exploring approximate methods to handle large-scale Bayesian networks. Additionally, investigating neural plausible models that implement Bayesian network functionality could be beneficial.

# The 2 related paper
## title
Bayesian Neural Networks: Essentials
## abstract
Bayesian neural networks utilize probabilistic layers that capture uncertainty over weights and activations, and are trained using Bayesian inference. Since these probabilistic layers are designed to be drop-in replacement of their deterministic counter parts, Bayesian neural networks provide a direct and natural way to extend conventional deep neural networks to support probabilistic deep learning. However, it is nontrivial to understand, design and train Bayesian neural networks due to their complexities. We discuss the essentials of Bayesian neural networks including duality (deep neural networks, probabilistic models), approximate Bayesian inference, Bayesian priors, Bayesian posteriors, and deep variational learning. We use TensorFlow Probability APIs and code examples for illustration. The main problem with Bayesian neural networks is that the architecture of deep neural networks makes it quite redundant, and costly, to account for uncertainty for a large number of successive layers. Hybrid Bayesian neural networks, which use few probabilistic layers judicially positioned in the networks, provide a practical solution.
## content
### Introduction
Bayesian Neural Networks (BNNs) extend conventional deep neural networks to incorporate probabilistic layers, enabling the capture of uncertainty in weights and activations. This extension is achieved through Bayesian inference, making BNNs a powerful tool for probabilistic deep learning. However, the complexity of BNNs poses challenges in understanding, designing, and training them. This paper discusses the essentials of BNNs, including their duality as both deep neural networks and probabilistic models, approximate Bayesian inference methods, Bayesian priors and posteriors, and deep variational learning. The primary issue with BNNs is the redundancy and computational cost associated with accounting for uncertainty in a large number of successive layers. Hybrid BNNs, which judiciously incorporate few probabilistic layers, offer a practical solution to this problem.

### Methods
#### Duality of Bayesian Neural Networks
BNNs exhibit a dual nature as both deep neural networks and probabilistic models. As deep neural networks, BNNs can be represented by a series of linear transformations followed by nonlinear activation functions. The architecture is defined by input variables (\(\mathbf{X}\)), output variables (y), and hidden variables (h). The network is trained using stochastic gradient descent and backpropagation.

As probabilistic models, BNNs are trained using Bayesian inference, which involves inferring a posterior distribution over the parameters (\(\theta\)) given observed data (D) using Bayes' theorem. The posterior predictive distribution is used for making predictions on new data.

#### Approximate Bayesian Inference
Computing the Bayesian posterior is typically intractable, necessitating the use of approximate Bayesian inference methods. These include Markov Chain Monte Carlo (MCMC) and Variational Inference (VI). MCMC constructs a Markov chain to sample from the posterior, while VI learns a variational distribution (\(q_{\phi}(\theta)\)) to approximate the posterior. The variational distribution is optimized to minimize the KL-divergence from the true posterior.

#### Bayesian Priors
Bayesian priors (\(p(\theta)\)) encode beliefs about the parameters before observing data. For basic BNN architectures, an isotropic Gaussian prior is commonly used due to its mathematical properties. However, the choice of prior can significantly impact the posterior, especially in complex networks.

#### Bayesian Posteriors
Bayesian posteriors (\(p(\theta \mid D)\)) are used for making predictions in BNNs. Since computing the exact posterior is intractable, approximate posteriors obtained through variational inference are used. For BNNs with Gaussian priors, Gaussian approximate posteriors are natural choices.

#### Deep Variational Learning
Deep variational learning adapts variational inference to deep neural networks, which traditionally use stochastic gradient descent and backpropagation. Bayes By Backprop (BBB) is a practical implementation that combines stochastic variational inference with a reparametrization trick to ensure backpropagation works as usual.

### Experiments/Results
The paper presents experiments using TensorFlow Probability to illustrate the implementation of BNNs. Key findings include:
1. **Duality in BNNs**: BNNs can be represented as both deep neural networks and probabilistic models, each with distinct training methodologies.
2. **Approximate Bayesian Inference**: Variational inference is more practical for deep learning due to its scalability compared to MCMC.
3. **Bayesian Priors and Posteriors**: Gaussian priors and approximate posteriors are commonly used, but their impact on network performance varies.
4. **Deep Variational Learning**: BBB effectively combines variational inference with backpropagation, enabling the training of BNNs.
5. **Hybrid BNNs**: Positioning few probabilistic layers at the end of the network significantly reduces computational costs while maintaining performance.

### Conclusions
BNNs provide a natural extension of conventional deep neural networks to support probabilistic deep learning. The duality of BNNs as both deep neural networks and probabilistic models introduces complexity but also offers flexibility. Approximate Bayesian inference methods, particularly variational inference, are essential for making BNNs practical. The judicious use of probabilistic layers in hybrid BNNs offers a scalable solution to the computational challenges posed by BNNs.

### Future Work
Future research should focus on optimizing the placement and number of probabilistic layers in BNNs to further reduce computational costs. Additionally, exploring alternative priors and approximate posteriors could improve the performance and interpretability of BNNs. Investigating the impact of BNNs on out-of-distribution data and developing more robust uncertainty estimation methods are also promising directions.

# The 3 related paper
## title
Learned Feature Importance Scores for Automated Feature Engineering
## abstract
Feature engineering has demonstrated substantial utility for many machine learning workflows, such as in the small data regime or when distribution shifts are severe. Thus automating this capability can relieve much manual effort and improve model performance. Towards this, we propose AutoMAN, or Automated Mask-based Feature Engineering, an automated feature engineering framework that achieves high accuracy, low latency, and can be extended to heterogeneous and time-varying data. AutoMAN is based on effectively exploring the candidate transforms space, without explicitly manifesting transformed features. This is achieved by learning feature importance masks, which can be extended to support other modalities such as time series. AutoMAN learns feature transform importance end-to-end, incorporating a dataset's task target directly into feature engineering, resulting in state-of-the-art performance with significantly lower latency compared to alternatives.
## content
### Introduction

Feature engineering is crucial for enhancing model performance, particularly in scenarios with limited data or severe distribution shifts. Traditional feature engineering is time-consuming and requires domain expertise. Automated feature engineering aims to alleviate these issues by automating the process of crafting powerful features. Various approaches have been explored, including search-based algorithms, meta-learning, and deep learning models. However, challenges remain in achieving robust performance across different data regimes, handling feature explosion, and ensuring scalability and interpretability.

The proposed AutoMAN framework addresses these challenges by leveraging a set of expert-curated transform functions and learning feature importance masks to explore the transform space implicitly. AutoMAN optimizes feature transforms directly for the downstream task, achieving state-of-the-art performance with lower latency compared to alternatives. The framework is scalable, adaptable to time series data, and integrates seamlessly with gradient-based models.

### Methods

#### Overview
AutoMAN starts with a pre-determined set of candidate transform functions and explores the space of all transform-function-feature combinations implicitly by learning feature importance masks. The framework consists of local masks to select features for each transform function and a global mask to select the most relevant transformed features across all transforms.

#### Notations
- \(\mathbf{X} \in \mathbb{R}^{n \times d}\): Input data.
- \(\mathbf{m}_{loc}\), \(\mathbf{m}_{gbl}\): Learned feature importance masks.
- \(\mathbf{F} = \{f_i\}_{i=1}^k\): Set of \(k\) candidate transform functions.
- \(\odot\): Element-wise multiplication.

#### Efficient Search in Feature Transform Space
AutoMAN uses a small set of human-expert-curated transform functions, which include normalization, feature-wise aggregations, and learnable components. This approach improves scalability by limiting the transform space explored. The complexity is linear with respect to the number of features and transform functions.

#### Learning Feature Importance Masks
AutoMAN learns two types of feature importance masks:
1. **Local Masks** (\(\{\mathbf{m}_{loc}^{(f)}\}_{f \in \mathbf{F}}\)): Select features for each transform function.
2. **Global Mask** (\(\mathbf{m}_{gbl}\)): Selects the most relevant feature-transform combinations across all transforms.

The masks are learned using softmax and applied element-wise to the input features. The local masks are sparse, ensuring that only the most relevant features are selected for each transform. The global mask is applied to the concatenated output of all transform functions.

#### Extending Feature Discovery to Time Series
AutoMAN extends to time series data by learning temporal masks along the time dimension. These masks select the most relevant time steps for a given transform, preserving temporal relations within the data.

#### Transform Functions Explored
AutoMAN explores a diverse set of transformations, including polynomial transforms, logarithm, custom z-scaling, additive and multiplicative aggregations, Gaussian, quantile transform, GroupBy, and temporal transformations like standard normalization, differencing, lag, and mean.

#### Complexity Analysis
AutoMAN's complexity is \(O(Nmk)\), where \(N\) is the number of training samples, \(m\) is the number of initial features, and \(k\) is the number of transform functions. This linear scaling ensures efficient handling of large datasets.

### Experiments/Results

#### Experimental Setup
AutoMAN is evaluated on various prediction tasks against competitive baselines (OpenFE, AutoFeat) using MLP and XGBoost predictors. The same pipeline is applied across all methods, and the performance is averaged across multiple trials with different random seeds.

#### Datasets
Experiments are conducted on datasets with varying numbers and types of features, including Isolet, Diabetes, Heart Disease, Fraud, MNIST, Coil, Mice, and M5.

#### Results
AutoMAN consistently outperforms other baselines across different datasets and predictors. The framework demonstrates superior performance, particularly with the MLP predictor, due to its end-to-end learning approach. AutoMAN also shows significant improvements in latency performance, scaling linearly with the number of features and transform functions.

### Conclusions

AutoMAN introduces a novel approach to automated feature engineering by leveraging feature importance masks and a curated set of transform functions. The framework achieves state-of-the-art performance with lower latency, scalability, and adaptability to time series data. The research highlights the importance of continuous exploration in feature space and the potential for further optimization in transform function selection.

### Future Work

Future research could focus on automating the selection of transform functions, extending AutoMAN to other data modalities like images, and exploring the potential of composing transforms within the framework. Additionally, investigating the impact of feature space saturation on larger datasets could provide insights for further improvements.

# The 4 related paper
## title
IIFE: Interaction Information Based Automated Feature Engineering
## abstract
Automated feature engineering (AutoFE) is the process of automatically building and selecting new features that help improve downstream predictive performance. While traditional feature engineering requires significant domain expertise and time-consuming iterative testing, AutoFE strives to make feature engineering easy and accessible to all data science practitioners. We introduce a new AutoFE algorithm, IIFE, based on determining which feature pairs synergize well through an information-theoretic perspective called interaction information. We demonstrate the superior performance of IIFE over existing algorithms. We also show how interaction information can be used to improve existing AutoFE algorithms. Finally, we highlight several critical experimental setup issues in the existing AutoFE literature and their effects on performance.
## content
### Introduction

Feature engineering is a critical technique in machine learning, aimed at creating new features from existing ones to enhance model performance. Traditional feature engineering requires significant domain expertise and iterative testing, which can be time-consuming. Automated feature engineering (AutoFE) seeks to automate this process, making it accessible to general data science practitioners without the need for deep domain knowledge.

This paper introduces a new AutoFE algorithm called Interaction Information Based Automated Feature Engineering (IIFE). IIFE leverages interaction information, an information-theoretic measure, to determine which feature pairs synergize well in predicting the target. By focusing on feature pairs with high interaction information, IIFE aims to create complex engineered features efficiently, reducing computation time.

The main research questions addressed in this paper are:
1. How does IIFE perform compared to existing AutoFE methods?
2. Can interaction information be used to improve existing AutoFE algorithms?
3. What are the critical experimental setup issues in the existing AutoFE literature, and how do they affect performance?

### Methods

#### Algorithm Description

IIFE is an iterative algorithm that uses interaction information to guide feature engineering. Interaction information generalizes mutual information to more than two variables, quantifying the synergy between three variables (two features and the target). The interaction information \(\tau_{ij}\) between features \(F_i\) and \(F_j\) with target \(Y\) is computed as:

\[
\tau_{ij} = I(F_i, F_j, Y) = I(F_i, F_j | Y) - I(F_i, F_j)
\]

where \(I(F_i, F_j)\) is the mutual information between \(F_i\) and \(F_j\), and \(H(F_i)\) is the Shannon entropy of \(F_i\).

The algorithm proceeds as follows:
1. Compute interaction information for all pairs of original features.
2. Explore feature pairs with the highest interaction information.
3. Create combinations of these feature pairs using bivariate functions from a fixed set \(\mathcal{B}\).
4. Evaluate the performance of these combinations using a downstream model \(M\) via cross-validation \(V_M\).
5. Select the best-performing engineered feature and add it to the feature pool.
6. Repeat the process, including the new feature in subsequent iterations.

#### Experimental Setup

The performance of IIFE is compared with state-of-the-art AutoFE algorithms (OpenFE, EAAFE, AutoFeat, and DIFER) on both public and proprietary datasets. The public datasets vary in size and include classification and regression tasks. The proprietary dataset is significantly larger than those used in the AutoFE literature.

For each dataset and model, 25 runs are completed with different random seeds. Hyperparameter tuning is performed both before and after AutoFE. The test score is computed on the raw features as a baseline and again after AutoFE. Metrics used include F1-micro for classification and 1 − (relative absolute error) for regression.

### Experiments/Results

#### Algorithm Comparisons

IIFE outperforms existing AutoFE methods on public datasets, showing superior performance across various metrics. The algorithm demonstrates significant improvements over the baseline, with an average percent improvement of 26.88% over all datasets and downstream models.

#### Experimental Verification of Interaction Information

A synthetic data experiment is conducted to verify that interaction information can determine the synergy of two features in predicting a target. The results show that interaction information effectively captures the synergy between features, even for complex, nonlinear relationships.

#### Issues in AutoFE Literature

Several issues in the AutoFE literature are identified:
1. **Cross-validation scores as performance metric**: Using cross-validation scores on the full dataset can lead to overfitting. A hold-out test set is necessary for a more realistic measure of performance.
2. **Transductive learning in OpenFE**: OpenFE's use of transductive learning can overestimate performance. Adjusting OpenFE to operate in the inductive setting shows more realistic performance.

#### Improving Other Algorithms with Interaction Information

Interaction information can significantly accelerate existing expand-reduce AutoFE algorithms by reducing the search space. The accelerated versions of OpenFE and AutoFeat show comparable or better test scores with significantly shorter runtimes.

### Conclusions

IIFE is an effective AutoFE algorithm that uses interaction information to determine which feature pairs to combine, significantly reducing the search space and allowing complex engineered features to be found efficiently. The algorithm outperforms existing methods on various datasets and downstream models, demonstrating its adaptability and effectiveness. Interaction information can also be used to accelerate other AutoFE algorithms, making them more efficient without compromising performance.

### Future Work

Future research could explore further optimizations of IIFE, such as parallelizing the computation of interaction information and expanding the set of bivariate functions. Additionally, investigating the impact of different feature selection criteria and exploring the combination of IIFE with other AutoFE methods could yield further improvements. Addressing the identified issues in the AutoFE literature and developing best practices for experimental setup would also be beneficial.

# The 5 related paper
## title
MeMOT: Multi-Object Tracking with Memory
## abstract
We propose an online tracking algorithm that performs the object detection and data association under a common framework, capable of linking objects after a long time span. This is realized by preserving a large spatio-temporal memory to store the identity embeddings of the tracked objects, and by adaptively referencing and aggregating useful information from the memory as needed. Our model, called MeMOT, consists of three main modules that are all Transformer-based: 1) Hypothesis Generation that produce object proposals in the current video frame; 2) Memory Encoding that extracts the core information from the memory for each tracked object; and 3) Memory Decoding that solves the object detection and data association tasks simultaneously for multi-object tracking. When evaluated on widely adopted MOT benchmark datasets, MeMOT observes very competitive performance.
## content
### Introduction

Online Multi-Object Tracking (MOT) aims to localize and track multiple objects, such as pedestrians, across a video sequence, ensuring consistent object identities over time. Traditional methods often divide this task into two stages: object detection in individual frames and data association across frames. Recent studies suggest that combining these stages can improve performance but may oversimplify the association module, particularly in modeling object state changes over time.

This paper introduces MeMOT, a Transformer-based tracking model that integrates object detection and data association within a unified framework. MeMOT employs a large spatio-temporal memory to store past observations of tracked objects, enabling accurate state approximation for association tasks. The model consists of three main components: Hypothesis Generation, Memory Encoding, and Memory Decoding, all based on Transformer architectures. MeMOT's design allows it to maintain active tracks, link reappearing objects after occlusion, and generate new object instances without requiring post-processing steps.

### Methods

#### Overview

Given a sequence of video frames \( I = \{I^0, I^1, \ldots, I^T\} \), the goal of online MOT is to localize and track \( K \) objects over time. MeMOT achieves this by jointly learning object detection and association. The model comprises three main components:

1. **Hypothesis Generation Module (\(\Theta_H\))**: Produces region proposals for the current frame \( I^t \).
2. **Memory Encoding Module (\(\Theta_E\))**: Aggregates track embeddings.
3. **Memory Decoding Module (\(\Theta_D\))**: Associates new detections with tracked objects.

#### Hypothesis Generation

The Hypothesis Generation network \(\Theta_H\) uses a Transformer-based encoder-decoder architecture to produce \( N_{pro}^t \) region proposals represented as proposal embeddings \(\bar{\pmb{Q}}_{pro}^i \in \mathbb{R}^{N_{pro}^t \times d}\). The encoder processes a sequentialized feature map \(\boldsymbol{z}_0^t \in \mathbb{R}^{C \times H W}\) extracted from the input frame \( I^t \). The decoder generates the final set of proposal embeddings \(\pmb{Q}_{pro}^t \in \mathbb{R}^{N_{pro}^t \times d}\).

#### Spatio-Temporal Memory

The history states of all \( N \) tracked objects are stored in a spatio-temporal memory buffer \( X \in \mathbb{R}^{N \times T \times d} \), with a maximum of \( N_{max} \) objects and \( T_{max} \) time steps per object. The memory uses a FIFO data structure, updating at each time step \( t \).

#### Memory Encoding

The Memory Encoding module \(\Theta_E\) aggregates track embeddings using three attention modules:

1. **Short-term Block (\(f_{short}\))**: Assembles embeddings of neighboring frames to smooth out noise.
2. **Long-term Block (\(f_{long}\))**: Extracts relevant features from the temporal window covered by the memory.
3. **Fusion Block (\(f_{fusion}\))**: Aggregates embeddings from short- and long-term branches.

The short-term module uses the most recent state \(\mathbf{\bar{X}}^{t-1}\), while the long-term module uses a dynamically updated embedding called Dynamic Memory Aggregation Tokens (DMAT) \( Q_{dmat}^{t-1} \). The outputs are fused to produce the track embedding \(\pmb{Q}_{tck}^t\) and an updated \( \pmb{Q}_{dmat}^t \).

#### Memory Decoding

The Memory Decoder \(\Theta_D\) takes proposal embeddings, track embeddings, and image features as inputs to produce final tracking results. It uses stacked Transformer decoder units with concatenated proposal and track embeddings \( [\pmb{Q}_{pro}^t, \pmb{Q}_{tck}^t] \) as queries and the encoded image feature \( z_1^t \) from \(\Theta_H\) as key and value.

For each query \( q_i^t \) in the outputs \( [\widehat{\pmb{Q}}_{pro}^t, \widehat{\pmb{Q}}_{tck}^t] \), the decoder generates bounding box predictions, objectness scores, and uniqueness scores. The confidence score \( s_k^t \) is defined as the product of objectness and uniqueness scores:

\[ s_k^t = o_k^t \cdot u_k^t \]

During inference, entries with \( s_i^t \geq \epsilon \) are retained, determining whether they represent tracked or new objects.

#### Training MeMOT

MeMOT is supervised with a tracking loss computed on objectness scores, uniqueness scores, and bounding boxes. The loss is a combination of focal loss, L1 loss, and generalized IoU loss. An auxiliary detection loss is also applied to enhance localization capability.

### Experiments/Results

#### Datasets and Metrics

MeMOT is evaluated on the MOT Challenge datasets (MOT16, 17, 20) using standard protocols including CLEAR MOT Metrics and HOTA.

#### Settings

MeMOT is implemented in PyTorch, trained on 8 Tesla A100 GPUs. Input frames are resized to 800 pixels on the shorter side. The model uses ResNet50 and Deformable DETR pretrained on COCO for hypothesis generation. The memory buffer contains up to 300 tracks for MOT16/17 and 600 for MOT20, with a maximum temporal length of 22 for MOT16/17 and 20 for MOT20.

#### Comparison with State-of-the-Art Methods

MeMOT achieves state-of-the-art performance among in-network association solver (IAS) methods on MOT16/17, with competitive detection accuracy and superior data association metrics. On crowded scenarios like MOT20, MeMOT shows significant reductions in ID switches (IDsw) compared to other Transformer-based methods.

#### Visualization

Visualizations of object trajectories demonstrate MeMOT's ability to generate long, consistent predictions even in crowded and occluded scenes. Attention weights from the memory aggregator show that the model effectively captures distinctive object features, especially during occlusions.

#### Ablation Studies

Ablation studies validate the design choices of MeMOT, including the effects of short-term and long-term memory lengths, memory aggregation methods, and the use of learnable tokens versus latest observations. The studies confirm the effectiveness of the proposed memory design and aggregation strategies.

### Conclusions

MeMOT effectively integrates object detection and data association within a unified framework, leveraging a large spatio-temporal memory and attention-based aggregation. Extensive experiments demonstrate its superior performance in object localization and association, particularly in crowded scenes.

### Future Work

Future research could focus on developing annotation-efficient training methods to overcome the limitations of current tracking datasets. Additionally, improving the efficiency of the spatio-temporal memory to handle longer temporal lengths could enhance the model's capabilities further.

# The 6 related paper
## title
A First Look at Deep Learning Apps on Smartphones
## abstract
We are in the dawn of deep learning explosion for smartphones. To bridge the gap between research and practice, we present the first empirical study on 16,500 the most popular Android apps, demystifying how smartphone apps exploit deep learning in the wild. To this end, we build a new static tool that dissects apps and analyzes their deep learning functions. Our study answers threefold questions: what are the early adopter apps of deep learning, what do they use deep learning for, and how do their deep learning models look like. Our study has strong implications for app developers, smartphone vendors, and deep learning R\&D. On one hand, our findings paint a promising picture of deep learning for smartphones, showing the prosperity of mobile deep learning frameworks as well as the prosperity of apps building their cores atop deep learning. On the other hand, our findings urge optimizations on deep learning models deployed on smartphones, the protection of these models, and validation of research ideas on these models.
## content
### Introduction
The research focuses on the adoption of deep learning (DL) in smartphone applications, a critical area given the ubiquity of smartphones and the advancements in DL technologies. The study aims to bridge the gap between DL research and practical application by examining 16,500 popular Android apps. The primary objectives are to identify early adopters of DL, understand the applications of DL in these apps, and analyze the characteristics of the DL models used. This study is significant for app developers, smartphone vendors, and DL researchers, providing insights into the current state and future potential of DL on smartphones.

### Methods
#### Research Design
The study involves a static analysis of Android apps to identify those utilizing DL frameworks. Two datasets of 16,500 popular apps each were collected in June and September 2018. The analysis tool, DL Sniffer, detects the usage of popular DL frameworks by examining APK files and native shared libraries.

#### Data Sources and Sample Selection
The datasets consist of the top 500 free apps from each of the 33 categories listed on Google Play. The analysis focuses on the September 2018 dataset, with comparisons to the June 2018 dataset.

#### Experimental Setup
The DL Sniffer tool decomposes APK files and searches for specific strings in the rodata section of native libraries to identify DL frameworks. For Java-based frameworks, the tool converts APK files to smali code for static analysis. The Model Extractor module further extracts DL models from identified apps for detailed analysis.

### Experiments/Results
#### Characteristics of DL Apps
- **Popularity**: DL apps represent only 1.3% of all apps but contribute significantly to downloads and reviews.
- **Growth**: The number of DL apps increased by 27% over the study period.
- **Core Functionality**: 81% of DL apps use DL for core functionalities, indicating its critical role.

#### Popular Uses of DL
- **Image Processing**: The most common use, particularly in photo beauty and face detection apps.
- **Text and Audio Processing**: Includes word and emoji prediction, auto-correct, and speech recognition.

#### DL Frameworks
- **Adoption**: TensorFlow, TFLite, and ncnn are the most popular frameworks.
- **Trends**: Mobile-optimized frameworks like TFLite and ncnn are gaining traction, reflecting a shift towards on-device DL inference.

#### Model Analysis
- **Structures**: Most models are CNN-based, with convolutional layers being the most common.
- **Optimizations**: Only 6% of models use known optimizations like quantization, indicating a significant untapped potential for efficiency improvements.
- **Resource Footprint**: DL models on smartphones are lightweight, with median memory usage of 2.47 MB and inference computation of 10M FLOPs.
- **Security**: Only 39.2% of models are obfuscated, and 19.2% are encrypted, leaving most models vulnerable to extraction and misuse.

### Conclusions
The study reveals a promising landscape for DL on smartphones, with top apps leading the adoption. DL is increasingly used as a core component in various app functionalities, particularly in image processing. The findings highlight the need for further optimizations and security measures for DL models deployed on smartphones. The study provides valuable insights for app developers, DL framework developers, and hardware designers, urging them to prioritize lightweight models and robust security measures.

### Future Work
Future research should focus on extending the analysis to longer time periods and other platforms like iOS. Dynamic analysis could provide deeper insights into runtime performance. Additionally, enhancing the static analysis tool to detect more DL apps and validate their actual usage is crucial.

# The 7 related paper
## title
Filling out the missing gaps: Time Series Imputation with Semi-Supervised Learning
## abstract
Missing data in time series is a challenging issue affecting time series analysis. Missing data occurs due to problems like data drops or sensor malfunctioning. Imputation methods are used to fill in these values, with quality of imputation having a significant impact on downstream tasks like classification. In this work, we propose a semi-supervised imputation method, ST-Impute, that uses both unlabeled data along with downstream task's labeled data. ST-Impute is based on sparse self-attention and trains on tasks that mimic the imputation process. Our results indicate that the proposed method outperforms the existing supervised and unsupervised time series imputation methods measured on the imputation quality as well as on the downstream tasks ingesting imputed time series.
## content
### Introduction
Time series data is prevalent in various applications, including meteorological forecasting, healthcare monitoring, and financial predictions. Despite advancements in deep learning, missing values in time series data remain a significant issue due to sensor failures, data transmission errors, and malfunctioning sensors. Missing data can adversely affect downstream models for classification and forecasting. Given the scarcity of labeled data, especially in sensitive domains like healthcare, discarding entire time series data is impractical. Therefore, developing models that handle missing time series data effectively is crucial.

The primary utility of imputation methods is to enhance the accuracy of downstream tasks like classification or regression. These tasks are compromised if the imputation method alters the time-series distribution, leading to errors in downstream models. Time series imputation methods can be categorized into unsupervised and supervised approaches. Unsupervised methods learn statistical patterns in observed time series to interpolate missing values, while supervised methods use downstream tasks as the primary teaching signal for imputation. However, labeled data is often limited in practical settings, making semi-supervised methods that leverage both unlabeled and labeled data essential.

This work introduces a novel semi-supervised method, Sparse Transformer based Imputation (ST-Impute), for imputing missing time series values. ST-Impute modifies the transformer architecture using diagonal self-attention masking and sparse activation functions. The model is trained on masked imputation modeling (MIM) to predict artificially removed values, mimicking the imputation task. ST-Impute demonstrates improvements over competitive baselines, enhancing imputation quality and performance in downstream tasks.

### Methods
#### Model Architecture
ST-Impute utilizes the encoder network from the transformer architecture, focusing on time-series reconstruction similar to BERT. The model incorporates three modifications:
1. **Missing Value Mask**: Concatenates the input time series with a mask indicating missing values, which is passed through a linear layer with ReLU activation.
2. **Diagonal Self-Attention Masking**: Prevents the model from trivially reconstructing observed values by masking the diagonal elements in the self-attention mechanism.
3. **Sparse Self-Attention**: Replaces the softmax function with Sparsegen to create a sparse attention distribution, focusing on meaningful connections.

#### Training Objectives
ST-Impute employs three training objectives:
1. **Masked Imputation Modeling (MIM)**: Randomly masks time series observations and trains the model to predict these values based on neighboring observations. The loss function is Mean Absolute Error (MAE) on imputed values.
2. **Non-missing Reconstruction Loss (NRL)**: Ensures accurate reconstruction of non-masked observed time series values, helping the model learn time-series patterns and generalize better.
3. **Semi-supervised Downstream Task Loss**: Incorporates downstream task loss (classification or regression) when labels are available, guiding the imputation learning process in a semi-supervised fashion.

The combined training loss function is:
\[
\mathcal{L} = \mathcal{L}_{\mathrm{MIM}} + \mathcal{L}_{\mathrm{NRL}} + \mathcal{L}_{\mathrm{c}}
\]

### Experiments/Results
#### Datasets
Experiments were conducted on three public datasets:
1. **PhysioNet**: Multivariate clinical time series with high missingness (80.67%) and a downstream task of predicting in-hospital mortality.
2. **Activity**: Multivariate time series of motion state recordings with 4,100 samples over 40 time steps.
3. **KDD Cup**: PM2.5 particulate measurements from monitoring stations in Beijing, with a missingness rate of 13.30% and a downstream regression task.

#### Baselines
Comparisons were made against several baselines, including Mean Imputation, Last Imputation, ImputeTS, BRITS, GRU-D, GP-VAE, and NAOMI.

#### Imputation Quality Metrics
Imputation quality was measured using Root Mean Square Error (RMSE). ST-Impute consistently outperformed all baselines, demonstrating a 6%-10% lower RMSE than BRITS across datasets.

#### Downstream Tasks
1. **Classification**: Evaluated on the PhysioNet dataset, ST-Impute improved AUC-ROC by 1.3% and PR-AUC by 2.7% over BRITS.
2. **Regression**: On the KDD dataset, ST-Impute achieved a 5.1% lower RMSE than BRITS and a 0.9% lower RMSE than the Transformer model.

#### Ablation Studies
1. **Impact of Loss Functions and Masking**: Diagonal self-attention masking and downstream task loss significantly impacted imputation performance.
2. **Amount of Labeled Data**: Imputation performance improved with more labeled data, with ST-Impute outperforming BRITS in both low and high label data regimes.
3. **Missingness Pattern**: ST-Impute performed better with missing completely at random (MCAR) compared to block missingness patterns, especially at higher missingness rates.

### Conclusions
ST-Impute, a novel transformer-based semi-supervised learning method, effectively imputes missing time-series values by leveraging masked imputation modeling and sparse self-attention. The method outperforms existing unsupervised, supervised, and semi-supervised baselines on imputation tasks and downstream classification and regression tasks across multiple datasets.

### Future Work
Future research could explore more sophisticated missingness patterns and extend ST-Impute to other domains. Additionally, investigating the impact of different sparse activation functions and exploring ensemble methods with ST-Impute could further enhance performance.

# The 8 related paper
## title
Comparison of different Methods for Univariate Time Series Imputation in R
## abstract
Missing values in datasets are a well-known problem and there are quite a lot of R packages offering imputation functions. But while imputation in general is well covered within R, it is hard to find functions for imputation of univariate time series. The problem is, most standard imputation techniques can not be applied directly. Most algorithms rely on inter-attribute correlations, while univariate time series imputation needs to employ time dependencies. This paper provides an overview of univariate time series imputation in general and an in-detail insight into the respective implementations within R packages. Furthermore, we experimentally compare the R functions on different time series using four different ratios of missing data. Our results show that either an interpolation with seasonal kalman filter from the zoo package or a linear interpolation on seasonal loess decomposed data from the forecast package were the most effective methods for dealing with missing data in most of the scenarios assessed in this paper.
## content
### Introduction

Time series data is ubiquitous across various domains, including biology, finance, social sciences, energy, and climate observation. However, missing values are a common issue in such datasets, arising from various causes such as measurement errors, transmission failures, or sensor malfunctions. Imputation, the process of replacing missing values with reasonable estimates, is crucial for maintaining the integrity of subsequent data analysis. Traditional imputation methods often rely on inter-attribute correlations, which are not applicable to univariate time series where only temporal dependencies exist. This paper aims to provide an overview of univariate time series imputation methods and compare their effectiveness using R packages. The primary research questions focus on identifying the most effective imputation techniques for different types of time series data and evaluating their performance under varying ratios of missing data.

### Methods

#### Research Design

The research design involves comparing various imputation methods for univariate time series using R packages. The study focuses on four key datasets: `airpass`, `beersales`, `SP`, and `google`, each representing different time series characteristics (e.g., trend, seasonality). The performance of each imputation method is evaluated using Root Mean Square Error (RMSE) and Mean Absolute Percentage Error (MAPE).

#### Data Sources and Sample Selection

The datasets used in the experiments are sourced from the `TSA` package in R. These datasets are chosen for their representativeness and frequent use in time series analysis literature. The datasets include:
- `airpass`: Monthly total international airline passengers.
- `beersales`: Monthly beer sales in millions of barrels.
- `SP`: Quarterly S&P Composite Index.
- `google`: Daily returns of the Google stock.

#### Experimental Setup

The experiments involve artificially introducing missing values into complete time series datasets and then applying various imputation methods to these datasets. The missing values are simulated using an exponential distribution, which is common in real-life applications. The simulation function is designed to mimic the occurrence of missing data in sensor recordings due to transmission failures.

#### Imputation Methods

Several imputation methods are tested, including:
1. **Univariate Algorithms**: Simple methods like mean, mode, median, and random sample imputation.
2. **Univariate Time Series Algorithms**: Advanced methods that leverage time series characteristics, such as Last Observation Carried Forward (LOCF), Next Observation Carried Backward (NOCB), linear interpolation, and seasonal decomposition methods.
3. **Multivariate Algorithms on Lagged Data**: Techniques that convert univariate time series into multivariate datasets by adding lagged variables.

#### Implementation in R

The following R functions are used for the experiments:
- `na.aggregate` (zoo): Replaces NAs with aggregated values (e.g., overall mean).
- `na.locf` (zoo): Replaces NAs with the most recent non-NA value.
- `na.StructTS` (zoo): Uses a seasonal Kalman filter for interpolation.
- `na.interp` (forecast): Uses linear interpolation for non-seasonal series and seasonal decomposition for seasonal series.
- `na.approx` (zoo): Uses linear interpolation.
- `ar.irmi` (custom function): Combines lagged data with the `irmi` function from the `VIM` package.

### Experiments/Results

#### Experimental Procedure

1. **Data Preparation**: Complete time series datasets are selected.
2. **Missing Data Simulation**: Missing values are introduced using the exponential distribution-based simulation function.
3. **Imputation**: Various imputation methods are applied to the datasets with missing values.
4. **Evaluation**: The performance of each method is evaluated using RMSE and MAPE.

#### Key Findings

- **Airpass Dataset**: `na.StructTS` and `na.interp` performed best due to their ability to handle seasonality and trend.
- **Beersales Dataset**: Similar to the `airpass` dataset, `na.interp` and `na.StructTS` showed the best results, with `na.interp` slightly outperforming `na.StructTS`.
- **Google Dataset**: All methods performed poorly due to the lack of trend and seasonality, with `na.StructTS` and `ar.irmi` showing the worst results.
- **SP Dataset**: `na.StructTS` and `na.interp` again performed best, with `na.interp` showing slightly better results.

#### Error Metrics

- **RMSE**: Measures the average squared difference between the imputed and actual values.
- **MAPE**: Measures the average percentage difference between the imputed and actual values, providing a more interpretable measure for datasets with strong trends.

### Conclusions

The study concludes that imputation methods specifically designed for time series data, such as `na.StructTS` and `na.interp`, outperform general imputation methods. These methods effectively handle the temporal dependencies and seasonal patterns inherent in time series data. The research highlights the importance of using domain-specific imputation techniques for univariate time series, emphasizing the limitations of traditional methods that do not account for temporal characteristics.

### Future Work

Future research could explore additional imputation methods, particularly those that leverage machine learning techniques. Additionally, the study could be extended to include more diverse datasets and evaluate the performance of imputation methods under different missing data mechanisms (e.g., Missing at Random, Not Missing at Random). There is also potential for developing a dedicated R package for univariate time series imputation, incorporating the best-performing methods identified in this study.

# The 9 related paper
## title
A Survey on Semi-Supervised Learning Techniques
## abstract
Semisupervised learning is a learning standard which deals with the study of how computers and natural systems such as human beings acquire knowledge in the presence of both labeled and unlabeled data. Semisupervised learning based methods are preferred when compared to the supervised and unsupervised learning because of the improved performance shown by the semisupervised approaches in the presence of large volumes of data. Labels are very hard to attain while unlabeled data are surplus, therefore semisupervised learning is a noble indication to shrink human labor and improve accuracy. There has been a large spectrum of ideas on semisupervised learning. In this paper we bring out some of the key approaches for semisupervised learning.
## content
### Introduction
Machine learning, a subfield of artificial intelligence, involves creating algorithms that enable computers to learn from experience and improve efficiency. Learning can be inductive, where the goal is to build a classifier that generalizes to unseen data, or transductive, where the learner knows the test dataset during training. Supervised learning uses only labeled data for training, while unsupervised learning uses unlabeled data to find patterns. Semi-supervised learning combines both labeled and unlabeled data to create better classifiers, leveraging the abundance of unlabeled data to improve classification performance. Popular semi-supervised learning models include self-training, generative mixture models, graph-based methods, co-training, and multiview learning. The success of these methods depends on underlying assumptions about the data.

### Methods
#### Generative Models
Generative models assume a joint probability distribution \( \mathsf{p}(\mathrm{x},\mathrm{y})=\mathsf{p}(\mathrm{y})\ \mathsf{p}(\mathrm{x}|\mathrm{y}) \), where \( \mathsf{p}(\mathrm{\boldsymbol{x}}|\mathrm{\boldsymbol{y}}) \) is a mixture distribution. With large unlabeled data, the mixture components can be identified, and one labeled example per component can fully determine the distribution. A binary classification problem is illustrated in Fig. 1. A bias correction model combines generative and discriminative training using the maximum entropy principle, evaluated on the Reuters-21578, WebKB, and 20 newsgroups datasets, outperforming Naïve Bayes with EM and multinomial logistic regression with minimum entropy regularizer (MLR/MER).

#### Self-Training
Self-training involves training a classifier with labeled data, then using it to classify unlabeled data. The most confident predictions are added to the training set, and the process repeats. A semi-supervised approach for object detection systems uses a five-step self-training process, demonstrating comparable results to traditional fully labeled training. Two bootstrapping algorithms, Meta-Bootstrapping and Basilisk, identify subjective nouns from non-annotated texts, starting with seed words and syntactic templates.

#### Co-Training
Co-training requires two views of the data, each providing different, complementary information. Each view is conditionally independent and sufficient for classification. Two classifiers are trained separately, and their most confident predictions on unlabeled data are used to iteratively build labeled training data. A co-training style semi-supervised regression algorithm, COREG, uses two regressors and kNN search, outperforming other co-training algorithms.

#### Multiview Learning
Multiview learning uses multiple hypotheses with different inductive biases, requiring them to make similar predictions on unlabeled data. A multi-view HM perceptron and multi-view 1-norm and 2-norm HM SVMs are developed, minimizing errors for labeled samples and updating views to reduce disagreement on unlabeled samples. Random feature splits perform better than token and surface clue splits, as shown in Fig. 2.

#### Graph-Based Models
Graph-based methods define a graph where nodes represent labeled and unlabeled samples, and edges represent similarity. Label smoothness over the graph is assumed. A directed graph framework classifies unlabeled instances using a random walk with a transition probability matrix and a stationary distribution. This method simplifies spectral clustering for undirected graphs.

### Experiments/Results
Generative models, particularly the bias correction model, outperformed traditional methods on text categorization datasets, handling overfitting effectively. Self-training in object detection showed comparable results to fully labeled training, and bootstrapping algorithms identified over 1000 subjective nouns. COREG outperformed other co-training algorithms in regression tasks. Multiview learning algorithms demonstrated better performance with random feature splits. Graph-based methods provided a robust framework for semi-supervised learning on directed graphs.

### Conclusions
Semi-supervised learning leverages the abundance of unlabeled data to improve classification performance, reducing human labor and enhancing accuracy. Generative models, self-training, co-training, multiview learning, and graph-based methods are effective approaches, each with unique advantages and assumptions. The study highlights the potential of semi-supervised learning in various applications, contributing to both theoretical and practical advancements in machine learning.

### Future Work
Future research could explore more complex data structures and additional assumptions to further enhance semi-supervised learning methods. Evaluating these methods on diverse datasets and real-world applications could provide deeper insights. Addressing limitations such as model assumptions and computational complexity will be crucial for broader adoption and practical utility.

# The 10 related paper
## title
Adaptive Semisupervised Inference
## abstract
Semisupervised methods inevitably invoke some assumption that links the marginal distribution of the features to the regression function of the label. Most commonly, the cluster or manifold assumptions are used which imply that the regression function is smooth over high-density clusters or manifolds supporting the data. A generalization of these assumptions is that the regression function is smooth with respect to some density sensitive distance. This motivates the use of a density based metric for semisupervised learning. We analyze this setting and make the following contributions - (a) we propose a semi-supervised learner that uses a density-sensitive kernel and show that it provides better performance than any supervised learner if the density support set has a small condition number and (b) we show that it is possible to adapt to the degree of semi-supervisedness using data-dependent choice of a parameter that controls sensitivity of the distance metric to the density. This ensures that the semisupervised learner never performs worse than a supervised learner even if the assumptions fail to hold.
## content
### Introduction

Semisupervised learning methods rely on assumptions linking the marginal distribution of features to the regression function of labels. Common assumptions include the cluster or manifold assumption, which implies that the regression function is smooth over high-density clusters or manifolds. A generalization of these assumptions is that the regression function is smooth with respect to a density-sensitive distance. This paper proposes a semisupervised learner using a density-sensitive kernel and demonstrates its superior performance over supervised learners under certain conditions. The key contributions include:
1. A semisupervised learner that outperforms supervised learners if the density support set has a small condition number.
2. An adaptive method to choose the sensitivity parameter of the distance metric based on data, ensuring the semisupervised learner never performs worse than a supervised learner.

### Methods

#### Research Design and Data Sources
The research involves a collection of joint distributions \(\mathcal{P}_{XY}(\alpha)\) indexed by \(\alpha\), where \(X\) is supported on a compact domain \(\mathcal{X} \subset \mathbb{R}^d\) and \(Y\) is real-valued. The marginal density \(p(x)\) is bounded, and the conditional density \(p(y|x)\) has a bounded variance. The regression function \(f(x) = \mathbb{E}[Y|X=x]\) is also bounded.

#### Density-Sensitive Distance
A density-sensitive distance \(D_\alpha(x_1, x_2)\) is defined as:
\[ D_\alpha(x_1, x_2) = \inf_{\gamma \in \Gamma(x_1, x_2)} \int_0^{L(\gamma)} \frac{1}{p(\gamma(t))^\alpha} dt \]
where \(\Gamma(x_1, x_2)\) is the set of all continuous finite curves from \(x_1\) to \(x_2\) with unit speed.

#### Assumptions
1. **Semisupervised Smoothness**: The regression function \(f(x)\) is \(\beta\)-smooth with respect to \(D_\alpha\):
\[ |f(x_1) - f(x_2)| \leq C_1 [D_\alpha(x_1, x_2)]^\beta \]
2. **Density Smoothness**: The density function \(p(x)\) is \(\eta\)-smooth with respect to Euclidean distance.

#### Semisupervised Kernel Estimator
The semisupervised kernel estimator \(\widehat{f}_{h,\alpha}(x)\) is defined as:
\[ \widehat{f}_{h,\alpha}(x) = \frac{\sum_{i=1}^n Y_i K_h(\widehat{D}_{\alpha,m}(x, X_i))}{\sum_{i=1}^n K_h(\widehat{D}_{\alpha,m}(x, X_i))} \]
where \(K_h(x) = K(\|x\|/h)\) and \(\widehat{D}_{\alpha,m}(x_1, x_2)\) is a plug-in estimate of \(D_\alpha\).

### Experiments/Results

#### Performance Upper Bound
Theorem 1 provides an upper bound on the performance of the density-sensitive semisupervised kernel estimator:
\[ \sup_{(p,f) \in \mathcal{P}_{XY}(\alpha)} \mathbb{E}_{n,m} \left\{ \int (\widehat{f}_{h,\alpha}(x) - f(x))^2 dP(x) \right\} \leq (M^2 + \sigma^2) \left( \frac{1}{m} + 3c_3 2^d \Lambda_0 \frac{\delta_m}{\tau_0} \right) + \left[ h \left( \frac{\lambda_0 + \epsilon_m}{\lambda_0} \right)^\alpha \right]^{2\beta} + \frac{K(M^2/e + 2\sigma^2)}{n} \]

#### Performance Lower Bound
Theorem 2 establishes a lower bound on the performance of any supervised estimator:
\[ \inf_{\widehat{f}} \sup_{(p,f) \in \mathcal{P}_{XY}(\alpha)} \mathbb{E}_n \int (\widehat{f}(x) - f(x))^2 dP(x) = \Omega(1) \]

### Conclusions

The study demonstrates that a semisupervised kernel estimator using a density-sensitive distance can outperform any supervised learning algorithm in terms of integrated mean squared error rate when the condition number of the support set is small. The adaptive method to choose the sensitivity parameter ensures that the semisupervised learner gracefully degrades to a supervised learner if the semisupervised assumption does not hold.

### Future Work

Future research could explore other density-sensitive metrics, relax assumptions about the density being strictly bounded away from zero, and investigate other types of estimators beyond kernel estimators. Additionally, simulations and empirical studies could further validate the proposed methods and their adaptability to different scenarios.


# The draft of the idea that requires iterative optimization is as follows:
### Problem:
The identification and classification of pulsar candidates in modern astronomical surveys is a challenging task due to the vast volumes of data, the complexity of the features involved, and the presence of missing data. Existing methods, such as Bayesian networks, automated feature engineering, and deep learning models, have shown promise individually, but their integration has not been thoroughly explored. This integration could enhance the overall efficiency and accuracy of pulsar candidate classification, addressing the limitations of current methods, such as the inability to handle missing data effectively and the reliance on large labeled datasets.

### Rationale:
The proposed integrated framework leverages the strengths of Bayesian networks, automated feature engineering, and transformer-based deep learning models. Bayesian networks can model the complex probabilistic relationships between features, while automated feature engineering identifies critical synergistic feature pairs. Transformer-based models, known for their ability to handle sequential and multi-dimensional data, can further improve classification accuracy by leveraging the rich, multi-modal data typical of pulsar candidates. Additionally, time series imputation techniques and semisupervised learning methods are incorporated to handle missing data and leverage unlabeled data effectively. This integrated approach aims to provide a robust and adaptable solution for pulsar candidate classification.

### Necessary technical details:
1. **Bayesian Networks**: To model the probabilistic relationships between different features in pulsar candidate data.
2. **Automated Feature Engineering (AutoFE)**: Specifically, algorithms like IIFE to identify synergistic feature pairs.
3. **Transformer-based Deep Learning Models**: Vision Transformer (ViT) and Convolutional Vision Transformer (CvT) for classification.
4. **Time Series Imputation Techniques**: Deep learning methods to handle missing values in the data.
5. **Semisupervised Learning**: Self-tuning pseudolabeling techniques to leverage unlabeled data effectively.

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
   - **Bayesian Networks**: Construct Bayesian networks to model the probabilistic relationships between different features in the pulsar candidate data.
   - **Automated Feature Engineering**: Apply IIFE algorithms to identify synergistic feature pairs that enhance the input data for deep learning models.
   - **Time Series Imputation**: Use deep learning-based imputation techniques to handle missing values in the time series data.

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
5. "Enhancing Pulsar Candidate Identification with Self-tuning Pseudolabeling Semisupervised Learning"

# Output Requirements
With the provided idea draft, your objective now is to optimize the idea draft based on the related papers, "# Next Steps for Optimization", "# Optimization Keywords" but also strives to be original, clear, feasible, relevant, and significant. Before optimizing the idea draft, revisit the title and abstract of the target paper, to ensure it remains the focal point of your research problem identification process.

# Respond in the following format:
### Problem:
### Rationale:
### Necessary technical details:
### Datasets:
### Paper title:
### Paper abstract:
### Methods:
### Experiments:
### Reference: [Title 1], [Title 2], ..., [Title n]
"""
    moa_table(model_configs=model_configs,topic='')



    # moa_idea_iteration(model_configs=model_configs, topic="Pulsar Candidate Classification", user_prompt=user_prompt)
    # # 来自Alice的简单文本消息示例
    # message_from_alice = Msg("Alice", "Hi!")

    # dict={
    #  'main':'deepseek-chat',
    #  'helper':['deepseek-chat','qwen-max-0919']
    # }
    #
    # moa_model(model_configs=model_configs, agent_list=dict, topic='', user_prompt='hello', systeam_prompt='', aggregation_prompt="")

