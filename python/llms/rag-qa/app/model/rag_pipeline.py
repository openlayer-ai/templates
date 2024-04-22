"""Module for my RAG pimenine."""

import numpy as np
import openai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from openlayer import llm_monitors
from openlayer.tracing import tracer

import os

CONTEXT_PATH = os.path.join(os.path.dirname(__file__), "contexts.txt")


class RagPipeline:
    """RAG pipeline.

    The main method is `query`, which answers to a user query with the LLM."""

    def __init__(self):
        # Wrap OpenAI client with Openlayer's OpenAIMonitor to trace it
        self.openai_client = openai.OpenAI()
        llm_monitors.OpenAIMonitor(client=self.openai_client)

        self.vectorizer = TfidfVectorizer()
        with open(CONTEXT_PATH, "r", encoding="utf-8") as file:
            self.context_sections = file.read().split("\n\n")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.context_sections)

    # Decorate the functions you'd like to trace with @tracer.trace()
    @tracer.trace()
    def query(self, user_query: str) -> str:
        """Main method.

        Answers to a user query with the LLM.
        """
        context = self.retrieve_context(user_query)
        prompt = self.inject_prompt(user_query, context)
        answer = self.generate_answer_with_gpt(prompt)
        return answer

    @tracer.trace()
    def retrieve_context(self, query: str) -> str:
        """Context retriever.

        Given the query, returns the most similar context (using TFIDF).
        """
        query_vector = self.vectorizer.transform([query])
        cosine_similarities = cosine_similarity(
            query_vector, self.tfidf_matrix
        ).flatten()
        most_relevant_idx = np.argmax(cosine_similarities)
        return self.context_sections[most_relevant_idx]

    @tracer.trace()
    def inject_prompt(self, query: str, context: str):
        """Combines the query with the context and returns
        the prompt (formatted to conform with OpenAI models)."""
        return [
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Answer the user query using only the following context: {context}. \nUser query: {query}",
            },
        ]

    @tracer.trace()
    def generate_answer_with_gpt(self, prompt):
        """Forwards the prompt to GPT and returns the answer."""
        response = self.openai_client.chat.completions.create(
            messages=prompt,
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content.strip()
