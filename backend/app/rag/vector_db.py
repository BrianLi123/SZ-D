# backend/rag/vector_db.py
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
AZURE_OPENAI_EMB_SERVICE = os.getenv("AZURE_OPENAI_EMB_SERVICE")
AZURE_OPENAI_EMB_API_KEY = os.getenv("AZURE_OPENAI_EMB_API_KEY")
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_SERVICE_KEY")

def init_vector_store(index_name: str) -> AzureSearch:
    print("AZURE_OPENAI_EMB_SERVICE-->", AZURE_OPENAI_EMB_SERVICE)
    print("AZURE_OPENAI_EMB_API_KEY-->", AZURE_OPENAI_EMB_API_KEY)
    print("AZURE_SEARCH_SERVICE-->", AZURE_SEARCH_SERVICE)
    print("AZURE_SEARCH_KEY-->", AZURE_SEARCH_KEY)
    print("index_name-->", index_name)
    # 初始化Embeddings
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="embedding3L",
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
        # SimpleField(name="company", type=SearchFieldDataType.String, filterable=True),
        # SimpleField(name="chatroomID", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="source", type=SearchFieldDataType.String),
    ]
    print("Creating Azure Search index...")
    return AzureSearch(
        azure_search_endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
        azure_search_key=AZURE_SEARCH_KEY,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
        fields=fields
    )

def create_documents_from_results(results: dict) -> List[Document]:
    """从分类结果创建带类别标签的文档列表"""
    all_documents = []
    
    # 遍历四个类别
    for category in ['acceptance', 'functional', 'schedule', 'team']:
        if category in results:
            category_items = results[category]
            
            # 处理该类别下的每个条目（假设每个条目是一个文本或对象）
            for idx, item in enumerate(category_items):
                # 提取文本内容（根据实际数据结构调整）
                if isinstance(item, str):
                    content = item  # 如果直接是文本
                elif isinstance(item, dict) and 'content' in item:
                    content = item['content']  # 如果是包含content字段的字典
                else:
                    # 处理其他格式（根据实际情况调整）
                    content = str(item)
                
                # 生成唯一ID（类别+索引确保唯一性）
                doc_id = hashlib.sha256(f"{category}_{idx}_{content}".encode()).hexdigest()[:32]
                
                # 构建文档对象
                doc = Document(
                    page_content=content,
                    metadata={
                        "category": category.title(),  # 转为首字母大写（如Acceptance）
                        "source": "results_dict"
                    },
                    id=doc_id
                )
                
                all_documents.append(doc)
    
    return all_documents