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
from typing import Optional,Dict
import tiktoken
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
            
            # 提取用户提问
            userInput = request.history[-1]['user']
            print(f"收到请求：{userInput}")
            
            # 流式生成响应
            async for token in stream_llm_response(userInput,request.history, retriever):
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
    userInput: str,
    history: List[dict],
    retriever: AdvancedRetriever
) -> AsyncGenerator[str, None]:
    try:
        history = get_chat_history_as_text(history)
        print(f"历史记录：{history}")
        # 识别问题类别
        category = determine_category(userInput)
        print(f"识别到问题类别：{category or '无特定类别'}")
        
        # RAG上下文检索（带类别过滤）
        docs = await retriever._aget_relevant_documents(userInput, category=category)
        # context = "\n\n".join([f"【{doc.metadata['category']}类信息】{doc.page_content}" for doc in docs])
        
        print(f"检索到相关文档：{docs}")
        # 处理返回结果格式
        result_list = []
        for item in docs:
            doc = item[0]
            category = doc.metadata['category']
            try:
                page_content = eval(doc.page_content)
            except:
                page_content = doc.page_content
            record = {
                "category": category,
                "page_content": page_content
            }
            result_list.append(record)

        # 向量有点问题，这里暂时先处理下
        if category =="无特定类别":
            result_list = ""
        print(f"上下文：{result_list}")
        # 构造增强prompt
        rag_prompt = f"""
        Resources:
        {result_list}

        history:
        {history}
        
        Question:{userInput}
        
        [Requirements]
        1. ** Data Parsing and Table representation **
            Output complete information based on different categories (such as "Schedule", "Team", etc.) and organize it into separate Markdown tables. Each table should have an appropriate title (for example, for "Schedule", the title can be "ID", "Milestone", "Completion Date", "Deliverable";) For "Team", the title may include "Name", "Role", "Responsibilities".
            Logically sort the entries in each category (for example, schedules are sorted in chronological order and teams in hierarchical order).

        2. **Rich Content and Interpretation
            Add a brief description for each entry (for example, "Schedule" milestones, explanations of goals, key activities and dependencies;) For the "team" members, clarify their roles and professional knowledge.
            Analyze the data of each category (for example, assess the feasibility of progress and identify potential risks; Evaluate the team composition based on the project requirements.
            Infer the overall nature of the project and possible use cases based on cross-category data.

        3. **Visualization Recommendations**
           - Recommend the most suitable visualization type for each category (e.g., Gantt charts for schedules, organizational charts for teams, flowcharts for functional processes).
           - If using timelines/flowcharts, highlight critical paths, dependencies, or key milestones.

        4. **Best Practice Alignment**
           - Compare each category against industry best practices (e.g., software development lifecycle for schedules, Agile team structures for teams).
           - Propose 1-2 actionable optimization suggestions per category (e.g., adjusting timelines, reallocating resources, refining acceptance criteria).

        5. **Additional Notes**
           - Flag potential ambiguities or data gaps (e.g., conflicting timepoints, missing roles).
           - Highlight critical entries that require special attention (e.g., key deliverables, bottleneck tasks).

        [Output Format]
        - Use standard Markdown tables (separate columns with |).
        - Organize explanations under clear subheadings.
        - Include simple diagrams or Mermaid code for visualizations.
        - Ensure optimization suggestions are specific and evidence-based."""
        
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

def get_chat_history_as_text(history, include_last_turn=True, approx_max_tokens=1000) -> str:
    """安全处理可能缺失bot字段的对话历史"""
    encoder = tiktoken.get_encoding("cl100k_base")
    history_text = []
    current_tokens = 0
    processed_history = history if include_last_turn else history[:-1]

    for h in reversed(processed_history):
        # 安全获取字段（兼容bot键缺失或值为空）
        user_content = h.get("user", "[Deleted Content]")  # 处理user缺失
        bot_content = h.get("bot")  # 安全访问bot键
        
        # 构建对话段
        user_part = f"<|im_start|>user\n{user_content}\n<|im_end|>"
        bot_part = ""
        if bot_content:  # 仅在bot内容存在时添加
            bot_part = f"\n<|im_start|>assistant\n{bot_content}\n<|im_end|>"
        
        # 合并并计算TOKEN
        segment = user_part + bot_part
        try:
            segment_tokens = len(encoder.encode(segment))
        except Exception as e:
            print(f"Tokenization error: {e}")
            continue  # 跳过编码异常的片段
        
        # TOKEN控制
        if current_tokens + segment_tokens > approx_max_tokens:
            break
            
        history_text.insert(0, segment)
        current_tokens += segment_tokens
    
    return "\n\n".join(history_text)