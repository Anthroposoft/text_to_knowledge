import logging

from openai import OpenAI

from ttk.llm_processing.common_tools import process_summary
from ttk.models.text_models import BookModel, ResultMetaModel
from ttk.models.config_models import SummaryChunkConfigModel
from ttk.utils import request_llm, log_exception


def add_chapter_summaries(book: BookModel, config: SummaryChunkConfigModel, file_path: str,
                          save_to_file: bool = True, save_llm_request: bool = False):
    """This method will add a detailed summary to the chapters of a book, make sure that the provided configuration
    describes the summary generation correctly and includes required format strings and the JSON output description

    Schreibe detaillierte und umfangreiche Unittests for the Funktion add_chapter_summaries().
    Benutze das Python unittest Modul. Stelle sicher, das detaillierte Testdaten generiert werden, sodass 3 Fragen
    beantwortet werden müssen. 
    Verwende Mock-Techniken für den request_llm() Call und alle weiteren Calls, die gemocked werden müssen.
    """

    openai_client = OpenAI(api_key=config.api_key, base_url=config.url)
    for chapter in book.chapters:
        if config.name not in chapter.summaries:
            chapter.summaries[config.name] = ResultMetaModel(context=config.context)
        sum_meta_model = chapter.summaries[config.name]
        num_summaries = len(sum_meta_model.results)

        # Check if sufficient number of summaries where generated for this chapter
        summaries_to_create = config.num_summaries - num_summaries
        # Continue, if all summaries where already created, AFTER the chunk_ids where checked
        if summaries_to_create <= 0:
            print(file_path, "Summary present for chapter ", chapter.chapter)
            continue
        # Create the prompt based on the user configuration
        system_text = config.system_prompt
        user_text = config.user_prompt.format(book_title=book.book_title, chapter=chapter.chapter,
                                              authors=",".join(book.authors), chapter_text=chapter.text)
        messages = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
        # Create several summaries if requested
        for idx in range(summaries_to_create):
            content = None
            try:
                content = request_llm(openai_client=openai_client, config=config, messages=messages)
                if not content:
                    logging.error(f"No content created for file {file_path} chapter {chapter.chapter}")
                    continue
                process_summary(book=book, config=config, content=content, file_path=file_path,
                                save_to_file=save_to_file, sum_meta_model=sum_meta_model, system_text=system_text,
                                user_text=user_text, save_llm_request=save_llm_request)
                print(file_path, "Chapter:", chapter.chapter, "summary ", idx, "added")

                message = f"Book: {book.book_title}, Chapter: {chapter.chapter} " \
                          f"{chapter.chapter_id + 1}/{len(book.chapters)}, " \
                          f"Added {idx + 1}/{summaries_to_create} summaries :: identifier {config.name}"
                print(message)
                logging.info(message)
            except Exception as e:
                log_exception(book=book, chapter=chapter, chunk=None, content=content, e=e, file_path=file_path,
                              meta_model=sum_meta_model, save_to_file=save_to_file, system_text=system_text,
                              user_text=user_text)
                continue
