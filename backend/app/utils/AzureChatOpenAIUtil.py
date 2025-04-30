import os
from langchain_openai import AzureChatOpenAI
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel


# 配置模型信息 # [Setting] any LLM setting here
models = {
    'gpt-35-turbo-16k': {'endpoint': os.environ["AZURE_OPENAI_GPT35_SERVICE"],'key': os.environ["AZURE_OPENAI_GPT_API_KEY"], 'Model_Deployname': os.environ["AZURE_OPENAI_GPT_DEPLOYMENT"]},
    'gpt4': {'endpoint': os.environ["AZURE_OPENAI_GTP4_SERVICE_org"],'key': os.environ["AZURE_OPENAI_API_KEY_org"], 'Model_Deployname': os.environ["AZURE_OPENAI_GPT4"]},
    'gpt4-32k': {'endpoint': os.environ["AZURE_OPENAI_GTP4_SERVICE_org"],'key': os.environ["AZURE_OPENAI_API_KEY_org"], 'Model_Deployname': os.environ["AZURE_OPENAI_GPT4_32"]},
    'gpt4-turbo': {'endpoint': os.environ["AZURE_OPENAI_GTP4_SERVICE_T"],'key': os.environ["AZURE_OPENAI_API_KEY_T"], 'Model_Deployname': os.environ["AZURE_OPENAI_GPT4_T"]},
    'gpt4o': {'endpoint': os.environ["AZURE_OPENAI_GTP4_SERVICE_o"],'key': os.environ["AZURE_OPENAI_API_KEY_o"], 'Model_Deployname': os.environ["AZURE_OPENAI_GPT4_o"]},
    'gpt4o-2': {'endpoint': os.environ["AZURE_OPENAI_GTP4_SERVICE_o_2"],'key': os.environ["AZURE_OPENAI_API_KEY_o_2"], 'Model_Deployname': os.environ["AZURE_OPENAI_GPT4_o_2"]},
    'gpt4o-mini': {'endpoint': os.environ["AZURE_OPENAI_GTP4_SERVICE_o_mini"],'key': os.environ["AZURE_OPENAI_API_KEY_o_mini"], 'Model_Deployname': os.environ["AZURE_OPENAI_GPT4_o_mini"]},
    'textemb002': {'endpoint': os.environ["AZURE_OPENAI_EMB_SERVICE_002"],'key': os.environ["AZURE_OPENAI_EMB_API_KEY_002"], 'Model_Deployname': os.environ["AZURE_OPENAI_EMB_002"]},
    # 'Deekseek-R1': {'application_method':"AIF",'endpoint_full': os.environ["AIF_Deekseek_endpoint"],'key': os.environ["AIF_Deekseek_apikey"]},
    'gpt4o1-perview': {'endpoint': os.environ.get("AZURE_OPENAI_GTP4_SERVICE_o"),'key': os.environ.get("AZURE_OPENAI_API_KEY_o"), 'Model_Deployname': os.environ.get("AZURE_OPENAI_GPT4_o1"),'temperatures':1},
}


class AzureChatOpenAIUtil:

    """
    Sample usage:
    llm = AzureChatOpenAIUtil('gpt-35-turbo-16k', max_tokens=1000).llm
    """
    def __init__(self, model_name, max_tokens=None):
        self.model_name = model_name
        self.max_tokens = max_tokens if max_tokens is not None else self._get_default_max_tokens(model_name)
        self.llm = self.configure_openai(model_name)


    def _get_default_max_tokens(self, model_name):
        default_max_tokens = {
            'gpt-35-turbo-16k': 1000,
            'gpt4': 1000,
            'gpt4-32k': 1000,
            'gpt4-turbo': 2000,
            'gpt4o': 10000,
            'gpt4o-mini': 10000,
            'textemb002': 1000
        }
        return default_max_tokens.get(model_name, 4000)  

    def configure_openai(self, model_name):
        model_info = models[model_name]
        application_method = model_info.get('application_method') or "AzureOpenAI" ##[update] need update if there is more application_method
        temperature = model_info.get('temperatures') or 0

        if application_method == "AIF": #endpoint_full

            llm = AzureAIChatCompletionsModel(
                        endpoint=model_info['endpoint_full'],
                        credential=model_info['key'],
                        streaming=True,  # 确保开启流模式
                        max_retries=3,   # 增加重试机制
                        timeout=30.0     # 设置合理超时
                    )

        else:
        # 配置openai API
            endpoint =f"https://{model_info['endpoint']}.openai.azure.com"
            # 创建 AzureChatOpenAI 实例
            llm = AzureChatOpenAI(openai_api_version=model_info.get('openai_api_version') or "2023-07-01-preview",
                                azure_deployment=model_info['Model_Deployname'],
                                azure_endpoint=endpoint,
                                api_key=model_info['key'],
                                temperature = temperature,
                                #   max_tokens=self.max_tokens  # 使用设置的 max_tokens
                                streaming=True,  # 确保开启流模式
                                max_retries=3,   # 增加重试机制
                                timeout=30.0     # 设置合理超时
                                )
        
        return llm
    
    
    def generate_message(self, prompt, overrides=None):
        # 使用 AzureChatOpenAI 实例生成文本完成请求
        temperature = overrides.get("temperature") if overrides else 0.0
        max_tokens = overrides.get("max_tokens") if overrides else 900
        stop = overrides.get("stop") if overrides else ["<|im_end|>", "<|im_start|>"]

        # 生成消息
        completion = self.llm.generate_messages(
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop
        )
        return completion


