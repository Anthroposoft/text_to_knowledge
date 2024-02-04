# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
import os
from dotenv import load_dotenv
from ttk.models.config_models import SummaryChunkConfigModel

SYSTEM_PROMPT_SUMMARIZE_QUESTION_EN = u"""
You are an expert in text analysis, crafting excellent, expressive, and thoughtful summaries, 
and formulating meaningful, well-articulated, and coherent questions. Moreover, you excel at categorizing texts, 
capturing keywords, and identifying the most pertinent themes within a text. You proceed methodically, 
contemplating whether each significant theme has been captured in the summary and questions. 
"""

SUMMARIZE_QUESTION_TEMPLATE_EN = u"""
Your task involves the analysis of a text, the creation of summaries, the generation of questions answered 
within the text, and the production of JSON as the output format. The text for analysis is a paragraph among 
many from a chapter of a book. In addition to the text under analysis, you have access to detailed summaries 
of the {max_context_summaries} preceding paragraphs of the chapter to clarify the context of the paragraph being analyzed. 
"""

# Load the API keys
load_dotenv()

config = SummaryChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT_SUMMARIZE_QUESTION_EN
config.user_prompt = SUMMARIZE_QUESTION_TEMPLATE_EN
config.num_context_chunks = 10
config.num_summaries = 3
config.sleep_time_between_api_calls = 1
config.name = "short"
config.context = "Short summaries"
config.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
config.url = "https://api.together.xyz/v1"
config.api_key = os.getenv('TOGETHER_AI_API_KEY')
config.max_tokens = 16768
config.frequency_penalty = 0
config.temperature = 0.3
config.top_p = 1.0
config.presence_penalty = 0.0
