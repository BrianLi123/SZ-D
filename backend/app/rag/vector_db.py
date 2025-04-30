# backend/rag/vector_db.py
import os
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

# 环境变量配置
AZURE_OPENAI_EMB_SERVICE = os.getenv("AZURE_OPENAI_EMB_SERVICE")
AZURE_OPENAI_EMB_API_KEY = os.getenv("AZURE_OPENAI_EMB_API_KEY")
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")

def build_vector_store(index_name: str) -> AzureSearch:
    # 初始化Embeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-ada-002",
        openai_api_version="2024-02-15-preview",
        azure_endpoint=f"https://{AZURE_OPENAI_EMB_SERVICE}.openai.azure.com/",
        api_key=AZURE_OPENAI_EMB_API_KEY,
    )

    # 索引字段配置
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=1536,
            vector_search_profile_name="myHnswProfile"
        ),
        SimpleField(name="company", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="chatroomID", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="source", type=SearchFieldDataType.String),
    ]

    return AzureSearch(
        azure_search_endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
        azure_search_key=AZURE_SEARCH_KEY,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
        fields=fields
    )