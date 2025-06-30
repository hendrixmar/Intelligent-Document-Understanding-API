
import weaviate

from weaviate.classes.config import Configure, DataType, Property



def create_database():
    client = weaviate.connect_to_local(
        host="weaviate",
        port=8080
    )

    if client.collections.exists("Documents"):
        return

    # Creating a new collection with the defined schema
    client.collections.create(
        name="Documents",
        properties=[
            Property(
                name="document_name",
                data_type=DataType.TEXT,
            ),
            Property(
                name="entities",
                data_type=DataType.OBJECT,
            ),
            Property(
                name="document_content",
                data_type=DataType.TEXT,
            ),
            Property(
                name="document_type",
                data_type=DataType.TEXT,
            ),
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
