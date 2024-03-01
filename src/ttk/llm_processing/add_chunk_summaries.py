import logging
from openai import OpenAI

from ttk.llm_processing.common_tools import process_summary
from ttk.models.text_models import BookModel, ResultMetaModel
from ttk.models.config_models import SummaryChunkConfigModel
from ttk.utils import request_llm, log_exception, check_create_previous_chunks_summary


def add_chunk_summaries(book: BookModel, config: SummaryChunkConfigModel, file_path: str,
                        save_to_file: bool = True, save_llm_request: bool = False):
    """This method will add a detailed summary to the chunks of a book, make sure that the provided configuration
    describes the summary generation correctly and includes required format strings and the YAML output description"""
    # Create the OpenAI client with config specific api key and url. The api key
    # read by the config Class and is not stored in the config
    openai_client = OpenAI(api_key=config.api_key, base_url=config.url)
    for chapter in book.chapters:
        previous_chunk_ids = []
        for chunk_id, chunk in enumerate(chapter.chunks):
            if config.name not in chunk.summaries:
                chunk.summaries[config.name] = ResultMetaModel(context=config.context, chunk_id=chunk_id)
            sum_meta_model = chunk.summaries[config.name]
            num_summaries = len(sum_meta_model.results)

            # Check if sufficient number of summaries where generated for this chunk
            summaries_to_create = config.num_summaries - num_summaries
            check_create_previous_chunks_summary(chunk_id, config, previous_chunk_ids, summaries_to_create)
            # Continue, if all summaries where already created, AFTER the chunk_ids where checked
            if summaries_to_create <= 0:
                print(file_path, "Summary present for chapter ", chapter.chapter, " with chunk id ", chunk.chunk_id)
                continue

            # Extract possible events from the category
            category_events = ""
            if chunk.category and chunk.category.events:
                category_events = "\n".join(chunk.category.events)

            # The chunk ids mus be stored to assure correct assessment of the generated summaries later on
            sum_meta_model.previous_chunk_ids = [i for i in previous_chunk_ids]
            # Create the context chunks for the LLM from the previous chunk ods
            context_chunks = "\n".join([chapter.chunks[cid].text for cid in previous_chunk_ids])
            # Create the prompt based on the user configuration
            system_text = config.system_prompt
            user_text = config.user_prompt.format(book_title=book.book_title, chapter=chapter.chapter,
                                                  authors=",".join(book.authors), context_chunks=context_chunks,
                                                  chunk_text=chunk.text, events=category_events)
            messages = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
            # Create several summaries if requested
            for idx in range(summaries_to_create):
                content = None
                try:
                    # Call the LLM
                    content = request_llm(openai_client=openai_client, config=config, messages=messages)
                    if not content:
                        logging.error(f"No content created for file {file_path} chapter {chapter.chapter}")
                        continue
                    process_summary(book=book, config=config, content=content, file_path=file_path,
                                    save_to_file=save_to_file, sum_meta_model=sum_meta_model, system_text=system_text,
                                    user_text=user_text, save_llm_request=save_llm_request)
                    message = f"Book: {book.book_title}, Chapter: {chapter.chapter} " \
                              f"{chapter.chapter_id + 1}/{len(book.chapters)}, " \
                              f"chunk {chunk.chunk_id + 1}/{len(chapter.chunks)} " \
                              f"Added {idx + 1}/{summaries_to_create} summaries :: identifier {config.name}"
                    print(message)
                    logging.info(message)
                    logging.info(content)
                except Exception as e:
                    log_exception(book=book, chapter=chapter, chunk=chunk, content=content, e=e, file_path=file_path,
                                  meta_model=sum_meta_model, save_to_file=save_to_file, system_text=system_text,
                                  user_text=user_text)
                    continue
