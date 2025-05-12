import os
import hashlib
from langchain_core.documents import Document
from typing import List, Dict
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

# 环境变量配置
def init_vector_store(index_name: str) -> AzureSearch:
    AZURE_OPENAI_EMB_SERVICE = os.getenv("AZURE_OPENAI_EMB_SERVICE")
    AZURE_OPENAI_EMB_API_KEY = os.getenv("AZURE_OPENAI_EMB_API_KEY")
    AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
    AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_SERVICE_KEY")

    # 初始化Embeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="embedding3L",
        openai_api_version="2024-02-15-preview",
        azure_endpoint=f"https://{AZURE_OPENAI_EMB_SERVICE}.openai.azure.com/",
        api_key=AZURE_OPENAI_EMB_API_KEY,
    )

    # 测试维度输出
    test_vector = embeddings.embed_query("test")
    print(f"模型实际输出维度：{len(test_vector)}")
    # 索引字段配置
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(
            name="metadata",
            type=SearchFieldDataType.String,
            filterable=True,
            retrievable=True
        ),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=3072,  # 改为 3072
            vector_search_profile_name="myHnswProfile"
        ),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="source", type=SearchFieldDataType.String),
    ]

    return AzureSearch(
        azure_search_endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
        azure_search_key=AZURE_SEARCH_KEY,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
        fields=fields
    )

def create_documents_from_results(results: dict) -> List[Document]:
    all_documents = []
    for category in ['acceptance', 'functional', 'schedule', 'team']:
        if category in results:
            category_items = results[category]
            for idx, item in enumerate(category_items):
                if isinstance(item, str):
                    content = item
                elif isinstance(item, dict) and 'content' in item:
                    content = item['content']
                else:
                    content = str(item)

                doc_id = hashlib.sha256(f"{category}_{idx}_{content}".encode()).hexdigest()[:32]

                doc = Document(
                    page_content=content,
                    metadata={
                        "category": category.title(),
                        "source": "results_dict"
                    },
                    id=doc_id
                )

                all_documents.append(doc)

    return all_documents