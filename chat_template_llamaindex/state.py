import os
import reflex as rx

from llama_index_client import ChatMessage, MessageRole
from llama_index.core.chat_engine import CondenseQuestionChatEngine

from traceloop.sdk.decorators import workflow

from chat_template_llamaindex.rag_utils import (
    load_remote_vector_store,
    get_engine,
)


# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    def load_engine(self):
        """Load the chat engine."""
        load_remote_vector_store()

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.openai_process_question

        async for value in model(question):
            yield value

    @workflow(name="chat-template-llamaindex-process-question")
    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.chats[self.current_chat]:
            messages.append(
                ChatMessage(
                    role=MessageRole.USER, content=qa.question, additional_kwargs={}
                )
            )
            messages.append(
                ChatMessage(
                    role=MessageRole.ASSISTANT, content=qa.answer, additional_kwargs={}
                )
            )

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session.
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=get_engine(),
            chat_history=messages,
            verbose=True,
        )
        streaming_response = chat_engine.stream_chat(question)

        # Stream the results, yielding after every word.
        for item in streaming_response.response_gen:
            # Ensure answer_text is not None before concatenation
            if item is not None:
                self.chats[self.current_chat][-1].answer += item
            else:
                # Handle the case where answer_text is None, perhaps log it or assign a default value
                # For example, assigning an empty string if answer_text is None
                self.chats[self.current_chat][-1].answer += ""
            self.chats = self.chats
            yield

        # Toggle the processing flag.
        self.processing = False
