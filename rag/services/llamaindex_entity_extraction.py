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
            You are an entity extraction assistant.

            Extract all meaningful named entities from the following text. Output them in a **valid JSON object** with appropriate keys such as
            `"name"`, `"address"`, `"organization"`, `"product"`, `"location"`, `"date"`, `"email"`, or `"phone"` or any other field entity that is relevant in the text.

            Do not include entities that are not clearly identifiable.
            Ensure the output is strictly valid JSON and that the values are always a string.

            Here is the text:
            ---
            {input_text}
            ---
            Respond with only the JSON output.

        """
        )
        decoded_object = json_repair.repair_json(completion.text, return_objects=True)

        return decoded_object
