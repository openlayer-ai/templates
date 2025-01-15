"""Module for my RAG pipeline."""

import os
from typing import List

import numpy as np
import openai
from openlayer.lib import trace, trace_openai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CONTEXT_PATH = os.path.join(os.path.dirname(__file__), "contexts.txt")


class RagPipeline:
    """RAG pipeline.

    The main method is `query`, which answers to a user query with the LLM."""

    def __init__(self):
        # Wrap the OpenAI client with Openlayer's `trace_openai` to trace it
        self.openai_client = trace_openai(openai.OpenAI())

        self.vectorizer = TfidfVectorizer()
        with open(CONTEXT_PATH, "r", encoding="utf-8") as file:
            self.context_sections = file.read().split("%%%")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.context_sections)

    # Decorate the functions you'd like to trace with @trace()
    @trace()
    def query(self, user_query: str) -> str:
        """Main method.

        Answers to a user query with the LLM.
        """
        contexts = self.retrieve_contexts(user_query)
        prompt = self.prepare_prompt(user_query, contexts)
        answer = self.call_llm(prompt)
        return answer

    @trace()
    def retrieve_contexts(self, query: str) -> List[str]:
        """Context retriever.

        Given the query, returns the most similar context (using TFIDF).
        """
        query_vector = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(
            query_vector, self.tfidf_matrix
        ).flatten()
        most_relevant_idx = np.argmax(cosine_similarities)
        contexts = [self.context_sections[most_relevant_idx]]
        return contexts

    # You can also specify the name of the `context_kwarg` to unlock RAG metrics that
    # evaluate the performance of the context retriever. The value of the `context_kwarg`
    # should be a list of strings.
    @trace(context_kwarg="contexts")
    def prepare_prompt(self, query: str, contexts: List[str]):
        """Combines the query with the context and returns
        the prompt (formatted to conform with OpenAI models)."""
        return [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Answer the user query using only the following context: {contexts[0]}. \nUser query: {query}",
            },
        ]

    @trace()
    def call_llm(self, prompt):
        """Forwards the prompt to GPT and returns the answer."""
        response = self.openai_client.chat.completions.create(
            messages=prompt,
            model="gpt-4o",
        )
        return response.choices[0].message.content
