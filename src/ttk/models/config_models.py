from pydantic import BaseModel


class ConfigBaseModel(BaseModel):
    system_prompt: str = ""
    user_prompt: str = ""
    temperature: float = 0.7
    model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    """The name of the model from the provided API host"""
    url: str = "http://localhost:1234/v1/"
    """The url of the API provider, that must be compatible with the OpenAI API.
    This can also be a local running LM Studio in local inference server mode"""
    api_key: str = "This is not an API key"
    """The API key that should be used to connect to the API"""
    max_tokens: int = 16768
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0
    sleep_time_between_api_calls: int = 0


class CategoryChunkConfigModel(ConfigBaseModel):
    """Chunk specific prompt for category generation

    The user prompt must contain the following string substitutions:

    {chunk_text}  - Formulate the prompt, so that the chunk_text is mentioned
    """
    pass


class ContextChunkBaseModel(ConfigBaseModel):
    context: str = ""
    """Description of the summary that gets generated: e.g. Complex summaries, short summaries, list of topics"""
    name: str = ""
    """The unique name of this summary that is used to identify it for chunks"""


class SummaryChunkConfigModel(ContextChunkBaseModel):
    """Chunk specific prompt for summaries generation

    The user prompt can contain the following string substitutions:

    {book_title}  - Formulate the prompt, so that the book title is mentioned
    {chapter}  - Formulate the prompt, so that the chapter is mentioned
    {authors}  - Formulate the prompt, so that the author is mentioned
    {context_chunks}  - Formulate the prompt, so that the context_chunks is mentioned
    {chunk_text}  - Formulate the prompt, so that the chunk_text is mentioned

    if events and person were found in categories, then these can be used in the summary using these identifiers:
    {events}
    {persons}
    """
    num_context_chunks: int = 10
    """The number of previous chunks that should be used as additional context to the current chunk for 
    question, answer and summary generation. This may help the LLM to have additional contextThe user prompt 
    must contain the variable {context_chunks}."""
    num_summaries: int = 1
    """The number of summaries that should be created from the same chunk to be able to compare them"""


class QuestionChunkConfigModel(ContextChunkBaseModel):
    """Chunk specific prompt for questions generation

    The user prompt can contain the following string substitutions:

    {book_summary} - This will include the book summary, if present to improve the context for question generation
    {chapter_summary} - This will include the chapter summary, if the number of chunks is greater 1, for better context
    {book_title}  - Formulate the prompt, so that the book title is mentioned
    {chapter}  - Formulate the prompt, so that the chapter is mentioned
    {authors}  - Formulate the prompt, so that the author is mentioned
    {context_chunks}  - Formulate the prompt, so that the context_chunks is mentioned
    {num_questions}  - Formulate the prompt, so that the num_questions is mentioned
    {chunk_text}  - Formulate the prompt, so that the chunk_text is mentioned
    """
    num_context_chunks: int = 10
    """The number of previous chunks that should be used as additional context to the current chunk for 
    question, answer and summary generation. This may help the LLM to have additional contextThe user prompt 
    must contain the variable {context_chunks}."""
    number_of_questions_div: int = 30
    """This parameters is used to compute the number of questions based on the number of words in the chunk.
    The number of question = num_words_chunk / number_of_questions_div """
    chapter_summarie_id: str = ""
    """The id of the chapter summary that should be used to add context to the question generation"""
    book_summarie_id: str = ""
    """The id of the book summary that should be used to add context to the question generation"""


class QuestionAnsweringChunkConfigModel(ContextChunkBaseModel):
    """Chunk specific prompt for questions answering

    The user prompt must contain the following string substitutions:

    {book_title}  - Formulate the prompt, so that the book title is mentioned
    {chapter}  - Formulate the prompt, so that the chapter is mentioned
    {authors}  - Formulate the prompt, so that the author is mentioned
    {context_chunks}  - Formulate the prompt, so that the context_chunks is mentioned
    {chunk_text}  - Formulate the prompt, so that the chunk_text is mentioned
    {question}  - Formulate the prompt, so that the chunk_text is mentioned
    """
    number_of_answers: int = 1
    """The number of answers that should be generated for a single question"""
