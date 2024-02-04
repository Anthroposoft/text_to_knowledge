# 1. Transform all ebooks into JSON format, so we can add summaries, question, answers and categories
# books_to_json --input_list=./ebook_texts/00_file_list.txt --input_dir=./ebook_texts --output_dir=./json
# 2. Add two different summaries, a simpler and a reflective one to chunks, but only a single form to chapters
augment_books add_chunk_summaries --input_dir=json/ --config=configs/add_detailed_chunk_summaries_config.py
augment_books add_chunk_summaries --input_dir=json/ --config=configs/add_detailed_chunk_summaries_reflect_config.py
augment_books add_chapter_summaries --input_dir=json/ --config=configs/add_detailed_chapter_summaries_config.py
# 3. Create questions
augment_books add_chunk_questions --input_dir=json/ --config=configs/add_complex_chunk_questions_config.py
augment_books add_chapter_questions --input_dir=json/ --config=configs/add_complex_chapter_questions_config.py
# 4. Add answers for the questions from step 3
augment_books add_chunk_answers --input_dir=json/ --config=configs/add_complex_chunk_questions_answers_config.py
augment_books add_chapter_answers --input_dir=json/ --config=configs/add_complex_chapter_questions_answers_config.py
# 5. Create categories
augment_books add_categories --input_dir=json/ --config=configs/add_categories_config.py
# 6. Extract Question and answer pairs with metadata
extract_qa_pairs --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant.txt
extract_qa_pairs --json_file=json/Kepler_from_Walter_Bryant.json --output_file=training_data/Kepler_from_Walter_Bryant.json --indent=4
extract_qa_pairs --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver.txt
extract_qa_pairs --json_file=json/Martin_Luther_from_Carl_Koppenhaver.json --output_file=training_data/Martin_Luther_from_Carl_Koppenhaver.json --indent=4
extract_qa_pairs --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.txt
extract_qa_pairs --json_file=json/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --output_file=training_data/The_Spiritual_Guidance_of_Man_and_of_Mankind_from_Rudolf_Steiner.json --indent=4
extract_qa_pairs --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training.txt
extract_qa_pairs --json_file=json/The_Story_of_Atlantis_and_the_lost_Lemuria.json --output_file=training_data/The_Story_of_Atlantis_and_the_lost_Lemuria_training.json --indent=4
