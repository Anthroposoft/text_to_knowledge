import json
import time
from typing import Union, Optional
import yaml

from ttk.models.config_models import SummaryChunkConfigModel, ConfigBaseModel, QuestionChunkConfigModel, \
    QuestionAnsweringChunkConfigModel
from ttk.models.text_models import BookModel, ChapterModel, ResultMetaModel, TextResponseModel, LLMRequestModel, \
    ResultModel, ChunkModel, QuestionMetaModel, ListOfTextResponseModel, QuestionModel
from ttk.utils import extract_json_from_text, save_book_to_file, extract_yaml_from_text


def process_summary(book: BookModel, config: Union[SummaryChunkConfigModel, ConfigBaseModel], content: str,
                    file_path: str, save_to_file: bool, sum_meta_model: ResultMetaModel, system_text: str,
                    user_text: str, save_llm_request: bool = False):
    """Process the summary from the large language model"""
    content = content.encode('utf-8').decode('utf-8')
    # Most of the time the error raises here
    if '```json' in content:
        response_model = TextResponseModel.model_validate(json.loads(extract_json_from_text(content)))
    elif '```yaml' in content:
        response_model = TextResponseModel.model_validate(yaml.safe_load(extract_yaml_from_text(content)))
    else:
        response_model = TextResponseModel(response=content)
    # Create the summary entries
    if save_llm_request is True:
        llm_request = LLMRequestModel(system=system_text, user=user_text, assistant=content)
    else:
        llm_request = None
    result_model = ResultModel(text=response_model.response, assessment=response_model.assessment,
                               llm_request=llm_request)
    sum_meta_model.results.append(result_model)
    # Since LLM calls are expensive, we save the file after each response
    save_book_to_file(book, file_path, save_to_file)
    if config.sleep_time_between_api_calls:
        time.sleep(config.sleep_time_between_api_calls)


def process_questions(book: BookModel, chapter: ChapterModel, chunk: Optional[ChunkModel],
                      config: QuestionChunkConfigModel,
                      content: str, file_path: str, quest_meta_model: QuestionMetaModel, save_to_file: bool,
                      system_text: str, user_text: str, save_llm_request: bool = False) -> int:
    list_model = ListOfTextResponseModel.model_validate(json.loads(extract_json_from_text(content)))
    question_list = []
    for question in list_model.text_list:
        question_list.append(QuestionModel(question=question.encode('utf-8').decode('utf-8')))

    if save_llm_request is True:
        llm_request = LLMRequestModel(system=system_text, user=user_text, assistant=content)
    else:
        llm_request = None
    quest_meta_model.llm_request = llm_request
    quest_meta_model.questions = question_list
    quest_meta_model.assessment = list_model.assessment
    num_questions = len(question_list)
    if chunk is not None:
        chunk.num_questions += num_questions
    else:
        chapter.num_questions += num_questions
    # Since LLM calls are expensive, we save the file after each response
    save_book_to_file(book, file_path, save_to_file)
    if config.sleep_time_between_api_calls:
        time.sleep(config.sleep_time_between_api_calls)
    return len(question_list)


def process_permutation_questions(book: BookModel, question_model: QuestionModel, config: QuestionChunkConfigModel,
                                  content: str, file_path: str, save_to_file: bool) -> int:
    question_model.permutations = [line for line in content.split("\n") if line.strip()]
    save_book_to_file(book, file_path, save_to_file)
    if config.sleep_time_between_api_calls:
        time.sleep(config.sleep_time_between_api_calls)
    return len(question_model.permutations)


def process_answers(book: BookModel, config: QuestionAnsweringChunkConfigModel, content: str,
                    file_path: str, question: QuestionModel, save_to_file: bool, system_text: str,
                    user_text: str, save_llm_request: bool = False):
    if '```json' in content:
        response_model = TextResponseModel.model_validate(json.loads(extract_json_from_text(content)))
    else:
        response_model = TextResponseModel(response=content)
    # Create the summary entries
    if save_llm_request is True:
        llm_request = LLMRequestModel(system=system_text, user=user_text, assistant=content)
    else:
        llm_request = None
    result_model = ResultModel(text=response_model.response, assessment=response_model.assessment,
                               llm_request=llm_request)
    question.answers.append(result_model)
    # Since LLM calls are expensive, we save the file after each response
    save_book_to_file(book, file_path, save_to_file)
    if config.sleep_time_between_api_calls:
        time.sleep(config.sleep_time_between_api_calls)
