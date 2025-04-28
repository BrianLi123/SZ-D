# # app/dependencies.py
# async def handle_openai_errors():
#     try:
#         yield
#     except openai.APIError as e:
#         raise HTTPException(
#             status_code=503,
#             detail={
#                 "type": "api_error",
#                 "message": f"OpenAI API错误: {e.message}",
#                 "retryable": True
#             }
#         )
#     except openai.RateLimitError:
#         raise HTTPException(
#             429, 
#             "请求过于频繁，请稍后重试"
#         )

# # 在路由中使用
# @router.post("/chat")
# async def chat_endpoint(
#     request: ChatRequest, 
#     dependencies=Depends(handle_openai_errors)
# ):
#     ...