"""Module for our review extractor model that takes in a product review and outputs
structured information about it.

To get structured outputs from the Claude model, we use `instructor`
(https://github.com/jxnl/instructor/). `instructor` is a Python library that
wraps around an AI model and ensures that it returns a Pydantic model as output.
"""

from typing import List, Optional
import anthropic
import instructor
from openlayer.lib import trace_anthropic
from pydantic import BaseModel, Field


# This defines the Pydantic model we want out model to return
class StructuredReview(BaseModel):
    """Structured data extracted from the product review."""

    summary: str = Field(description="A short summary of the product review.")
    sentiment: str = Field(
        description="The user sentiment of the review. Must be one of 'positive',"
        " 'negative', or 'neutral'."
    )
    features: List[str] = Field(
        description="A list of features of the product that were mentioned."
    )
    pros: Optional[List[str]] = Field(
        description="A list of pros of the product that were mentioned. If no pros were"
        " mentioned, this field should be None."
    )
    cons: Optional[List[str]] = Field(
        description="A list of cons of the product that were mentioned. If no cons were"
        " mentioned, this field should be None."
    )


class ReviewExtractorModel:
    """The review extractor LLM.

    This class wraps around Anthropic's Claude model and extracts structured data from
    a product review.

    To get structured outputs from the Claude model, we use `instructor`. We also
    use Openlayer's Python SDK `trace_anthropic` to tracing all the calls to the
    model.
    """

    def __init__(self):
        """Make sure you import / instantiate your system here."""
        client = anthropic.Anthropic()
        # First, wrap with Openlayer's `trace_anthropic` to enable tracing
        client = trace_anthropic(client)
        # Then, wrap with `instructor`'s `from_anthropic`, to ensure structured outputs
        client = instructor.from_anthropic(client)

        self.client = client

    def extract(self, review: str) -> StructuredReview:
        """Extract structured data from the product review."""
        response: StructuredReview = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system="You are a world class AI that excels at extracting useful data"
            " from a product review.",
            messages=[
                {
                    "role": "user",
                    "content": review,
                }
            ],
            response_model=StructuredReview,  # This tells the model to return structured outputs
        )
        return response
