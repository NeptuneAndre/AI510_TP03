from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import psycopg2

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="<dbname>", user="<user>", password="<password>", host="<host>", port="<port>"
)
cursor = conn.cursor()

# Query data from PostgreSQL
query = "SELECT * FROM network_kpis"
cursor.execute(query)
data = cursor.fetchall()

# Azure Blob Storage credentials and connection
blob_service_client = BlobServiceClient(account_url="https://<storage_account_name>.blob.core.windows.net", credential=DefaultAzureCredential())
container_client = blob_service_client.get_container_client("<container_name>")
blob_client = container_client.get_blob_client("<blob_name>")

# Upload data to Blob Storage
blob_client.upload_blob(str(data))
