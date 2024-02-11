from typing import Dict

from ttk.models.config_models import SummaryChunkConfigModel
from ttk.models.text_models import BookModel, ChapterModel, ChunkModel, QuestionMetaModel, QuestionModel, \
    ResultMetaModel, ResultModel


def remove_llm_request_from_question_model(meta_dict: Dict[str, QuestionMetaModel]):
    for key, meta in meta_dict.items():
        meta.llm_request = None
        for question in meta.questions:
            question.llm_request = None
            for answer in question.answers:
                answer.llm_request = None


def remove_llm_request_from_summaries(meta_dict: Dict[str, ResultMetaModel]):
    for meta in meta_dict.values():
        meta.llm_request = None
        for result in meta.results:
            result.llm_request = None


def remove_llm_requests_from_json(book: BookModel, config: SummaryChunkConfigModel, file_path: str,
                                  save_to_file: bool = True, save_llm_request: bool = False):
    print("Remove llm responses from book", book.book_title)
    book.category.llm_request = None
    for chapter in book.chapters:
        chapter.llm_request = None
        chapter.category.llm_request = None
        for chunk in chapter.chunks:
            chunk.llm_request = None
            chunk.category.llm_request = None
            if chunk.questions:
                remove_llm_request_from_question_model(meta_dict=chunk.questions)
                remove_llm_request_from_summaries(meta_dict=chunk.summaries)

        remove_llm_request_from_question_model(meta_dict=chapter.questions)
        remove_llm_request_from_summaries(meta_dict=chapter.summaries)

    remove_llm_request_from_question_model(meta_dict=book.questions)
    remove_llm_request_from_summaries(meta_dict=book.summaries)
