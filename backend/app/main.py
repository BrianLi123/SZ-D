from fastapi import FastAPI,APIRouter
from fastapi import FastAPI, HTTPException
import sys
import os
from dotenv import load_dotenv
from app.routes.chat import chat
# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# 指定.env文件的路径
dotenv_path = os.path.join(os.getcwd(), '.env', '.env')
load_dotenv(dotenv_path)

# 创建应用实例
app = FastAPI(
    title="智能文档分析系统",
    description="集成RAG的智能文档分析与问答系统",
    version="2.0.0",
    openapi_tags=[
        {
            "name": "Chat Operations",
            "description": "实时聊天与文档交互相关接口"
        }
    ]
)

app.include_router(chat.router)

@app.post("/chat/hkt2",tags=["hkt2"])
async def api_test2():
    return {"here":"Here"} 



# 注册路由
app.include_router(APIRouter(prefix="/api", tags=["示例"]))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发模式自动重启
    )