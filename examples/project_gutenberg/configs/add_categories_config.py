# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
import os
from dotenv import load_dotenv
from ttk.models.config_models import CategoryChunkConfigModel

SYSTEM_PROMPT = u"""
You are an expert at analyzing texts and an expert at categorizing texts,
capture keywords and recognize the most important topics in a text.
You always go step by step and think about whether each is important
You have grasped the topic and recognized keywords and categories. 
You find all peoples, places, major events and dates mentioned in the text.
Make sure you always follow the user's instructions. You always write your answers in JSON format,
that the user specifies.
"""

CATEGORIES_TEMPLATE_EN = u"""
Perform the following text analysis:
- Find all relevant categories that are addressed in the text, add a short description of this category if available
- Find all relevant keywords in the text
- Find all persons, real or imaginary, that are mentioned in the text
- Find all dates like date, datetime, months, years, days, seasons
- Find all places, real or imaginary that are mentioned in the text
- Find all major events that are mentioned in the text

Put all this data in the following JSON format in your answer:

```json
{{
    "categories": ["This is the first category :: This is the optional description", "This is the seconds category :: Optional description of the category", ...],
    "keywords": ["keyword 1", "keyword 2", ...],
    "persons": ["First Person", "Second Person", "Third Person", ...],
    "dates": ["1904", "Januar 1904", "20.12.1904", ...],
    "places": ["Dornach", "Berlin", "Leipzig", "Weimar", ...],
    "events" : ["Entstehung der Erde", "Erscheinen der Söhne des Feuers", "Zerstörung Atlantis 10000bc"]
}}
```
Here is the text for analysis:

```text
{chunk_text}
```

"""

# Load the API keys
load_dotenv()

config = CategoryChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = CATEGORIES_TEMPLATE_EN
config.sleep_time_between_api_calls = 1

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
