# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
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
Your task involves the creation of a summary. 
The text to summarize is a paragraph among many from a chapter of a book. 
In addition to the text to summarize, you have access to preceding paragraphs (if they exist)
of the chapter to clarify the context of the paragraph to summarize. 

Write a detailed and comprehensive summary of the provided paragraph, 
that contains all relevant topics, is detailed enough to represent the gist 
of the paragraph and is written in excellent english. 

About the text
--------------

The text for analysis comes from the work {book_title}, specifically chapter {chapter}. The author(s) is/are {authors}. 
The text should be understood in the context of previous paragraphs, 
which are listed here as summaries in chronological order:

```text
{context_chunks}
```

Summarize this text:

```text
{chunk_text}
```

"""

# Load the API keys
load_dotenv()

config = SummaryChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = SUMMARIZE_TEMPLATE
config.num_context_chunks = 5
config.num_summaries = 1
config.sleep_time_between_api_calls = 1
config.name = "summaries"
config.context = "Create summaries for the provided paragraphs"

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
