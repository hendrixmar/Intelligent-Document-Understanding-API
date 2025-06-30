from collections import Counter

import json_repair
from llama_index.core.llms.function_calling import FunctionCallingLLM

from rag.domain.base_classifier import BaseDocumentClassifier
from rag.domain.models.document import Document, DocumentCategory

from collections import Counter

import json_repair
from llama_index.core.llms.function_calling import FunctionCallingLLM

from rag.domain.base_classifier import BaseDocumentClassifier
from rag.domain.models.document import Document, DocumentCategory


class LlamaIndexDocumentClassifier(BaseDocumentClassifier):
    """
    Document classifier using an LLM from LlamaIndex to assign a category
    to a document based on its textual content.

    Attributes:
        llm_provider (FunctionCallingLLM): An instance of a function-calling LLM
            for processing and classifying document content.
    """

    def __init__(self, llm_provider: FunctionCallingLLM):
        """
        Initialize the classifier with an LLM provider.

        Args:
            llm_provider (FunctionCallingLLM): The LLM client used to classify document content.
        """
        self.llm_provider = llm_provider

    async def clustering(self, document: Document) -> DocumentCategory | None:
        """
        Classify the given document into a predefined category using an LLM.

        Each chunk of every page in the document is sent to the LLM for classification.
        The predicted categories are collected, and the most frequent category is returned.

        If the LLM fails to return valid JSON or no valid category is detected, `None` is returned.

        Args:
            document (Document): The document to classify.

        Returns:
            DocumentCategory | None: The most probable document category, or None if classification fails.
        """
        result = []

        for page in document.pages:
            for chunk in page.chunks:
                completion = await self.llm_provider.acomplete(
                    """
                    You are a document classifier.
                    This is the list of categories:
                        - advertisement
                        - budget
                        - email
                        - file_folder
                        - form
                        - handwritten
                        - invoice
                        - letter
                        - memo
                        - news_article
                        - presentation
                        - questionnaire
                        - resume
                        - scientific_publication
                        - scientific_report
                        - specification
                    From the following text, return the predicted category in a JSON object with the field `category`.

                    Text:
                    {document}
                    """.format(document=chunk.text)
                )

                decoded_object = json_repair.repair_json(completion.text, return_objects=True)
                result.append(decoded_object)

        try:
            category, _ = Counter(
                (e.get("category", "no_category") for e in result)
            ).most_common(1).pop()

            return DocumentCategory(category)
        except Exception:
            return None
