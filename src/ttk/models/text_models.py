from enum import Enum
from typing import List, Optional, Dict
import yaml

from pydantic import BaseModel


class LLMRequestStatus(Enum):
    success = 1
    parse_error = 2
    other_error = 3


class LLMRequestModel(BaseModel):
    """The LLM request that created the question, or answer or summary"""
    system: str = ""
    """The system prompt for the LLM"""
    user: str = ""
    """The user question and context"""
    assistant: str = ""
    """The answer of the LLM"""
    status: int = LLMRequestStatus.success.value


class CategoryModel(BaseModel):
    categories: List[str] = []
    """A list of categories"""
    keywords: List[str] = []
    """A list of keywords"""
    persons: List[str] = []
    """A list of persons in the text"""
    dates: List[str] = []
    """A list of dates in the text"""
    places: List[str] = []
    """A list of places in the text"""
    events: List[str] = []
    """A list of major events that took place in the text"""
    llm_request: Optional[LLMRequestModel] = None
    """The LLM request to answer tis question"""


class QualityModel(BaseModel):
    """Quality assessment of a LLM request result"""
    quality: int = 0
    assessment: str = ""


class ResultModel(BaseModel):
    text: str = ""
    """The text of the result"""
    assessment: str = ""
    """The assessment of the LLM for its own result"""
    quality: Optional[QualityModel] = None
    """The quality of the result"""
    llm_request: Optional[LLMRequestModel] = None
    """The LLM request that generated the result"""


class QuestionModel(BaseModel):
    """The question regarding a text from a chunk, summary or chapter"""
    question: str = ""
    """The question"""
    permutations: Optional[List[str]] = []
    """All permutations of this question"""
    answers: List[ResultModel] = []
    """The list of answers"""
    llm_request: Optional[LLMRequestModel] = None
    """The LLM request if the answer generation failed"""


class ResultMetaModel(BaseModel):
    """A list of text results with metadata"""
    context: str = "The context of these results: e.g. complex summaries, short summaries"
    results: List[ResultModel] = []
    chunk_id: Optional[int] = None
    previous_chunk_ids: List[int] = []
    llm_request: Optional[LLMRequestModel] = None
    """The LLM request that generated the result"""


class QuestionMetaModel(BaseModel):
    """A list of questions with metadata"""
    context: str = "The context of these questions: e.g. simple questions, complex questions, contradictory questions"
    questions: List[QuestionModel] = []
    assessment: str = ""
    chunk_id: Optional[int] = None
    previous_chunk_ids: Optional[List[int]] = []
    category: Optional[CategoryModel] = None
    """The category of this question and answers"""
    llm_request: Optional[LLMRequestModel] = None
    """The LLM request that created the summary and questions"""


class TextBaseModel(BaseModel):
    """Base model for chunks, chapter and book models"""
    text: str = ""
    """The Text"""
    category: Optional[CategoryModel] = None
    """The category of this text"""
    summaries: Dict[str, ResultMetaModel] = {}
    """Detailed summary of the text"""
    questions: Dict[str, QuestionMetaModel] = {}
    """A dict with question metadata models that include questions and answers that a related to this text"""
    num_characters: int = 0
    num_words: int = 0
    num_questions: int = 0
    llm_request: Optional[LLMRequestModel] = None
    """The LLM request that created the summary and questions"""


class ChunkModel(TextBaseModel):
    """A text chunk model"""
    chunk_id: int = 0
    """The id of the chunk, usually the number"""
    section: str = ""
    """The name of the section this chunk contains to"""
    subsection: str = ""
    """The name of the subsection this chunk contains to"""


class ChapterModel(TextBaseModel):
    chapter: str = ""
    """The title of the chapter"""
    chapter_id: int = 0
    num_chunks: int = 0
    """The name of the chapter"""
    chunks: Optional[List[ChunkModel]] = []
    """A list of chunks with or without overlap"""

    def count_questions(self):
        """Count the number of questions"""
        count = 0
        for chunk in self.chunks:
            count += chunk.num_questions
        # Add the chapter specific questions
        for item in self.questions.values():
            count += len(item.questions)
        return count

    def build_category_from_chunks(self):
        category = CategoryModel()
        has_data = False
        for chunk in self.chunks:
            if chunk.category:
                has_data = True
                category.categories.extend(chunk.category.categories)
                category.keywords.extend(chunk.category.keywords)
                category.persons.extend(chunk.category.persons)
                category.places.extend(chunk.category.places)
                category.dates.extend(chunk.category.dates)
                category.events.extend(chunk.category.events)
        if has_data:
            self.category = category
            self.category.categories = list(set(self.category.categories))
            self.category.keywords = list(set(self.category.keywords))
            self.category.persons = list(set(self.category.persons))
            self.category.places = list(set(self.category.places))
            self.category.dates = list(set(self.category.dates))
            self.category.events = list(set(self.category.events))


class BookModel(TextBaseModel):
    """Representation of a book"""
    authors: List[str] = []
    publishing: str = ""
    book_title: str = ""
    chapters: Optional[List[ChapterModel]] = []

    def count_questions(self):
        """Count the number of questions"""
        count = 0
        for chapter in self.chapters:
            count += chapter.count_questions()
        # Add the number of book specific questions
        for item in self.questions.values():
            count += len(item.questions)
        return count

    def build_category_from_chapters(self):
        category = CategoryModel()
        has_data = False
        for chapter in self.chapters:
            chapter.build_category_from_chunks()
            if chapter.category:
                has_data = True
                category.categories.extend(chapter.category.categories)
                category.keywords.extend(chapter.category.keywords)
                category.persons.extend(chapter.category.persons)
                category.places.extend(chapter.category.places)
                category.dates.extend(chapter.category.dates)
                category.events.extend(chapter.category.events)
        if has_data:
            self.category = category
            self.category.categories = list(set(self.category.categories))
            self.category.keywords = list(set(self.category.keywords))
            self.category.persons = list(set(self.category.persons))
            self.category.places = list(set(self.category.places))
            self.category.dates = list(set(self.category.dates))
            self.category.events = list(set(self.category.events))


class TextResponseModel(BaseModel):
    """Model to store the response from the LLM when it creates a text response"""
    response: str = ""
    assessment: str = ""


class ListOfTextResponseModel(BaseModel):
    """Model to store the response from the LLM when it creates a list of text"""
    text_list: List[str] = []
    assessment: str = ""


class QuestionAnswerTrainingData(BaseModel):
    """Model to store the response from the LLM when it creates question/answer pairs"""
    original_text: str = ""
    question: str = ""
    permutations: Optional[List[str]] = []
    answer: str = ""
    categories: List[str] = []
    book_title: str = ""
    chapter: str = ""
    authors: List[str] = []
    typ: str = ""  # Can be a chunk, chapter or book


class SummariesTrainingData(BaseModel):
    """Model to store the response from the LLM when it creates categories"""
    summary: str = ""
    original_text: str = ""
    categories: List[str] = []
    book_title: str = ""
    chapter: str = ""
    authors: List[str] = []
    typ: str = ""  # Can be a chunk, chapter or book
