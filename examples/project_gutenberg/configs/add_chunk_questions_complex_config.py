# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
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
Your task involves the analysis of a text and the creation of complex questions. 
The text for analysis is a paragraph among many from a chapter of a book. 
In addition to the text under analysis, you have access to preceding paragraphs (if they exist)
of the chapter to clarify the context of the paragraph being analyzed. 

Your task is:

Generate {num_questions} unique, meaningful, well-formulated, and, if possible, compound questions that are answered in the text.
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

About the text
--------------

The text for analysis comes from the work {book_title}, specifically chapter {chapter}. The author(s) is/are {authors}. 
The text should be understood in the context of previous paragraphs, 
which are listed here as summaries in chronological order:

```text
{context_chunks}
```

Here is the text for question generation:

```text
{chunk_text}
```

MAKE SURE THAT YOU USE JSON TO WRITE THE ASSESSED LIST OF QUESTIONS AT THE END!
"""

# Load the API keys
load_dotenv()

config = QuestionChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = QUESTION_TEMPLATE
config.num_context_chunks = 5
config.number_of_questions_div = 40
config.sleep_time_between_api_calls = 1
config.name = "complex_questions"
config.context = "Create a list of complex questions for the provided paragraphs"

# config.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
# config.url = os.getenv('TOGETHER_AI_API_URL')
# config.api_key = os.getenv('TOGETHER_AI_API_KEY')
# config.max_tokens = 10000

config.model = "gpt-3.5-turbo-0125"
config.url = os.getenv('OPENAI_API_URL')
config.api_key = os.getenv('OPENAI_API_KEY')
config.max_tokens = 4096

config.frequency_penalty = 0
config.temperature = 0.3
config.top_p = 1.0
config.presence_penalty = 0.0
