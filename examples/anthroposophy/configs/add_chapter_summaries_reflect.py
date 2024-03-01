# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
import os
from dotenv import load_dotenv
from ttk.models.config_models import SummaryChunkConfigModel

SYSTEM_PROMPT = u"""
Als der weltbeste Textzusammenfasser ist es deine Aufgabe, komplexe Texte effizient und präzise zu analysieren. 
Deine Fähigkeit, alle relevanten Themen zu erkennen und zu verstehen, ist unübertroffen. 
Bitte lies den Text des Benutzers sorgfältig durch und erstelle eine Zusammenfassung, 
die alle wichtigen Events und Themen beinhaltet. Deine Zusammenfassung sollte im Bullet-Point-Format erfolgen, 
um Klarheit und Übersichtlichkeit zu gewährleisten. 
Präsentiere die Ergebnisse wie folgt:

Hauptthema: [Hauptthema des Textes]

Wichtige Punkte:

- [Wichtiger Punkt 1]
- [Wichtiger Punkt 2]
- [Wichtiger Punkt 3]
...

Schlüsselerkenntnisse:

- [Schlüsselerkenntnis 1]
- [Schlüsselerkenntnis 2]
...


Nachdem du diese erste Zusammenfassung erstellt hast, möchte ich, dass du über die von dir präsentierten 
Informationen reflektierst. Überlege, wie du die Zusammenfassung weiter verbessern kannst. Erstelle eine zweite, 
verbesserte Version der Zusammenfassung, die folgende Kriterien erfüllt:

- Halte die Informationen prägnant und auf den Punkt gebracht.
- Verwende das unten vorgestellte YAML Format. 
- Schreibe die Zusammenfassung in das "response" Feld.
- Schreibe deine Überlegungen und Reflexionen zur finalen Zusammenfassung in dass "assessment" Feld.

```yaml
response: |
  Die finale Zusammenfassung im gleichen Format wie die erste Zusammenfassung
  
assessment: |
  Deine Einschätzung zur finalen Zusammenfassung
```

"""

SUMMARIZE_TEMPLATE = u"""
Der zu zusammenfassende Text ist das Kapitel '{chapter}' des Buches '{book_title}'. 
Der/die Autor(en) ist/sind {authors}.


Stelle sicher das folgende Events Zusammenfassung behandelt werden
------------------------------------------------------------------

{events}


Fasse folgenden Text zusammen unter berücksichtigung der Events
---------------------------------------------------------------


{chapter_text}
"""

# Load the API keys
load_dotenv()

config = SummaryChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = SUMMARIZE_TEMPLATE
config.num_context_chunks = 5
config.num_summaries = 1
config.sleep_time_between_api_calls = 1
config.name = "summaries_reflected_1"
config.context = "Erzeuge Kapitel Zusammenfassungen als Bullet-Points für Text-Absätze"

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
