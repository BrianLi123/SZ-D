from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
import os
from azure.storage.blob import BlobServiceClient
import pickle

def Tender_2docblob(doc_link: str):

    AZURE_FORMRECOGNIZER_SERVICE = os.environ.get("AZURE_FORMRECOGNIZER_SERVICE")
    AZURE_FORMRECOGNIZER_SERVICE_KEY = os.environ.get("AZURE_FORMRECOGNIZER_SERVICE_KEY")
    
    AZURE_STORAGE_ACCOUNT = os.environ["AZURE_STORAGE_ACCOUNT"]
    AZURE_STORAGE_ACCOUNT_key = os.environ["AZURE_STORAGE_ACCOUNT_key"]
    CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT};AccountKey={AZURE_STORAGE_ACCOUNT_key};EndpointSuffix=core.windows.net"
    blob_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
   
    file_name = ".".join(doc_link.split('/')[-1].split('?')[0].split(".")[:-1])
    container_name = "tenderdocs"
    ###process
    endpoint = f"https://{AZURE_FORMRECOGNIZER_SERVICE}.cognitiveservices.azure.com/"
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=endpoint, api_key=AZURE_FORMRECOGNIZER_SERVICE_KEY, url_path=doc_link, api_model="prebuilt-layout"
    )
    docs = loader.load()
    ###upload doc class as pkl file
    pickled_docs = pickle.dumps(docs)
    blob_name = file_name + ".pkl"
    foucs_blob = blob_client.get_blob_client(container_name,blob_name)

    if foucs_blob.exists(): foucs_blob.delete_blob()
    blob_client.get_container_client(container_name).upload_blob(blob_name, pickled_docs)

    return file_name