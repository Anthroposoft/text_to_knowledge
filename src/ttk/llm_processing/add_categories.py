import json
import time
from openai import OpenAI
from ttk.models.text_models import BookModel, CategoryModel, LLMRequestModel
from ttk.models.config_models import ConfigBaseModel
from ttk.utils import extract_json_from_text, setup_logging, request_llm, log_exception, save_book_to_file


def add_categories(book: BookModel, config: ConfigBaseModel, file_path: str, save_to_file: bool = True):
    # Create the OpenAI client with config specific api key and url. The api key
    # read by the config Class and is not stored in the config
    setup_logging()
    openai_client = OpenAI(api_key=config.api_key, base_url=config.url)
    for chapter in book.chapters:
        for chunk in chapter.chunks:
            if chunk.category:
                print(file_path, "Categories exist", chapter.chapter, "chunk", chunk.chunk_id)
                continue
            print("Book:", book.book_title," Adding categories to chunk", chunk.chunk_id, "of chapter", chapter.chapter)

            system_text = config.system_prompt
            user_text = config.user_prompt.format(chunk_text=chunk.text)

            messages = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
            content = None
            try:
                content = request_llm(openai_client=openai_client, config=config, messages=messages)
                if not content:
                    print("Book:", book.book_title, "Chapter:", chapter.chapter, " Chunk:", chunk.chunk_id, "No content!!")
                    continue
                llm_request = LLMRequestModel(system=system_text, user=user_text, assistant=content)
                chunk.category = CategoryModel.model_validate(json.loads(extract_json_from_text(content)))
                chunk.category.llm_request = llm_request

                # Since LLM calls are expensive, we save the file after each response
                save_book_to_file(book, file_path, save_to_file)
                if config.sleep_time_between_api_calls:
                    time.sleep(config.sleep_time_between_api_calls)
            except Exception as e:
                log_exception(book, chapter, chunk, content, e, file_path, chunk, save_to_file, system_text, user_text)
                continue
