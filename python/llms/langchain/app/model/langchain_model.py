"""Module for my LangChain model."""

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from openlayer.lib.integrations import langchain_callback


class LangChainModel:
    """Class for a LangChain model.

    The class instantiates Openlayer's callback handler, which is used to enable
    tracing calls to chat completion LLMs with LangChain. It also defines an `invoke`
    method, which is used to call the model with a message and uses the callback
    handler.

    The `invoke` method is what's used throughout the app, to keep
    a single source of truth for the model.
    """

    def __init__(self):
        """Make sure you import / instantiate your system here."""
        self.openlayer_handler = langchain_callback.OpenlayerHandler()

    def invoke(self, message: str) -> str:
        """Wrapper for the chain / model invokation."""
        chat = ChatOpenAI(max_tokens=25, callbacks=[self.openlayer_handler])
        response = chat.invoke([HumanMessage(content=message)])
        return response.content
