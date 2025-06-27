import json_repair
from llama_index.core.llms.function_calling import FunctionCallingLLM

from rag.domain.base_classifier import BaseDocumentClassifier



class LlamaIndexDocumentClassifier(BaseDocumentClassifier):

    def __init__(self, llm_provider: FunctionCallingLLM):
        self.llm_provider = llm_provider

    async def clustering(self, document: str) -> str:
        """Add documents with optional metadata to the vector store."""

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
                """.format(document=document)
        )
        decoded_object = json_repair.repair_json(completion.text, return_objects=True)

        return decoded_object
