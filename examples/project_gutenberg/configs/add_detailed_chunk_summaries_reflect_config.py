# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
import os
from dotenv import load_dotenv
from ttk.models.config_models import SummaryChunkConfigModel

SYSTEM_PROMPT = u"""
You are an expert in text analysis, crafting excellent, expressive, and thoughtful summaries, 
and formulating meaningful, well-articulated, and coherent assessments. You proceed methodically, 
contemplating whether each significant theme has been captured in the summary. 
You will assess your summary and reflect over it. 
When possible, mention the author of the text. Ensure that you always adhere to the user's instructions.
Write the final summary and assessment using the user provided JSON format. 
"""

SUMMARIZE_TEMPLATE = u"""
Your task involves the analysis of a text and the creation of a detailed summary using JSON as the output format. 
The text for analysis is a paragraph among many from a chapter of a book. 
In addition to the text under analysis, you have access to preceding paragraphs (if they exist)
of the chapter to clarify the context of the paragraph being analyzed. 


Perform the following steps:
1. Write the summary
2. Write your assessment of the summary
3. Use the JSON format to write the final summary based on the assessment and then add the re-assessment of the final summary

Detailed explanation
--------------------

1. Write summary: 
    Write a detailed and comprehensive summary of the provided paragraph, that contains all relevant topics and is written in excellent english. 
    Reflect over it, if it contains all important topics and is detailed enough to represent the gist of the paragraph.

2. Assess the summary
    Then assess your created summary if it fits the provided criteria and write an assessment after the summary.

3. Use the JSON format to write final summary and assessment
    Then use the provided JSON format below to write your re-assessed summary (in "response" field) and your final assessment (in the "assessment" field) of this summary.
    Ensure that a correct JSON format is created and that it includes the final summary and the final assessment.

Use the following JSON definition as output format for the final summary and assessment:

```json
{{
    "response": "final summary", 
    "assessment": "final assessment"
}}
```

This is the JSON example, of the summary and the assessment stored as JSON format:

```json
{{
"response": "The paragraph discusses the ancient form of sexual propagation through hermaphrodites, prevalent in plants and some animals like garden snails, leeches, and earthworms. Hermaphrodites produce both eggs and sperm within themselves, enabling self-fertilization in some cases, while in others, reciprocal fertilization between hermaphrodites is required for egg development, marking a transition to sexual separation.",
"assessment": "The summary captures the main points of the paragraph, focusing on the ancient form of sexual propagation through hermaphrodites in plants and certain animals. It highlights the production of both eggs and sperm within hermaphrodites and the necessity of reciprocal fertilization in some cases, indicating a shift towards sexual separation. The summary is detailed and provides a clear understanding of the text.",
}}            
```

About the text
--------------

The text for analysis comes from the work {book_title}, specifically chapter {chapter}. The author(s) is/are {authors}. 
The text should be understood in the context of previous paragraphs, 
which are listed here as summaries in chronological order:

```text
{context_chunks}
```

Here is the text for analysis:

```text
{chunk_text}
```

"""

# Load the API keys
load_dotenv()

config = SummaryChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = SUMMARIZE_TEMPLATE
config.num_context_chunks = 10
config.num_summaries = 3
config.sleep_time_between_api_calls = 1
config.name = "detailed_summaries"
config.context = "Create detailed summaries with reflection for the provided paragraphs"

# config.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
# config.url = os.getenv('TOGETHER_AI_API_URL')
# config.api_key = os.getenv('TOGETHER_AI_API_KEY')
# config.max_tokens = 16768

config.model = "gpt-3.5-turbo-0125"
config.url = os.getenv('OPENAI_API_URL')
config.api_key = os.getenv('OPENAI_API_KEY')
config.max_tokens = 4096

config.frequency_penalty = 0
config.temperature = 0.3
config.top_p = 1.0
config.presence_penalty = 0.0
