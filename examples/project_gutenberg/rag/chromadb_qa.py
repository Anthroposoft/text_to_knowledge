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
    #metadata = [{"answer": d["answer"], "book": d["book_title"], "chapter": d["chapter"], "typ": d["typ"],
    #             "category": ",".join(d["categories"]), "authors": ";".join(d["authors"])} for d in data]
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
