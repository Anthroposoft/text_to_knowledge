# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
import os
from dotenv import load_dotenv
from ttk.models.config_models import QuestionChunkConfigModel, QuestionAnsweringChunkConfigModel

SYSTEM_PROMPT = u"""
You are an expert in text analysis and adept at answering questions about texts. 
You always proceed step by step, contemplating whether every aspect of the user's question 
has been addressed by you based on the provided text. Answer the question solely based on the 
text given to you, without using any personal knowledge. In your response, you use quotations 
from the given text to support your answer.
"""

ANSWER_TEMPLATE = u"""
Your job is to answer a question about a provided chapter from a larger text. 
The chapter taht must be used for answering is from the book '{book_title}', Chapter '{chapter}' author(s) '{authors}'.

Here is the chapter for which the question should be answered:

```text
{chapter_text}
```

Answer the following question based on the paragraphs above:

'''text
{question}
'''

"""

# Load the API keys
load_dotenv()

config = QuestionAnsweringChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = ANSWER_TEMPLATE
config.sleep_time_between_api_calls = 1
config.name = "complex_questions"
config.number_of_answers = 1

config.model = "gpt-4-turbo-preview"
config.url = os.getenv('OPENAI_API_URL')
config.api_key = os.getenv('OPENAI_API_KEY')
config.max_tokens = 4096

config.frequency_penalty = 0
config.temperature = 0.3
config.top_p = 1.0
config.presence_penalty = 0.0