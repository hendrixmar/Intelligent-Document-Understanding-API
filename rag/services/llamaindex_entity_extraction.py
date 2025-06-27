import json_repair
from llama_index.core.llms.function_calling import FunctionCallingLLM
from rag.domain.base_entity_extraction import BaseEntityExtractor

class LlamaIndexEntityExtractor(BaseEntityExtractor):

    def __init__(self, llm_provider: FunctionCallingLLM):
        self.llm_provider = llm_provider

    async def extract_entities(self, input_text: str) -> dict[str, list[str]]:
        """Add documents with optional metadata to the vector store."""

        completion = await self.llm_provider.acomplete(
         f"""
            You are an information extractor.
            Extract all meaningful named entities that is relevant from the type of document
            from the following text and return them as a JSON object.

            Text:
            {input_text}
        """
        )
        decoded_object = json_repair.repair_json(completion.text, return_objects=True)

        return decoded_object
