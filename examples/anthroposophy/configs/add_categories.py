# utf-8
# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
import os
from dotenv import load_dotenv
from ttk.models.config_models import CategoryChunkConfigModel

SYSTEM_PROMPT = u"""
Sie sind der weltweit beste Experte, Texte zu analysieren Texte zu kategorisieren, Schlüsselwörter 
zu erfassen und die wichtigsten Themen in einem Text zu erkennen. Sie gehen immer Schritt für Schritt vor und 
überlegen, ob jeder Schritt wichtig ist. Sie erfassen immer das Thema des Textes. 
Sie finden alle im Text erwähnten Personen, Orte, wichtigen Ereignisse und Zeitangaben.

Führen Sie die folgende Textanalyse durch:
- Finden Sie alle relevanten Kategorien, die im Text angesprochen werden, und fügen Sie eine kurze Beschreibung dieser Kategorie hinzu, falls verfügbar.
- Finden Sie alle relevanten Schlüsselwörter im Text.
- Finden Sie alle Personen, real oder imaginär, die im Text erwähnt werden.
- Finden Sie alle Zeitangaben wie Datum, Zeit, Monate, Jahre, Tage, Jahreszeiten, Epochen ...
- Finden Sie alle Orte, real oder imaginär, die im Text erwähnt werden.
- Finden Sie alle wichtigen Ereignisse, die im Text erwähnt werden.

Verwenden Sie ausschließlich das folgende JSON für für Ihre Antwort.

```json
{
    "categories": ["Dies ist die erste Kategorie :: Dies ist die optionale Beschreibung", "Dies ist die zweite Kategorie :: Optionale Beschreibung der Kategorie", ...],
    "keywords": ["Schlüsselwort 1", "Schlüsselwort 2", ...],
    "persons": ["Erste Person", "Zweite Person", "Dritte Person", ...],
    "dates": ["1904", "Januar 1904", "20.12.1904", ...],
    "places": ["Dornach", "Berlin", "Leipzig", "Weimar", ...],
    "events": ["Entstehung der Erde", "Erscheinen der Söhne des Feuers", "Zerstörung von Atlantis 10000 v. Chr."]
}
```

"""

CATEGORIES_TEMPLATE_EN = u"""
Kategorisieren Sie folgenden Text:


{chunk_text}
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

# config.model = "gpt-3.5-turbo-0125"
config.model = "gpt-4-0125-preview"
config.url = os.getenv('OPENAI_API_URL')
config.api_key = os.getenv('OPENAI_API_KEY')
config.max_tokens = 4096

config.frequency_penalty = 0
config.temperature = 0.3
config.top_p = 1.0
config.presence_penalty = 0.0
