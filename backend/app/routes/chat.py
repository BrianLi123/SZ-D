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

# 创建路由实例
chat = APIRouter(prefix="/chat", tags=["Chat Operations"])



# 文件上传API
@chat.post("/upload")
async def upload_documents_for_chat(
    file: UploadFile = File(...)
):
    """为特定聊天室上传并索引文档"""
    try:
        temp_dir = tempfile.mkdtemp()
        file_paths = []
        
        # 保存上传文件到临时目录
        file_path = os.path.join(temp_dir, file.filename)
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        file_paths.append(file_path)
        file_name = Tender_2docblob(file_path)
        HandleRetriever().handle(file_name)
        
        return {
            "status": "processing",
            "message": f"已接收{len(file)}个文件，正在后台处理"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@chat.post("/upload")
async def upload_documents_for_chat(
    files: List[UploadFile] = File(...),
):
    """为特定聊天室上传并索引文档"""
    try:
        temp_dir = tempfile.mkdtemp()

        # 保存上传文件到临时目录
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

        

        
        
        
        # 添加清理任务
        background_tasks.add_task(shutil.rmtree, temp_dir)

        # 添加清理任务
        background_tasks.add_task(shutil.rmtree, temp_dir)
        
        return {
            "status": "processing",
            "message": f"已接收{len(files)}个文件，正在后台处理",
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

# 流式聊天API
@chat.post("/stream")
async def chat_stream(
    request: ChatRequest
):
    async def event_generator():
        try:
            # 构建用户提问
            print("进入这个接口了")
            # company = request.company
            retriever = AdvancedRetriever()   
            print("22222")
            prompt = " ".join(
                item["user"] for item in request.history if "user" in item
            ).strip()
            print("3333")
            # 流式生成响应
            async for token in stream_llm_response(prompt, retriever):
                yield f"data: {json.dumps({'token': token})}\n\n".encode()
                await asyncio.sleep(0.01)  # 控制输出频率
                
            yield "data: [DONE]\n\n".encode()
            
        except Exception as e:
            error = json.dumps({"error": str(e)})
            yield f"data: {error}\n\n".encode()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )



# 流式生成器
async def stream_llm_response(
    prompt: str,
    retriever: AdvancedRetriever
) -> AsyncGenerator[str, None]:
    try:
        # RAG上下文检索
        docs = await retriever._aget_relevant_documents(prompt)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # 构造增强prompt
        rag_prompt = f"""基于以下上下文回答：
        {context}
        
        问题：{prompt}
        
        请用中文以专业的技术文档风格回答，并标注引用来源。"""
        

        llm = AzureChatOpenAIUtil("gpt-4").llm
        
        # 流式生成
        async for chunk in llm.astream(rag_prompt):
            content = chunk.content if hasattr(chunk, 'content') else ""
            if content:
                yield content
                
    except Exception as e:
        yield f"[ERROR] 生成失败: {str(e)}"