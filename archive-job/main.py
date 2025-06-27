import os, json
import datetime
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

COSMOS_URI = os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
BLOB_CONN_STR = os.getenv("BLOB_CONN_STR")
ARCHIVE_CONTAINER = os.getenv("ARCHIVE_CONTAINER")

client = CosmosClient(COSMOS_URI, credential=COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
blob_container = blob_service_client.get_container_client(ARCHIVE_CONTAINER)

cutoff_date = (datetime.datetime.utcnow() - datetime.timedelta(days=90)).isoformat()

query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff_date}'"
archived = []

for item in container.query_items(query, enable_cross_partition_query=True):
    archived.append(item)
    blob_name = f"{item['id']}.json"
    blob_container.upload_blob(blob_name, json.dumps(item), overwrite=True)
    container.delete_item(item, partition_key=item['partitionKey'])

print(f"Archived {len(archived)} items.")
