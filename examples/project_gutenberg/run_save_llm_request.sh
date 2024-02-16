# 1. Transform all ebooks into JSON format, so we can add summaries, question, answers and categories
books_to_json --input_list=./ebook_texts/00_file_list.txt --input_dir=./ebook_texts --output_dir=./json_save_llm_request
# 2. Add two different summaries, a simpler and a reflective one to chunks, but only a single form to chapters
augment_books add_chunk_summaries --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chunk_summaries_detailed_config.py
augment_books add_chapter_summaries --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chapter_summaries_detailed_config.py
# 3. Create questions
augment_books add_chunk_questions --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chunk_questions_complex_config.py
augment_books add_chapter_questions --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chapter_questions_complex_config.py
# 4. Add answers to the questions
augment_books add_chunk_answers --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chunk_questions_answers_complex_config.py
augment_books add_chapter_answers --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_chapter_question_answers_complex_config.py
# 5. Create categories
augment_books add_categories --save_llm=True --input_dir=json_save_llm_request/ --config=configs/add_categories_config.py
