import weaviate
import pandas as pd
from weaviate.classes.config import Configure, DataType, Property


client = weaviate.connect_to_local()

def create_database():
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

create_database()
documents_collection = client.collections.get("Documents")

def insert():
    # Iterating through the wine_reviews dataset and storing it all in an array to be inserted later
    with documents_collection.batch.fixed_size() as batch:
        for index, row in data.iterrows():
            batch.add_object(properties={
                "title": row["title"] + '.',
                "description": row["description"],
            })

insert()

response = documents_collection.query.near_text(
    include_vector = True,
    query= "laptop",
    limit = 5,
    return_metadata = ["creation_time", "last_update_time", "distance", "certainty", "score", "explain_score", "is_consistent"]
)
for e in response.objects:
    print(e.properties)
client.close()
