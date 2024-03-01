# 1. Transform all ebooks into JSON format, so we can add summaries, question, answers and categories
books_to_json --input_list=./ebook_texts/00_file_list.txt --input_dir=./ebook_texts --output_dir=./json_save_llm_request

# 2. Generate the categories that can be used in the summary approach
augment_books add_categories --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_categories.py

# 3. Extract the categorical LLM requests and responses as a trainings dataset
extract_knowledge --typ CAT_LLM --json_file=json_save_llm_request/GA_345.json --output_file=training_data/GA_345_category_llm.json --indent=4

# 4. Create chunk summaries
augment_books add_chunk_summaries --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chunk_summaries.py

# 5. Extract the summaries LLM requests and responses as a trainings dataset
extract_knowledge --typ SUM_LLM --json_file=json_save_llm_request/GA_345.json --output_file=training_data/GA_345_summarie_llm.json --indent=4  --key=summaries

# 6. Create chunk summaries with reflection
augment_books add_chunk_summaries --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chunk_summaries_reflect.py

# 7. Extract the summaries LLM requests and responses as a trainings dataset
extract_knowledge --typ SUM_LLM --json_file=json_save_llm_request/GA_345.json --output_file=training_data/GA_345_summarie_reflected_llm.json --indent=4  --key=summaries_reflected
