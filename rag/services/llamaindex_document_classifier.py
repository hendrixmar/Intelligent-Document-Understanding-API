from collections import Counter

import json_repair
from llama_index.core.llms.function_calling import FunctionCallingLLM

from rag.domain.base_classifier import BaseDocumentClassifier
from rag.domain.models.document import Document, DocumentCategory


class LlamaIndexDocumentClassifier(BaseDocumentClassifier):

    def __init__(self, llm_provider: FunctionCallingLLM):
        self.llm_provider = llm_provider

    async def clustering(self, document: Document) -> DocumentCategory | None:
        """Add documents with optional metadata to the vector store."""
        result = []
        for page in document.pages:
            for chunk in page.chunks:
                completion = await self.llm_provider.acomplete(
                    """
                        You are an document classifier.
                        this is the list of categories:
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
                        from the following text and return them as a JSON object with field category and the value.

                        Text:
                        {document}
                        """.format(document=chunk.text)
                )
                decoded_object = json_repair.repair_json(completion.text, return_objects=True)
                result.append(decoded_object)


        try:
            category, ocurrences = Counter(
                (
                    e.get("category", "no_category")
                    for e in result)
            ).most_common(1).pop()

            return DocumentCategory(category)
        except Exception:
            return None


