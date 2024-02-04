# This directory contains generated training data from text books

## Data generation

The data in this directory was generated using the *extract_qa_pairs* tool from the text_to_knowledge
framework. The input data are JSON files that were created with the augmentation tools of this framework.

Here are the command line calls to create the question-answer pairs with metadata

```shell   
extract_qa_pairs --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant.txt
extract_qa_pairs --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant.json --indent=4
extract_qa_pairs --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver.txt
extract_qa_pairs --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver.json --indent=4
extract_qa_pairs --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.txt
extract_qa_pairs --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --indent=4
extract_qa_pairs --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training.txt
extract_qa_pairs --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training.json --indent=4
```

The created data is a text file with a list of dictionaries that have the following form:

```json 
[
    {
        "question": "How does the concept of Lemuria challenge traditional ideas of human evolution?",
        "answer": "The concept of Lemuria challenges traditional ideas of human evolution by suggesting that mankind did not develop from Anthropoid apes as commonly believed. The text states, \"[Haeckel] is correct enough in his surmise that Lemuria was the cradle of the human race as it now exists, but it was not out of Anthropoid apes that mankind developed.\" This challenges the traditional evolutionary theory that humans evolved from apes. Instead, the text hints at a different origin for humanity, with Lemuria playing a significant role in the development of the human race.",
        "categories": [
            "Evolution and Anthropology :: Discusses the development of mankind and the Anthropoid apes",
            "Geography and Geology :: Mentions the geographical changes and distribution of animals",
            "Historical Publications :: References to historical publications and authors"
        ],
        "book_title": "The Story of Atlantis and the Lost Lemuria",
        "chapter": "FOOTNOTES",
        "authors": [
            "W. Scott-Elliot"
        ],
        "typ": "chunk"
    },
    {
        "question": "What surmise did Haeckel make regarding Lemuria's role in human evolution, and how does the text clarify the actual development of mankind from Anthropoid apes?",
        "answer": "Haeckel surmised that \"Lemuria was the cradle of the human race as it now exists,\" as indicated in the text. However, the text clarifies this point by stating that \"it was not out of Anthropoid apes that mankind developed.\" This distinction is made to correct Haeckel's assumption about the evolutionary lineage of humans, emphasizing that while Lemuria played a crucial role in human history, the development of mankind did not proceed from Anthropoid apes. Further details on the actual position of Anthropoid apes in nature and their relation to human evolution are suggested to be discussed later in the text.",
        "categories": [
            "Geography and Geology :: Mentions the geographical changes and distribution of animals",
            "Evolution and Anthropology :: Discusses the development of mankind and the Anthropoid apes",
            "Historical Publications :: References to historical publications and authors"
        ],
        "book_title": "The Story of Atlantis and the Lost Lemuria",
        "chapter": "FOOTNOTES",
        "authors": [
            "W. Scott-Elliot"
        ],
        "typ": "chapter"
    }
]
```

This training data can be used to train large language models LLM's.