import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 获取当前文件所在目录的父目录（即 backend/app/ 的父目录 backend/）
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 打印当前工作目录
print(f"当前工作目录: {os.getcwd()}")

# 指定.env文件的路径
dotenv_path = os.path.join(os.getcwd(),  '.env')
print(f"尝试加载的.env文件路径: {dotenv_path}")

# 加载.env文件
load_dotenv(dotenv_path)

# 检查环境变量是否加载成功
service_endpoint = os.getenv("AZURE_OPENAI_GPT35_SERVICE")
if service_endpoint is None:
    print("AZURE_OPENAI_GPT35_SERVICE 环境变量未加载成功。")
else:
    print("AZURE_OPENAI_GPT35_SERVICE 环境变量加载成功。")

from app.routes.chat import chat
from fastapi import FastAPI,APIRouter

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

app.include_router(chat)

@app.post("/chat/hkt2",tags=["hkt2"])
async def api_test2():
    return {"here":"Here"} 



# 注册路由
app.include_router(APIRouter(prefix="/api", tags=["示例"]))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发模式自动重启
    )