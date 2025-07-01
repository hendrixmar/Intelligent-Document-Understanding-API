import json_repair
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.types import Model
from pydantic import BaseModel

from rag.domain.base_entity_extraction import BaseEntityExtractor
from rag.domain.models.document import DocumentCategory
from rag.domain.models.entities import (AdvertisementEntities, BudgetEntities,
                                        EmailEntities, FileFolderEntities, FormEntities,
                                        HandwrittenEntities, InvoiceEntities,
                                        LetterEntities, MemoEntities,
                                        NewsArticleEntities, PresentationEntities,
                                        QuestionnaireEntities, ResumeEntities,
                                        ScientificPublicationEntities,
                                        ScientificReportEntities, SpecificationEntities)


def _select_pydantic_model(category: DocumentCategory) ->  type[BaseModel]:

    match category:
        case DocumentCategory.ADVERTISEMENT:
            return AdvertisementEntities
        case DocumentCategory.BUDGET:
            return BudgetEntities
        case DocumentCategory.EMAIL:
            return EmailEntities
        case DocumentCategory.FILE_FOLDER:
            return FileFolderEntities
        case DocumentCategory.FORM:
            return FormEntities
        case DocumentCategory.HANDWRITTEN:
            return HandwrittenEntities
        case DocumentCategory.INVOICE:
            return InvoiceEntities
        case DocumentCategory.LETTER:
            return LetterEntities
        case DocumentCategory.MEMO:
            return MemoEntities
        case DocumentCategory.NEWS_ARTICLE:
            return NewsArticleEntities
        case DocumentCategory.PRESENTATION:
            return PresentationEntities
        case DocumentCategory.QUESTIONNAIRE:
            return QuestionnaireEntities
        case DocumentCategory.RESUME:
            return ResumeEntities
        case DocumentCategory.SCIENTIFIC_PUBLICATION:
            return ScientificPublicationEntities
        case DocumentCategory.SCIENTIFIC_REPORT:
            return ScientificReportEntities
        case DocumentCategory.SPECIFICATION:
            return SpecificationEntities
        case _:
            raise ValueError(f"Unsupported document category: {category}")


class LlamaIndexEntityExtractor(BaseEntityExtractor):

    def __init__(self, llm_provider: FunctionCallingLLM):
        self.llm_provider = llm_provider
        self.prompt = """
            You are an entity extraction assistant. Extract the followig text:
            {input_text}

            Respond with only the JSON output.

        """



    async def extract_entities(self, input_text: str, category: DocumentCategory) -> dict[str, list[str]]:
        """Add documents with optional metadata to the vector store."""


        program = LLMTextCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(output_cls=_select_pydantic_model(category)),
            prompt_template_str=self.prompt,
            verbose=True,
            llm=self.llm_provider
        )

        completion: BaseModel = await program.acall(input_text=input_text)

        return completion.model_dump(exclude_none=True)

