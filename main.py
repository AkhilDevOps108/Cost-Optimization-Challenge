```python
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
import os, json
from fastapi import FastAPI, HTTPException

app = FastAPI()

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

@app.get("/billing-record/{record_id}")
def get_billing_record(record_id: str):
    try:
        item = container.read_item(record_id, partition_key=record_id)
        return item
    except:
        blob_name = f"{record_id}.json"
        blob_client = blob_container.get_blob_client(blob_name)
        if blob_client.exists():
            data = blob_client.download_blob().readall()
            return json.loads(data)
        raise HTTPException(status_code=404, detail="Record not found")
