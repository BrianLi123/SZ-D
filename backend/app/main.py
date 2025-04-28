from fastapi import FastAPI,APIRouter
import sys
import os

# 获取项目根目录路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)



# 创建应用实例
app = FastAPI(
    title="My FastAPI Service",
    version="1.0.0",
    debug=True
)



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