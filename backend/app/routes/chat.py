# backend/api/routers/chat.py
from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List, AsyncGenerator
import tempfile
import os
import shutil
import asyncio
import json
from ..api.models import ChatRequest, DocumentUploadRequest, SearchResult, HealthCheckResponse
from ..rag.data_loader import load_and_index_documents
from ..rag.vector_db import build_vector_store
from ..rag.advanced_retriever import AdvancedRetriever
# 初始化LLM（示例实现）
from ..utils.AzureChatOpenAIUtil import AzureChatOpenAIUtil


router = APIRouter(prefix="/chat", tags=["Chat Operations"])


# 依赖项注入
def get_retriever(request: ChatRequest):
    vector_store = build_vector_store(request.index_name)
    return AdvancedRetriever(
        vector_store=vector_store,
        company=request.chatroomID  # 使用chatroomID过滤
    )

# 文件上传API
@router.post("/upload")
async def upload_documents_for_chat(
    files: List[UploadFile] = File(...),
    company: str = Form(...),
    chatroomID: str = Form(...),
    index_name: str = Form("default-index"),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """为特定聊天室上传并索引文档"""
    try:
        temp_dir = tempfile.mkdtemp()
        file_paths = []
        
        # 保存上传文件到临时目录
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            file_paths.append(file_path)
        
        # 后台执行索引任务
        background_tasks.add_task(
            load_and_index_documents,
            file_paths=file_paths,
            index_name=index_name,
            company=company,
            additional_metadata={"chatroomID": chatroomID}
        )
        
        # 添加清理任务
        background_tasks.add_task(shutil.rmtree, temp_dir)
        
        return {
            "status": "processing",
            "message": f"已接收{len(files)}个文件，正在后台处理",
            "chatroomID": chatroomID
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 流式聊天API
@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    retriever: AdvancedRetriever = Depends(get_retriever)
):
    async def event_generator():
        try:
            # 构建用户提问
            prompt = " ".join(
                item["user"] for item in request.history if "user" in item
            ).strip()
            
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