# Configuration of the summarizing API call for OpenAI ChatGPT4
import os
from dotenv import load_dotenv
from ttk.models.config_models import QuestionChunkConfigModel

SYSTEM_PROMPT = u"""
You are an expert in text analysis, crafting excellent, expressive, and thoughtful questions from existing texts, 
and formulating meaningful, well-articulated, and coherent assessments. You proceed methodically, 
contemplating whether each significant theme has been captured in the questions you generate from a given text. 
You will assess your generated questions and reflect over it. 
Ensure that you always adhere to the user's instructions.
"""

QUESTION_TEMPLATE = u"""
Your task involves the analysis of a text and the creation of a complex questions. 
The text for analysis is a chapter among several from a chapters of a book. 

Your task is:

Generate unique, meaningful, well-formulated, and, if possible, compound questions that are answered in the text.
Make sure that all aspects of the chapter is captures by the questions.
Additionally add cross paragraph questions, when these questions add to the understanding of the chapter.
The text for question generation comes from the work {book_title}, specifically chapter {chapter}. The author(s) is/are {authors}.
Write each question in excellent english. Use the JSON format defined below as output format.
Reflect over it, if the list of questions contains all important topics and are detailed enough to questions the gist of the paragraph.

Then assess your created list of questions if it fits the provided criteria and write an assessment 
(in the "assessment" field) after the list of questions. Use the JSON format defined below as output format.

Use the following JSON definition as output format for the list of questions and assessment:

```json
{{
    "text_list": ["questions one", "questions two", "question three", ...], 
    "assessment": "final assessment"
}}
```

This examples shows the question and assessment as JSON format, that you MUST generate:

```json
{{
    "text_list": [
        "What is the evidence that supports the existence of a lost continent as the origin of wheat cultivation?",
        "How does Darwin explain the origin of modern wheat varieties based on archaeological findings?",
        "What is the significance of the Basque language's uniqueness among European tongues?",
        "How does the Basque language's structure compare to the aboriginal languages of America?",
        "What is the evidence that supports the theory of the Basque language's connection to the aboriginal languages of America?",
        "How does the existence of the Basque language support the theory of a lost continent?",
        "What is the relationship between the lost continent and the colonization of Europe and America?",
        "How did the intelligent selection of extinct wheat species lead to the cultivation of modern varieties?",
        "What is the significance of the absence of wild wheat species in modern times?",
        "How does the evidence of wheat cultivation support the theory of a lost continent?",
        "How does the Basque language's uniqueness among European tongues contribute to the theory of a lost continent?"
    ],
    "assessment": "The generated questions cover the main points of the text, including the evidence for the existence of a lost continent, the origin of wheat cultivation, and the uniqueness of the Basque language. However, the questions could be more specific and focused on the relationship between the lost continent and the colonization of Europe and America."
}}
```

Here is the text for question generation:

```text
{chapter_text}
```

"""

# Load the API keys
load_dotenv()

config = QuestionChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = QUESTION_TEMPLATE
config.sleep_time_between_api_calls = 1
config.name = "complex_questions"
config.context = "Create a list of complex questions for the provided paragraphs"

config.model = "gpt-4-turbo-preview"
config.url = os.getenv('OPENAI_API_URL')
config.api_key = os.getenv('OPENAI_API_KEY')
config.max_tokens = 4096

config.frequency_penalty = 0
config.temperature = 0.3
config.top_p = 1.0
config.presence_penalty = 0.0
