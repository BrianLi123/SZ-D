# backend/api/routers/chat.py
from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List, AsyncGenerator
import tempfile
import os
import asyncio
import json
from api.models import ChatRequest, DocumentUploadRequest, SearchResult, HealthCheckResponse
from rag.data_loader import load_and_index_documents
from rag.advanced_retriever import AdvancedRetriever
from rag.tender_summary import HandleRetriever
from rag.blob_client import Tender_2docblob
# 初始化LLM（示例实现）
from utils.AzureChatOpenAIUtil import AzureChatOpenAIUtil
from typing import Optional
# 创建路由实例
chat = APIRouter(prefix="/chat", tags=["Chat Operations"])



# 文件上传API
@chat.post("/upload")
async def upload_documents_for_chat(
    file: UploadFile = File(...)
):
    """为特定聊天室上传并索引文档"""
    try:
        print("开始进入上传接口")
        temp_dir = tempfile.mkdtemp()
        file_paths = []
        
        # 保存上传文件到临时目录
        file_path = os.path.join(temp_dir, file.filename)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        file_paths.append(file_path)
        print("保存文件成功文件路劲是===",file_path)
        # file_name = Tender_2docblob(file_path)
        
        print("文件名是===",os.path.splitext(file.filename)[0])
        HandleRetriever().handle(os.path.splitext(file.filename)[0])
        
        return {
            "status": "processing",
            "message": f"数据上传成功！"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# 流式聊天API增强版（新增类别识别和过滤）
@chat.post("/stream")
async def chat_stream(
    request: ChatRequest
):
    async def event_generator():
        try:
            print("进入流式聊天接口")
            retriever = AdvancedRetriever()   
            
            # 提取用户历史提问
            prompt = " ".join(
                item["user"] for item in request.history if "user" in item
            ).strip()
            print(f"收到请求：{prompt}")
            
            # 流式生成响应
            async for token in stream_llm_response(prompt, retriever):
                # 关键修改：明确指定 JSON 编码
                json_data = json.dumps({'token': token}, ensure_ascii=False)
                yield f"data: {json_data}\n\n".encode('utf-8')
                await asyncio.sleep(0.01)
                
            yield "data: [DONE]\n\n".encode('utf-8')
            
        except Exception as e:
            # 关键修改：错误信息也使用 UTF-8 编码
            error = json.dumps({"error": str(e)}, ensure_ascii=False)
            yield f"data: {error}\n\n".encode('utf-8')

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream; charset=utf-8",  # 关键修改：添加字符集声明
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

# 增强的流式生成器（新增类别过滤）
async def stream_llm_response(
    prompt: str,
    retriever: AdvancedRetriever
) -> AsyncGenerator[str, None]:
    try:
        # 识别问题类别
        category = determine_category(prompt)
        print(f"识别到问题类别：{category or '无特定类别'}")
        
        # RAG上下文检索（带类别过滤）
        docs = await retriever._aget_relevant_documents(prompt, category=category)
        # context = "\n\n".join([f"【{doc.metadata['category']}类信息】{doc.page_content}" for doc in docs])
        
        print(f"检索到相关文档：{docs}")
        # 处理返回结果格式
        processed_docs = []
        for item in docs:
            if isinstance(item, tuple):
                # 假设元组格式为 (document, score)
                doc = item[0]
                if hasattr(doc, 'metadata'):
                    processed_docs.append(doc)
            elif hasattr(item, 'metadata'):
                processed_docs.append(item)
        
        if not processed_docs:
            yield "抱歉，没有找到相关信息。"
            return
            
        # 构建上下文，包含类别信息
        context = "\n\n".join([
            f"【{doc.metadata.get('category', '未知类别')}类信息】{doc.page_content}" 
            for doc in processed_docs
        ])

        # 构造增强prompt
        rag_prompt = f"""基于以下分类信息回答：
        {context}
        
        问题：{prompt}
        
        要求：
        1. 用中文回答，保持技术文档的专业性
        2. 严格根据信息类别筛选相关内容
        3. 标注引用来源的类别信息"""
        
        # 初始化LLM
        llm = AzureChatOpenAIUtil("gpt4o").llm
        
        # 流式生成
        async for chunk in llm.astream(rag_prompt):
            content = chunk.content if hasattr(chunk, 'content') else ""
            if content:
                yield content
                
    except Exception as e:
        yield f"[ERROR] 生成失败: {str(e)}"

def determine_category(prompt: str) -> Optional[str]:
    """智能识别问题类别"""
    category_keywords = {
        "schedule": ["schedule", "timeline", "deadline", "时间表", "进度"],
        "acceptance": ["acceptance", "验收标准", "验收条件", "sign-off"],
        "functional": ["functional", "功能需求", "feature", "功能点"],
        "team": ["team", "成员", "stakeholder", "角色", "负责人"]
    }
    
    prompt_lower = prompt.lower()
    for category, keywords in category_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            return category.title()  # 返回首字母大写的类别名称
    return None