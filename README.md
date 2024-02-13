# text_to_knowledge
This set of tools augments books with summaries, question-answer pairs, keywords and topics using LLM's.

This is a very early development version and should only be used very carefully.

## Approach

- Generate augmented JSON from Books
- Augment the JSON with 
  - summaries
  - questions/answer pairs
  - categories
  - topics, events, keywords, places, dates
- Generate training or RAG ready data 


## The example data was generated with these commands

```bash
# 1. Transform all ebooks into JSON format, so we can add summaries, question, answers and categories
books_to_json --input_list=./ebook_texts/00_file_list.txt --input_dir=./ebook_texts --output_dir=./json

# 2. Add two different summaries, a simpler and a reflective one to chunks, but only a single form to chapters
augment_books add_chunk_summaries --input_dir=json/ --config=configs/add_chunk_summaries_detailed_config.py
augment_books add_chunk_summaries --input_dir=json/ --config=configs/add_chunk_summaries_detailed_reflected_config.py
augment_books add_chapter_summaries --input_dir=json/ --config=configs/add_chapter_summaries_detailed_config.py

# 3. Create questions
augment_books add_chunk_questions --input_dir=json/ --config=configs/add_chunk_questions_complex_config.py
augment_books add_chapter_questions --input_dir=json/ --config=configs/add_chapter_questions_complex_config.py

# 4. Add answers for the questions from step 3
augment_books add_chunk_answers --input_dir=json/ --config=configs/add_chunk_questions_answers_complex_config.py
augment_books add_chapter_answers --input_dir=json/ --config=configs/add_chapter_questions_answers_complex_config.py

# 5. Create categories
augment_books add_categories --input_dir=json/ --config=configs/add_categories_config.py

# 6. Extract Question and answer pairs with metadata
extract_knowledge --typ QA --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant.txt
extract_knowledge --typ QA --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant.json --indent=4
extract_knowledge --typ QA --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver.txt
extract_knowledge --typ QA --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver.json --indent=4
extract_knowledge --typ QA --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.txt
extract_knowledge --typ QA --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --indent=4
extract_knowledge --typ QA --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training.txt
extract_knowledge --typ QA --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training.json --indent=4

# 7. Extract the summaries with metadata
extract_knowledge --typ SUM --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant_sum.txt
extract_knowledge --typ SUM --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant_sum.json --indent=4
extract_knowledge --typ SUM --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver_sum.txt
extract_knowledge --typ SUM --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver_sum.json --indent=4
extract_knowledge --typ SUM --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner_sum.txt
extract_knowledge --typ SUM --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner_sum.json --indent=4
extract_knowledge --typ SUM --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training_sum.txt
extract_knowledge --typ SUM --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training_sum.json --indent=4
```

## The generated JSON data can directly be used in a Vector Database like chromaDB

```python
from pprint import pprint

import chromadb
import json

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="my_collection")


def question(text):
    results = collection.query(
        query_texts=[text],
        n_results=3
    )
    return results


def load_qa_data(file_path: str):
    items = collection.peek(2)
    print(items)
    if len(items["ids"]) > 1:
        print("Database was created")
        return

    with open(file_path, "r") as input:
        data = json.load(input)
    questions = [d["question"] for d in data]
    print("Indexing data")
    count = 0
    for i, q in enumerate(questions):
        metadata = {"answer": data[i]["answer"], "book": data[i]["book_title"],
                    "chapter": data[i]["chapter"], "typ": data[i]["typ"],
                    "category": ",".join(data[i]["categories"]),
                    "authors": ";".join(data[i]["authors"])}
        all_questions = data[i]["permutations"]
        all_questions.append(q)
        print(i, q)
        for question in all_questions:
            collection.add(
                documents=question,
                metadatas=metadata,
                ids=str(count)
            )
            count += 1


load_qa_data(file_path="../training_data/Martin_Luther_from_Carl_Koppenhaver.json")

answer = question("What did Martin Luther achieved?")
pprint(answer)

answer = question("What were Martin Luther greatest fears?")
pprint(answer)

answer = question("What were the significant events in Luther's life between 1501 and 1511?")
pprint(answer)

answer = question("What was the outcome of Luther's debate with Eck at Leipzig in 1519?")
pprint(answer)

answer = question("What important publication did Luther make in 1534?")
pprint(answer)

answer = question("When was Luther born?")
pprint(answer)

answer = question("Where was Luther born?")
pprint(answer)

answer = question("Who where Luther parents?")
pprint(answer)

answer = question("Did Luther had a good relationship with his father?")
pprint(answer)
```
