import logging
from openai import OpenAI

from ttk.llm_processing.common_tools import process_answers
from ttk.models.text_models import BookModel
from ttk.models.config_models import QuestionAnsweringChunkConfigModel
from ttk.utils import request_llm, log_exception


def add_chunk_answers_to_questions(book: BookModel, config: QuestionAnsweringChunkConfigModel, file_path: str,
                                   save_to_file: bool = True, save_llm_request: bool = False):
    # Create the OpenAI client with config specific api key and url. The api key
    # read by the config Class and is not stored in the config
    openai_client = OpenAI(api_key=config.api_key, base_url=config.url)
    for chapter in book.chapters:
        for idx, chunk in enumerate(chapter.chunks):
            if not chunk.questions:
                continue
            if config.name not in chunk.questions:
                continue
            meta_model = chunk.questions[config.name]
            for question_id, question in enumerate(meta_model.questions):
                # Jump over already created answers
                num_existing_answers = len(question.answers)
                answers_to_create = config.number_of_answers - num_existing_answers
                if answers_to_create <= 0:
                    continue
                # Create context chunks
                context_chunks = "\n".join([chapter.chunks[cid].text for cid in meta_model.previous_chunk_ids])
                # Create the prompt based on the user configuration
                system_text = config.system_prompt
                user_text = config.user_prompt.format(book_title=book.book_title, chapter=chapter.chapter,
                                                      authors=",".join(book.authors), context_chunks=context_chunks,
                                                      chunk_text=chunk.text, question=question.question)
                messages = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
                # Generate the answers
                for idx in range(answers_to_create):
                    content = None
                    try:
                        # Call the LLM
                        content = request_llm(openai_client=openai_client, config=config, messages=messages)
                        if not content:
                            logging.error(f"No content created for file {file_path} chapter: {chapter.chapter}, "
                                          f"chunk: {chunk.chunk_id}")
                            continue
                        process_answers(book, config, content, file_path, question, save_to_file, system_text,
                                        user_text, save_llm_request)
                        message = f"Book: {book.book_title}, Chapter: {chapter.chapter}, " \
                                  f"{chapter.chapter_id + 1}/{len(book.chapters)}, " \
                                  f"chunk {chunk.chunk_id + 1}/{len(chapter.chunks)} " \
                                  f"Added answer number {idx + 1}/{config.number_of_answers} for question " \
                                  f"{question_id + 1}/{len(meta_model.questions)} :: identifier {config.name}"
                        print(message)
                        logging.info(message)
                    except Exception as e:
                        log_exception(book=book, chapter=chapter, chunk=chunk, content=content, e=e,
                                      file_path=file_path, meta_model=meta_model, save_to_file=save_to_file,
                                      system_text=system_text, user_text=user_text)
                        continue
