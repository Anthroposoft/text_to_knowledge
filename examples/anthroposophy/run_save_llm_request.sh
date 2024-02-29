# 1. Transform all ebooks into JSON format, so we can add summaries, question, answers and categories
books_to_json --input_list=./ebook_texts/00_file_list.txt --input_dir=./ebook_texts --output_dir=./json_save_llm_request

# 2. Generate the categories that can be used in the summary approach
augment_books add_categories --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_categories.py

