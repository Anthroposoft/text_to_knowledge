import logging

from openai import OpenAI

from ttk.llm_processing.common_tools import process_questions
from ttk.models.text_models import BookModel, QuestionMetaModel
from ttk.models.config_models import QuestionChunkConfigModel
from ttk.utils import request_llm, log_exception


def add_chapter_questions(book: BookModel, config: QuestionChunkConfigModel, file_path: str,
                          save_to_file: bool = True, save_llm_request: bool = False):
    openai_client = OpenAI(api_key=config.api_key, base_url=config.url)

    for chapter in book.chapters:
        if config.name not in chapter.questions:
            chapter.questions[config.name] = QuestionMetaModel(context=config.context, chunk_id=None)
        quest_meta_model: QuestionMetaModel = chapter.questions[config.name]
        # Jump over already generated questions
        if len(quest_meta_model.questions) > 0:
            print(file_path, "Questions ", config.name, " present for chapter ", chapter.chapter, )
            continue
        system_text = config.system_prompt
        user_text = config.user_prompt.format(book_title=book.book_title,
                                              chapter=chapter.chapter,
                                              authors=",".join(book.authors),
                                              chapter_text=chapter.text)
        messages = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
        content = None
        try:
            content = request_llm(openai_client=openai_client, config=config, messages=messages)
            if not content:
                logging.error(f"No content created for file {file_path} chapter {chapter.chapter}")
                continue
            process_questions(book=book, chapter=chapter, chunk=None, config=config, content=content,
                              file_path=file_path, quest_meta_model=quest_meta_model, save_to_file=save_to_file,
                              system_text=system_text, user_text=user_text, save_llm_request=save_llm_request)
            message = f"Book: {book.book_title}, Chapter: {chapter.chapter}, " \
                      f"Added {chapter.num_questions} questions :: identifier {config.name}"
            print(message)
            logging.info(message)
        except Exception as e:
            log_exception(book=book, chapter=chapter, chunk=None, content=content, e=e, file_path=file_path,
                          meta_model=quest_meta_model, save_to_file=save_to_file, system_text=system_text,
                          user_text=user_text)
            continue
