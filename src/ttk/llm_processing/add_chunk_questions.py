import logging
from openai import OpenAI

from ttk.llm_processing.common_tools import process_questions, process_permutation_questions
from ttk.models.text_models import BookModel, QuestionMetaModel, LLMRequestModel
from ttk.models.config_models import QuestionChunkConfigModel
from ttk.utils import request_llm, log_exception, check_create_previous_chunks_questions


def add_chunk_questions(book: BookModel, config: QuestionChunkConfigModel, file_path: str,
                        save_to_file: bool = True, save_llm_request: bool = False):
    """Add questions to chunks

    :param book:
    :param config:
    :param file_path:
    :param save_to_file:
    :param save_llm_request:
    :return:
    """
    # Create the OpenAI client with config specific api key and url. The api key
    # read by the config Class and is not stored in the config
    openai_client = OpenAI(api_key=config.api_key, base_url=config.url)
    for chapter in book.chapters:
        generate_questions(book, chapter, config, file_path, openai_client, save_llm_request, save_to_file)


def generate_questions(book, chapter, config, file_path, openai_client, save_llm_request, save_to_file):
    previous_chunk_ids = []
    for chunk_id, chunk in enumerate(chapter.chunks):
        word_count = chunk.num_words
        num_questions = word_count // config.number_of_questions_div
        if num_questions < 1:
            num_questions = 1
        if config.name not in chunk.questions:
            chunk.questions[config.name] = QuestionMetaModel(context=config.context, chunk_id=chunk_id)
        quest_meta_model: QuestionMetaModel = chunk.questions[config.name]
        check_create_previous_chunks_questions(chunk_id, config, previous_chunk_ids, quest_meta_model)
        # Jump over already generated questions
        if len(quest_meta_model.questions) > 0:
            print("Book:", book.book_title, "Questions ", config.name, " present for chapter ", chapter.chapter,
                  " with chunk id ", chunk.chunk_id)
            continue
        # The chunk ids mus be stored to assure correct assessment of the generated summaries later on
        quest_meta_model.previous_chunk_ids = [i for i in previous_chunk_ids]
        # Create the context chunks for the LLM from the previous chunk ods
        context_chunks = "\n".join([chapter.chunks[cid].text for cid in previous_chunk_ids])
        system_text = config.system_prompt
        user_text = config.user_prompt.format(max_context_summaries=config.num_context_chunks,
                                              num_questions=num_questions,
                                              book_title=book.book_title,
                                              chapter=chapter.chapter,
                                              authors=",".join(book.authors),
                                              context_chunks=context_chunks,
                                              chunk_text=chunk.text)

        messages = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
        content = None
        try:
            content = request_llm(openai_client=openai_client, config=config, messages=messages)
            if not content:
                logging.error(f"No content created for file {file_path} chapter: {chapter.chapter}, "
                              f"chunk: {chunk.chunk_id}")
                continue
            num_questions = process_questions(book=book, chapter=chapter, chunk=chunk, config=config,
                                              content=content, file_path=file_path,
                                              quest_meta_model=quest_meta_model,
                                              save_to_file=save_to_file, system_text=system_text,
                                              user_text=user_text, save_llm_request=save_llm_request)
            message = f"Book: {book.book_title}, Chapter: {chapter.chapter} " \
                      f"{chapter.chapter_id + 1}/{len(book.chapters)}, " \
                      f"chunk {chunk.chunk_id + 1}/{len(chapter.chunks)} " \
                      f"Added {num_questions} questions :: identifier {config.name}"
            print(message)
            logging.info(message)
        except Exception as e:
            log_exception(book=book, chapter=chapter, chunk=chunk, content=content, e=e, file_path=file_path,
                          meta_model=quest_meta_model, save_to_file=save_to_file, system_text=system_text,
                          user_text=user_text)
            continue

