from pprint import pprint

import chromadb
import json

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="my_collection")


def question(text):
    results = collection.query(
        query_texts=[text],
        n_results=1
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
    metadata = [{"answer": d["answer"], "book": d["book_title"], "chapter": d["chapter"], "typ": d["typ"],
                 "category": ",".join(d["categories"]), "authors": ";".join(d["authors"])} for d in data]
    print("Indexing data")

    for i, q in enumerate(questions):
        print(i, q)
        collection.add(
            documents=q,
            metadatas=metadata[i],
            ids=str(i)
        )


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