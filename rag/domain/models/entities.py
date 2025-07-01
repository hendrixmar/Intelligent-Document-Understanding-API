
from pydantic import BaseModel

class AdvertisementEntities(BaseModel):
    product_name: str | None = None
    brand: str | None = None
    offer_details: str | None = None
    target_audience: str | None = None
    date: str | None = None
    contact_info: str | None = None

class BudgetEntities(BaseModel):
    department: str | None = None
    fiscal_year: str | None = None
    total_budget: float | None = None
    allocations: str | None = None
    approver: str | None = None

class EmailEntities(BaseModel):
    sender: str | None = None
    recipient: str | None = None
    subject: str | None = None
    timestamp: str | None = None
    body: str | None = None

class FileFolderEntities(BaseModel):
    folder_name: str | None = None
    creator: str | None = None
    created_date: str | None = None
    number_of_files: int | None = None

class FormEntities(BaseModel):
    form_type: str | None = None
    submission_date: str | None = None
    submitted_by: str | None = None
    fields: list[str] | None = None

class HandwrittenEntities(BaseModel):
    author: str | None = None
    date: str | None = None
    location: str | None = None
    keywords: list[str] | None = None

class InvoiceEntities(BaseModel):
    invoice_number: str | None = None
    date: str | None = None
    due_date: str | None = None
    vendor_name: str | None = None
    customer_name: str | None = None
    total_amount: float | None = None
    items: list[str] | None = None

class LetterEntities(BaseModel):
    sender: str | None = None
    recipient: str | None = None
    date: str | None = None
    subject: str | None = None
    body: str | None = None

class MemoEntities(BaseModel):
    sender: str | None = None
    recipient: str | None = None
    subject: str | None = None
    date: str | None = None
    department: str | None = None

class NewsArticleEntities(BaseModel):
    headline: str | None = None
    author: str | None = None
    publication: str | None = None
    publish_date: str | None = None
    location: str | None = None
    topic: str | None = None

class PresentationEntities(BaseModel):
    title: str | None = None
    presenter: str | None = None
    organization: str | None = None
    date: str | None = None
    topics: list[str] | None = None

class QuestionnaireEntities(BaseModel):
    title: str | None = None
    creator: str | None = None
    date: str | None = None
    questions: list[str] | None = None
    target_group: str | None = None

class ResumeEntities(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    education: list[str] | None = None
    experience: list[str] | None = None
    skills: list[str] | None = None

class ScientificPublicationEntities(BaseModel):
    title: str | None = None
    authors: list[str] | None = None
    abstract: str | None = None
    journal: str | None = None
    doi: str | None = None
    publication_date: str | None = None

class ScientificReportEntities(BaseModel):
    title: str | None = None
    authors: list[str] | None = None
    organization: str | None = None
    date: str | None = None
    experiment_summary: str | None = None
    conclusion: str | None = None

class SpecificationEntities(BaseModel):
    spec_name: str | None = None
    version: str | None = None
    author: str | None = None
    release_date: str | None = None
    requirements: list[str] | None = None

