import os
import json
from typing import List

from ttk.models.text_models import ChunkModel, ChapterModel, BookModel

MIN_CHUNK_WORDS = 99  # The minimum number of word that must be in a chunk


class ProcessingError(Exception):
    pass


def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def read_file_list(input_list):
    with open(input_list, 'r', encoding="utf-8") as f:
        return f.read().splitlines()


def process_files(files: List[str], input_dir: str, output_dir: str, chapter_prefix: str = "=",
                  section_prefix: str = "==", subsection_prefix: str = "==="):
    for count, file_name in enumerate(files, start=1):
        print(f"{file_name} {count} :: file of {len(files)} files")
        process_single_file(file_name, input_dir, output_dir, chapter_prefix, section_prefix,
                            subsection_prefix)


def process_single_file(file_name: str, input_dir: str, output_dir: str, chapter_prefix: str = "=",
                        section_prefix: str = "==", subsection_prefix: str = "==="):
    full_path = os.path.join(input_dir, file_name)
    output_file_name = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")

    try:
        with open(full_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        book_model = parse_book(lines, chapter_prefix, section_prefix, subsection_prefix)
        write_output(output_file_name, book_model)
    except ProcessingError as e:
        print(f"#### Warning: {e} in {full_path}")


def parse_book(lines: List[str], chapter_prefix: str = "=", section_prefix: str = "==",
               subsection_prefix: str = "===") -> BookModel:
    """First line is the title, for example: The Philosophy of Freedom
       Second line is the comma separated list of authors, for example: Rudolf Steiner, Marie Steiner
       Third line is the publishing date and place, for example: Berlin, 1905

       Example for the text file header:

       The Philosophy of Freedom
       Rudolf Steiner, Marie Steiner
       Berlin, 1905

    Args:
        lines: All lines of the input text file
        chapter_prefix (str): The chapter prefix
        section_prefix (str): The section prefix
        subsection_prefix (str): The subsection prefix

    Returns:
        The book_model (Book)
    """
    # Extract the first metadata
    book_title = lines[0].strip()
    authors = lines[1].strip().split(",")
    publishing = lines[2].strip()

    book_model = BookModel(authors=authors, book_title=book_title, publishing=publishing)
    book_model.text = "\n".join(lines)
    book_model.num_words = len(book_model.text.split())
    book_model.num_characters = len(book_model.text)

    parse_chapters(lines[3:], book_model, chapter_prefix, section_prefix, subsection_prefix)
    return book_model


def parse_chapters(lines, book_model, chapter_prefix: str = "=", section_prefix: str = "==",
                   subsection_prefix: str = "==="):
    """
    Parses the lines of a book text to identify and create chapters and chunks.

    This function iterates over each line of the book text, identifying chapters
    and paragraphs, and creates chunks of text. A new chapter is started when a line
    begins with "= ". Paragraphs within chapters are identified by lines starting
    with "==". Text lines are accumulated into chunks, which are consolidated into
    chapters and added to the book model.

    Args:
        lines (list of str): The lines of text representing the book content.
        book_model (BookModel): The book model instance to which chapters will be added.
        chapter_prefix (str): The chapter prefix
        section_prefix (str): The section prefix
        subsection_prefix (str): The subsection prefix

    Raises:
        ProcessingError: If an error occurs during the parsing of chapters.
    """
    current_chapter = None
    chunks = []
    current_text = ""
    chapter_id = 0
    section = ""
    subsection = ""

    for idx, line in enumerate(lines):
        text = line.strip()
        if not text:
            if current_text:
                chunks.append(create_chunk(current_text, section, subsection))
                current_text = ""
            continue

        if text.startswith(f"{chapter_prefix} "):
            new_chapter = text.replace(chapter_prefix, "").strip()
            section = ""
            subsection = ""
            if current_chapter is not None:
                book_model.chapters.append(create_chapter(current_chapter, chapter_id, chunks))
                chunks = []
                chapter_id += 1
            current_chapter = new_chapter
            print("At chapter:", current_chapter)
        elif text.startswith(f"{section_prefix} "):
            subsection = ""
            section = text.replace(section_prefix, "").strip()
            print("At section", section)
        elif text.startswith(f"{subsection_prefix} "):
            subsection = text.replace(subsection_prefix, "").strip()
            print("At subsection", subsection)
        else:
            current_text += " " + text

    if current_chapter and chunks:
        book_model.chapters.append(create_chapter(current_chapter, chapter_id, chunks))


def create_chunk(text: str, section: str, subsection: str):
    chunk_model = ChunkModel(text=text.strip(), chunk_id=0,
                             num_characters=len(text),
                             num_words=len(text.split()), section=section, subsection=subsection)
    return chunk_model


def consolidate_chunks(chunks):
    """
    Consolidates a list of chunks into larger chunks based on a word count threshold.

    This function iterates over the provided chunks and consolidates smaller chunks
    into larger ones to ensure that each chunk meets a minimum word count requirement.
    If a chunk is smaller than the threshold, it is merged with the preceding chunk.
    Each new consolidated chunk is assigned a unique ID.

    Args:
        chunks (list of ChunkModel): The list of chunk models to be consolidated.

    Returns:
        list of Chunk: The list of consolidated chunk models with updated IDs and word counts.

    Raises:
        ProcessingError: If an error occurs during the consolidation of chunks.
    """
    decent_chunk_list = []
    decent_chunk = None
    for chunk in chunks:
        if chunk.num_words > MIN_CHUNK_WORDS:
            decent_chunk = chunk
            decent_chunk_list.append(decent_chunk)
        else:
            if decent_chunk is None:
                decent_chunk = chunk
                decent_chunk_list.append(decent_chunk)
            else:
                decent_chunk.text += "\n" + chunk.text
                decent_chunk.num_characters += len(chunk.text)
                decent_chunk.num_words += len(chunk.text.split())
    # Generate the chunk_id's
    for chunk_id, chunk in enumerate(decent_chunk_list):
        chunk.chunk_id = chunk_id

    return decent_chunk_list


def create_chapter(title, chapter_id, chunks):
    decent_chunks = consolidate_chunks(chunks)
    chapter_text = "\n\n".join(chunk.text for chunk in decent_chunks)
    num_characters = len(chapter_text)
    num_words = len(chapter_text.split())

    return ChapterModel(chapter=title, chapter_id=chapter_id,
                        text=chapter_text,
                        chunks=decent_chunks,
                        num_chunks=len(decent_chunks),
                        num_characters=num_characters,
                        num_words=num_words)


def write_output(output_file_name, book_model):
    with open(output_file_name, 'w') as output_file:
        json.dump(book_model.model_dump(), output_file, indent=4)
