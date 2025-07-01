
import weaviate

from weaviate.classes.config import Configure, DataType, Property



def create_database(host: str = "weaviate"):
    client = weaviate.connect_to_local(
        host=host,
        port=8080
    )

    if client.collections.exists("Documents"):
        return

    # Creating a new collection with the defined schema

    entity_nested_props = [
        {'data_type': DataType.TEXT, 'name': 'product_name'},
        {'data_type': DataType.TEXT, 'name': 'brand'},
        {'data_type': DataType.TEXT, 'name': 'offer_details'},
        {'data_type': DataType.TEXT, 'name': 'target_audience'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.TEXT, 'name': 'contact_info'},
        {'data_type': DataType.TEXT, 'name': 'department'},
        {'data_type': DataType.TEXT, 'name': 'fiscal_year'},
        {'data_type': DataType.NUMBER, 'name': 'total_budget'},
        {'data_type': DataType.TEXT, 'name': 'allocations'},
        {'data_type': DataType.TEXT, 'name': 'approver'},
        {'data_type': DataType.TEXT, 'name': 'sender'},
        {'data_type': DataType.TEXT, 'name': 'recipient'},
        {'data_type': DataType.TEXT, 'name': 'subject'},
        {'data_type': DataType.TEXT, 'name': 'timestamp'},
        {'data_type': DataType.TEXT, 'name': 'body'},
        {'data_type': DataType.TEXT, 'name': 'folder_name'},
        {'data_type': DataType.TEXT, 'name': 'creator'},
        {'data_type': DataType.TEXT, 'name': 'created_date'},
        {'data_type': DataType.TEXT, 'name': 'form_type'},
        {'data_type': DataType.TEXT, 'name': 'submission_date'},
        {'data_type': DataType.TEXT, 'name': 'submitted_by'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'fields'},
        {'data_type': DataType.TEXT, 'name': 'author'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.TEXT, 'name': 'location'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'keywords'},
        {'data_type': DataType.TEXT, 'name': 'invoice_number'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.TEXT, 'name': 'due_date'},
        {'data_type': DataType.TEXT, 'name': 'vendor_name'},
        {'data_type': DataType.TEXT, 'name': 'customer_name'},
        {'data_type': DataType.NUMBER, 'name': 'total_amount'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'items'},
        {'data_type': DataType.TEXT, 'name': 'sender'},
        {'data_type': DataType.TEXT, 'name': 'recipient'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.TEXT, 'name': 'subject'},
        {'data_type': DataType.TEXT, 'name': 'body'},
        {'data_type': DataType.TEXT, 'name': 'sender'},
        {'data_type': DataType.TEXT, 'name': 'recipient'},
        {'data_type': DataType.TEXT, 'name': 'subject'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.TEXT, 'name': 'department'},
        {'data_type': DataType.TEXT, 'name': 'headline'},
        {'data_type': DataType.TEXT, 'name': 'author'},
        {'data_type': DataType.TEXT, 'name': 'publication'},
        {'data_type': DataType.TEXT, 'name': 'publish_date'},
        {'data_type': DataType.TEXT, 'name': 'location'},
        {'data_type': DataType.TEXT, 'name': 'topic'},
        {'data_type': DataType.TEXT, 'name': 'title'},
        {'data_type': DataType.TEXT, 'name': 'presenter'},
        {'data_type': DataType.TEXT, 'name': 'organization'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'topics'},
        {'data_type': DataType.TEXT, 'name': 'title'},
        {'data_type': DataType.TEXT, 'name': 'creator'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'questions'},
        {'data_type': DataType.TEXT, 'name': 'target_group'},
        {'data_type': DataType.TEXT, 'name': 'name'},
        {'data_type': DataType.TEXT, 'name': 'email'},
        {'data_type': DataType.TEXT, 'name': 'phone'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'education'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'experience'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'skills'},
        {'data_type': DataType.TEXT, 'name': 'title'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'authors'},
        {'data_type': DataType.TEXT, 'name': 'abstract'},
        {'data_type': DataType.TEXT, 'name': 'journal'},
        {'data_type': DataType.TEXT, 'name': 'doi'},
        {'data_type': DataType.TEXT, 'name': 'publication_date'},
        {'data_type': DataType.TEXT, 'name': 'title'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'authors'},
        {'data_type': DataType.TEXT, 'name': 'organization'},
        {'data_type': DataType.TEXT, 'name': 'date'},
        {'data_type': DataType.TEXT, 'name': 'experiment_summary'},
        {'data_type': DataType.TEXT, 'name': 'conclusion'},
        {'data_type': DataType.TEXT, 'name': 'spec_name'},
        {'data_type': DataType.TEXT, 'name': 'version'},
        {'data_type': DataType.TEXT, 'name': 'author'},
        {'data_type': DataType.TEXT, 'name': 'release_date'},
        {'data_type': DataType.NUMBER_ARRAY, 'name': 'requirements'}
    ]
    # Creating a new collection with the defined schema
    client.collections.create(
        name="Documents",
        properties=[
            Property(
                name="document_name",
                data_type=DataType.TEXT,
            ),
            Property(
                name="document_content",
                data_type=DataType.TEXT,
            ),
            Property(
                name="document_type",
                data_type=DataType.TEXT,
            ),
            Property(
                name="document_entities",
                data_type=DataType.OBJECT,
                nested_properties=entity_nested_props
            )
        ],
        vectorizer_config=[
            Configure.NamedVectors.text2vec_transformers(
                name="semantic_vector",
                source_properties=["document_content"],
                # Further options
                pooling_strategy="masked_mean",
            )
        ]
    )

    client.close()
