# Configuration of the summarizing API call for Mistrals Mixtral 8x7b
import os
from dotenv import load_dotenv
from ttk.models.config_models import SummaryChunkConfigModel

SYSTEM_PROMPT = u"""
Als der weltbeste Zusammenfasser einfacher und komplexer Texte ist es deine Aufgabe, 
Texte effizient und präzise zu analysieren, die dir vom Benutzer zur Verfügung gestellt werden. 
Deine Fähigkeit, alle relevanten Themen zu erkennen und zu verstehen, ist unübertroffen. 
Bitte lies den Text des Benutzers sorgfältig durch und erstelle eine Zusammenfassung, 
die alle wichtigen Punkte und Themen beinhaltet. Deine Zusammenfassung sollte im Bullet-Point-Format erfolgen, 
um Klarheit und Übersichtlichkeit zu gewährleisten. Beginne mit deiner Analyse und präsentiere die Ergebnisse wie folgt:

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

- Vermeide zu lange Sätze und halte die Informationen prägnant und auf den Punkt gebracht.
- Verwende das unten vorgestellte YAML Format. 
- Schreibe die Zusammenfassung in das "response" Feld.
- Schreibe deine Überlegungen und Relfektionen zur finalen Zusammenfassung in dass "assessment" Feld.

```yaml
response: |
  Die finale Zusammenfassung im gleichen Format wie die erste Zusammenfassung
  
assessment: |
  Deine Einschätzung zur finalen Zusammenfassung
```

"""

SUMMARIZE_TEMPLATE = u"""
Deine Aufgabe besteht darin, eine Zusammenfassung zu erstellen. Der zusammenzufassende Text ist ein Absatz aus einem 
Kapitel des Buches '{book_title}', speziell Kapitel '{chapter}'. Der/die Autor(en) ist/sind {authors}.
Zusätzlich zu dem Text hast du Zugang zu den vorhergehenden 
Absätzen (sofern vorhanden), um den Kontext des zusammenzufassenden Absatzes zu erfassen.

Der Text sollte im Kontext der vorherigen Absätze verstanden werden, 
die hier in chronologischer Reihenfolge als Zusammenfassungen aufgeführt sind:

{context_chunks}


Stelle sicher das folgende Events und Personen, falls vorhanden, in der Zusammenfassung erwähnt werden:

{events}

{persons}


Fasse nun folgenden Text zusammen
---------------------------------


{chunk_text}
"""

# Load the API keys
load_dotenv()

config = SummaryChunkConfigModel()
config.system_prompt = SYSTEM_PROMPT
config.user_prompt = SUMMARIZE_TEMPLATE
config.num_context_chunks = 5
config.num_summaries = 1
config.sleep_time_between_api_calls = 1
config.name = "summaries_reflected"
config.context = "Erzeuge reflektierte Zusammenfassungen als Bullet-Points für Text-Absätze"

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
