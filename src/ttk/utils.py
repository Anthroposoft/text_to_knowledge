# - utf-8 -
import json
import logging
import time
import traceback
from typing import List, Dict, Union

from openai import OpenAI
from openai.types.chat import ChatCompletion

from ttk.models.text_models import LLMRequestModel, LLMRequestStatus
from ttk.models.config_models import ConfigBaseModel, CategoryChunkConfigModel, SummaryChunkConfigModel, \
    QuestionChunkConfigModel


def setup_logging():
    logging.basicConfig(filename='text_to_knowledge.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def extract_json_from_text(text) -> str:
    # Define possible delimiters for JSON blocks
    delimiters = [("```json", "```"), ("'''json", "'''"), ("```python", "```"), ("'''python", "'''")]

    for start_delim, end_delim in delimiters:
        if start_delim in text:
            json_start = text.index(start_delim) + len(start_delim) + 1  # +1 for the newline after the delimiter
            try:
                json_end = text.index(end_delim, json_start)
            except ValueError:
                logging.error(f"The end of the JSON definition is missing. Text \n{text}")
                return ""  # Return an empty string if the end delimiter is missing
            return text[json_start:json_end].strip()
    # If no JSON block is found, return the entire text
    return text


def extract_yaml_from_text(text) -> str:
    # Finding the start and end of the YAML part
    if "```yaml" in text:
        start = text.index("yaml") + len("yaml\n")
        try:
            end = text.index("```", start)
        except ValueError:
            logging.error(f"The end of the YAML definition is missing. Text \n{text}")
            end = -1
        return text[start:end].strip()


def request_llm(openai_client: OpenAI, config: ConfigBaseModel, messages: List[Dict[str, str]]) -> str:
    """Create a LLM request

    :param openai_client: The initiated OpenAI client
    :param config: The configuration of the model
    :param messages: The prompts
    :return: the ChatCompletion object
    """

    logging.info(f"Request: {json.dumps(messages, indent=4)}")
    completion: ChatCompletion = openai_client.chat.completions.create(
        model=config.model,
        messages=messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        top_p=config.top_p,
        frequency_penalty=config.frequency_penalty,
        presence_penalty=config.presence_penalty,
        # response_format={"type": "json_object"}
    )
    logging.info(f"Response from LLM: {completion}")
    return completion.choices[0].message.content


def save_book_to_file(book, file_path, save_to_file):
    if save_to_file:
        with open(file_path, "w", encoding="utf-8") as f:
            book_json = book.model_dump_json(indent=4)
            f.write(book_json)


def log_exception(book, chapter, chunk, content, e, file_path, meta_model, save_to_file, system_text, user_text):
    if chunk is not None:
        message = f"Chapter: '{chapter.chapter}' Chunk: {chunk.chunk_id} :: Exception occurred: {str(e)}"
    elif chapter is not None:
        message = f"Chapter: '{chapter.chapter}' :: Exception occurred: {str(e)}"
    else:
        message = f"Exception occurred: {str(e)}"
    logging.error(message)
    logging.error(traceback.format_exc())
    print(message, traceback.format_exc())
    time.sleep(1)
    try:
        if content:
            llm_request = LLMRequestModel(system=system_text, user=user_text, assistant=content,
                                          status=LLMRequestStatus.parse_error)
            meta_model.llm_request = llm_request
            save_book_to_file(book, file_path, save_to_file)
    except Exception:
        logging.error("Exception raised while logging an exception")
        logging.error(traceback.format_exc())
        raise


def check_create_previous_chunks_summary(chunk_id: int, config: Union[
    CategoryChunkConfigModel, SummaryChunkConfigModel, QuestionChunkConfigModel, ConfigBaseModel],
                                         previous_chunk_ids: List[int], summaries_to_create):
    # Add chunk_id if the summaries were already created
    if summaries_to_create <= 0:
        if chunk_id not in previous_chunk_ids:
            previous_chunk_ids.append(chunk_id)
            return
    _check_chunks(chunk_id, config, previous_chunk_ids)


def check_create_previous_chunks_questions(chunk_id: int, config: Union[
    CategoryChunkConfigModel, SummaryChunkConfigModel, QuestionChunkConfigModel, ConfigBaseModel],
                                           previous_chunk_ids: List[int], quest_meta_model):
    # Add chunk_id if the questions were already created
    if len(quest_meta_model.questions) > 0:
        if chunk_id not in previous_chunk_ids:
            previous_chunk_ids.append(chunk_id)
            return
    _check_chunks(chunk_id, config, previous_chunk_ids)


def _check_chunks(chunk_id: int, config: Union[
    CategoryChunkConfigModel, SummaryChunkConfigModel, QuestionChunkConfigModel, ConfigBaseModel],
                  previous_chunk_ids: List[int]):
    # Add the previous chunks for context help
    if chunk_id > 0:
        if chunk_id - 1 not in previous_chunk_ids:
            previous_chunk_ids.append(chunk_id - 1)
    while len(previous_chunk_ids) > config.num_context_chunks:
        previous_chunk_ids.pop(0)
