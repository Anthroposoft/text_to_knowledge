import logging
from openai import OpenAI

from ttk.llm_processing.common_tools import process_permutation_questions
from ttk.models.text_models import BookModel, QuestionMetaModel, LLMRequestModel
from ttk.models.config_models import QuestionChunkConfigModel
from ttk.utils import request_llm, log_exception


def add_chunk_question_permutations(book: BookModel, config: QuestionChunkConfigModel, file_path: str,
                                    save_to_file: bool = True, save_llm_request: bool = False):
    """Add question permutations to questions already generated for chunks

    TODO: Add an LLM call to generate 10 - 20 permutations of each question
    TODO: Add an LLM call to define which category and event this question belongs to. Use the existing categories
          for the paragraph to let the LLM choose from

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
        generate_permutation_questions(book, chapter, config, file_path, openai_client, save_to_file, save_llm_request)


def generate_permutation_questions(book, chapter, config, file_path, openai_client, save_to_file, save_llm_request):
    for chunk_id, chunk in enumerate(chapter.chunks):
        quest_meta_model: QuestionMetaModel = chunk.questions[config.name]
        # Jump over already generated questions
        if not quest_meta_model.questions:
            continue
        for q_id, question_model in enumerate(quest_meta_model.questions):
            if len(question_model.permutations) > 0:
                print("Book:", book.book_title, "Permutation questions ", config.name,
                      " present for chapter ", chapter.chapter, " with chunk id ", chunk.chunk_id,
                      " question", question_model.question)
                continue
            user_text = config.user_prompt.format(question=question_model.question)
            system_text = config.system_prompt
            messages = [{"role": "system", "content": system_text},
                        {"role": "user", "content": user_text}]
            content = None
            try:
                content = request_llm(openai_client=openai_client, config=config, messages=messages)
                if not content:
                    logging.error(f"No content created for file {file_path} chapter: {chapter.chapter}, "
                                  f"chunk: {chunk.chunk_id}")
                    continue
                num_questions = process_permutation_questions(book=book,
                                                              question_model=question_model,
                                                              config=config,
                                                              content=content,
                                                              file_path=file_path,
                                                              save_to_file=save_to_file)

                if save_llm_request is True:
                    llm_request = LLMRequestModel(system="Follow the instructions of the user.",
                                                  user=user_text, assistant=content)
                else:
                    llm_request = None
                question_model.llm_request = llm_request
                message = f"Book: {book.book_title}, Chapter: {chapter.chapter} " \
                          f"{chapter.chapter_id + 1}/{len(book.chapters)}, " \
                          f"Chunk {chunk.chunk_id + 1}/{len(chapter.chunks)} " \
                          f"Question {q_id + 1}/{len(quest_meta_model.questions)} " \
                          f"Added {num_questions} permutation questions :: identifier {config.name}"
                print(message)
                logging.info(message)
            except Exception as e:
                log_exception(book=book, chapter=chapter, chunk=chunk, content=content, e=e, file_path=file_path,
                              meta_model=quest_meta_model, save_to_file=save_to_file, system_text="",
                              user_text=user_text)
                continue
