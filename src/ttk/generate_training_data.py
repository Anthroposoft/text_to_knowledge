import argparse
from typing import Dict, Optional

from ttk.models.text_models import BookModel, QuestionAnswerTrainingData, ChapterModel, \
    CategoryModel, ResultMetaModel, SummariesTrainingData
from ttk.utils import setup_logging


def generate_question_answer_pairs(book_model: BookModel, output_file: str, indent: Optional[int]):
    """Generate question answer pairs with additionally metadata

    :param book_model: The book model
    :param output_file: The output file
    :param indent: Indention of th generated json content
    """

    with open(output_file, "w", encoding="utf-8") as output:
        if indent is not None:
            output.write("[\n")
        for chapter in book_model.chapters:
            for chunk in chapter.chunks:
                if not chunk.questions:
                    continue
                extract_qa_pairs_with_metadata(book_model=book_model, chapter=chapter, questions=chunk.questions,
                                               original_text=chunk.text, output=output, category=chapter.category,
                                               indent=indent, typ="chunk")
            if not chapter.questions:
                continue
            extract_qa_pairs_with_metadata(book_model=book_model, chapter=chapter, questions=chapter.questions,
                                           original_text=chunk.text, output=output, category=chapter.category,
                                           indent=indent, typ="chapter")
        if indent is not None:
            output.write("\n]")


def extract_qa_pairs_with_metadata(book_model: BookModel, chapter: ChapterModel, questions: Dict, output,
                                   category: CategoryModel, original_text: str, indent: int = 0, typ: str = "chunk"):
    for meta in questions.values():
        for question in meta.questions:
            print(f"Write question:", question.question)
            if len(question.answers) > 0:
                m = QuestionAnswerTrainingData(question=question.question,
                                               original_text=original_text,
                                               answer=question.answers[0].text,
                                               categories=category.categories,
                                               book_title=book_model.book_title,
                                               typ=typ,
                                               chapter=chapter.chapter,
                                               authors=book_model.authors)
                if indent is not None:
                    line = m.model_dump_json(indent=int(indent)) + ",\n"
                else:
                    line = m.model_dump_json() + ",\n"
                output.write(line)


def generate_summary_output(book_model: BookModel, output_file: str, indent: Optional[int]):
    """Generate output that contains summaries for paragraphs or chapter with metadata

    :param book_model: The book model
    :param output_file: The output file
    :param indent: Indention of th generated json content
    :return:
    """
    with open(output_file, "w", encoding="utf-8") as output:
        if indent is not None:
            output.write("[\n")
        for chapter in book_model.chapters:
            for chunk in chapter.chunks:
                if not chunk.summaries:
                    continue
                print(f"Write summary for chapter {chapter.chapter}, chunk {chunk.chunk_id}")
                extract_summaries_with_metadata(book_model=book_model, chapter=chapter, summaries=chunk.summaries,
                                                original_text=chunk.text, output=output, category=chunk.category,
                                                indent=indent, typ="chunk")
            if not chapter.summaries:
                continue
            print(f"Write summary for chapter {chapter.chapter}")
            extract_summaries_with_metadata(book_model=book_model, chapter=chapter, summaries=chapter.summaries,
                                            original_text=chapter.text, output=output, category=chapter.category,
                                            indent=indent, typ="chapter")
        if indent is not None:
            output.write("\n]")


def extract_summaries_with_metadata(book_model: BookModel, chapter: ChapterModel, summaries: Dict[str, ResultMetaModel],
                                    output, category: CategoryModel, original_text: str, indent: int = 0,
                                    typ: str = "chunk"):

    for meta in summaries.values():
        for summary in meta.results:
            if len(summary.text) > 0:
                m = SummariesTrainingData(summary=summary.text,
                                          original_text=original_text,
                                          categories=category.categories,
                                          book_title=book_model.book_title,
                                          typ=typ,
                                          chapter=chapter.chapter,
                                          authors=book_model.authors)
                if indent is not None:
                    line = m.model_dump_json(indent=int(indent)) + ",\n"
                else:
                    line = m.model_dump_json() + ",\n"
                output.write(line)


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Extracts question/answer pairs and additional metadata from a book")
    parser.add_argument("--json_file", help="The filepath of the input book JSON file.")
    parser.add_argument("--output_file", help="The filepath to the output text or json file.")
    parser.add_argument("--indent", default=None, help="Use indention for the JSON output. 0 not indention, "
                                                       "number of spaces otherwise")
    parser.add_argument("--type", default="QA", choices=["QA", "SUM"],
                        help="The typ of information that should be extracted QA - Question/answer pairs, "
                             "SUM - Summaries and associated Paragraphs/Chapter.")
    args = parser.parse_args()

    with open(args.json_file, "r", encoding="utf-8") as f:
        book_json = f.read()
    book_model = BookModel.model_validate_json(book_json)
    if args.type == "QA":
        generate_question_answer_pairs(book_model, args.output_file, args.indent)
    if args.type == "SUM":
        generate_summary_output(book_model, args.output_file, args.indent)


if __name__ == "__main__":
    main()
