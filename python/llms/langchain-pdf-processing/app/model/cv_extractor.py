"""Module for our CV information extractor, which extracts structured data from a CV
(in PDF format).

To get structured outputs, we use LangChain. We also use Openlayer's Python SDK `trace`
the `OpenlayerHandler` to trace all the calls to the model.
"""

from typing import Optional

from langchain_community.document_loaders import PyPDFLoader
from pydantic import BaseModel, Field
from langchain_openai.chat_models import ChatOpenAI
from openlayer.lib import trace
from openlayer.lib.integrations.langchain_callback import OpenlayerHandler


# This defines the Pydantic model we want our model to return
class CVStructuredData(BaseModel):
    name: str = Field(description="Candidate's full name")
    email: str = Field(description="Candidate's email address")
    github_profile_url: Optional[str] = Field(
        description="The URL of the candidate's GitHub profile. If not available, "
        "should be None."
    )
    linkedin_profile_url: Optional[str] = Field(
        description="The URL of the candidate's LinkedIn profile. If not available, "
        "should be None."
    )


class CVExtractorModel:
    """The CV data extractor LLM.

    This class wraps around a LangChain chat model and extracts structured data from
    a CV (in PDF format).
    """

    def __init__(self):
        """Make sure you import / instantiate your system here."""
        # Instantiate the Openlayer callback handler and pass it to the model for tracing
        openlayer_handler = OpenlayerHandler()
        model = ChatOpenAI(
            callbacks=[openlayer_handler],
        )
        self.model = model.with_structured_output(CVStructuredData)

    # Decorate the functions you'd like to trace with @trace()
    @trace()
    def read_cv(self, file_dir: str) -> str:
        """Reads the CV from PDF file and returns its content."""
        loader = PyPDFLoader(file_dir)
        pages = loader.load_and_split()
        return " ".join(list(map(lambda page: page.page_content, pages)))

    @trace()
    def extract(self, file_dir: str) -> CVStructuredData:
        """Extract structured data from the product review."""
        # Read the CV text from the PDF file
        cv_text = self.read_cv(file_dir)

        # Call the model
        response: CVStructuredData = self.model.invoke(cv_text)

        return response
