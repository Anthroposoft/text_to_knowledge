import argparse
from typing import Dict, Optional, Union
import json

from ttk.models.text_models import BookModel, QuestionAnswerTrainingData, ChapterModel, \
    CategoryModel, ResultMetaModel, SummariesTrainingData, LLMRequestModel, ChunkModel, QuestionModel, ResultModel
from ttk.utils import setup_logging


def generate_output(book_model: BookModel, output_file: str, indent: Optional[int], extract_fn):
    output_data = []
    for chapter in book_model.chapters:
        for chunk in chapter.chunks:
            if chunk:
                extract_fn(output_data, chunk, chunk.text, chapter, book_model)
        if chapter:
            extract_fn(output_data, chapter, chapter.text, chapter, book_model)

    with open(output_file, "w", encoding="utf-8") as output:
        if indent is not None:
            json.dump(output_data, output, indent=int(indent))
        else:
            json.dump(output_data, output)


def extract_qa_pairs(output_data, model, original_text: str, chapter: ChapterModel, book_model: BookModel):
    for meta in model.questions.values():
        for question in meta.questions:
            if len(question.answers) > 0:
                training_data = QuestionAnswerTrainingData(
                    question=question.question,
                    permutations=question.permutations,
                    original_text=original_text,
                    answer=question.answers[0].text,
                    categories=chapter.category.categories if chapter.category else [],
                    book_title=book_model.book_title,
                    typ="chunk" if isinstance(model, ChunkModel) else "chapter",
                    chapter=chapter.chapter,
                    authors=book_model.authors
                )
                output_data.append(training_data.model_dump())


def extract_summaries(output_data, model, original_text: str, chapter: ChapterModel, book_model: BookModel):
    for meta in model.summaries.values():
        for summary in meta.results:
            if len(summary.text) > 0:
                training_data = SummariesTrainingData(
                    summary=summary.text,
                    original_text=original_text,
                    categories=chapter.category.categories if chapter.category else [],
                    book_title=book_model.book_title,
                    typ="chunk" if isinstance(model, ChunkModel) else "chapter",
                    chapter=chapter.chapter,
                    authors=book_model.authors
                )
                output_data.append(training_data.model_dump())


def extract_cat_llm(output_data, model: Union[CategoryModel, ResultModel, QuestionModel], original_text: str,
                    chapter: ChapterModel, book_model: BookModel):
    if model.category and model.category.llm_request:
        output_data.append(model.category.llm_request.model_dump())


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Extracts question/answer pairs, summaries with additional metadata "
                                                 "from a book, as well as the LLM API calls that were used to generate "
                                                 "the data")
    parser.add_argument("--json_file", help="The filepath of the input book JSON file.")
    parser.add_argument("--output_file", help="The filepath to the output jsonl/json file.")
    parser.add_argument("--indent", default=None, help="Use indention for the JSON output. 0 not indention, "
                                                       "number of spaces otherwise")
    parser.add_argument("--type", default="QA", choices=["QA", "SUM", "CAT_LLM", "QA_LLM", "SUM_LLM"],
                        help="The typ of information that should be extracted QA - Question/answer pairs, "
                             "SUM - Summaries and associated Paragraphs/Chapter as well as the LLM request/responses.")
    args = parser.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as f:
        book_json = f.read()
    book_model = BookModel.model_validate_json(book_json)

    extract_fns = {
        "QA": extract_qa_pairs,
        "SUM": extract_summaries,
        "CAT_LLM": extract_cat_llm
    }

    if args.type in extract_fns:
        extract_fn = extract_fns[args.type]
        generate_output(book_model, args.output_file, args.indent, extract_fn)


if __name__ == "__main__":
    main()
