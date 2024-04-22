"""Module for my OpenAI model."""

from typing import Dict, List

import openai
from openlayer import llm_monitors


class OpenAIModel:
    """Class for an OpenAI model.

    The class instantiates the OpenAI client, wraps it in a monitor to enable tracing,
    and defines a `create_chat_completion` method.

    The `create_chat_completion` method is what's used throughout the app, to keep
    a single source of truth for the OpenAI client and its methods.
    """

    def __init__(self):
        """Make sure you import / instantiate your system here."""
        self.openai_client = openai.Client()

        # Wrap the OpenAI client in a monitor to enable tracing
        llm_monitors.OpenAIMonitor(client=self.openai_client)

    def create_chat_completion(
        self, messages: List[Dict[str, str]], stream: bool = False
    ) -> "openai.types.chat.chat_completion.ChatCompletion":
        """Wrapper for the OpenAI chat completion API."""
        return self.openai_client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
            stream=stream,
        )
