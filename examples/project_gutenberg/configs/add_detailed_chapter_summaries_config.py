# Configuration of the summarizing API call for OpenAI ChatGPT4
import os
from dotenv import load_dotenv
from ttk.models.config_models import SummaryChunkConfigModel

SYSTEM_PROMPT = u"""
You are an expert in text analysis, crafting excellent, expressive, and thoughtful summaries, 
and formulating meaningful, well-articulated, and coherent summaries. You proceed methodically, 
contemplating whether each significant theme has been captured in the summary. 
When possible, mention the author of the text.
"""

SUMMARIZE_TEMPLATE = u"""
Your task involves the creation of a detailed and sophisticated summary. 
The text to summarize is a complete chapter '{chapter}' of the book '{book_title}' from author(s) {authors}. 
Write a detailed and comprehensive summary of the provided chapter, 
that contains all relevant topics, is detailed enough to represent the gist 
of the chapter and is written in excellent english. 

Summarize this text:

```text
{chapter_text}
```
"""

# Load the API keys
load_dotenv()

config = SummaryChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = SUMMARIZE_TEMPLATE
config.num_summaries = 1
config.sleep_time_between_api_calls = 1
config.name = "summaries"
config.context = "Create summaries for the provided chapter"

config.model = "gpt-4-turbo-preview"
config.url = os.getenv('OPENAI_API_URL')
config.api_key = os.getenv('OPENAI_API_KEY')
config.max_tokens = 4096

config.frequency_penalty = 0
config.temperature = 0.3
config.top_p = 1.0
config.presence_penalty = 0.0
