from langchain_core.pydantic_v1 import BaseModel, Field
from utils.AzureChatOpenAIUtil import AzureChatOpenAIUtil
import pickle
from concurrent.futures import ThreadPoolExecutor
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from rag.vector_db import create_documents_from_results,init_vector_store
from azure.storage.blob import BlobServiceClient
import os
class HandleRetriever():
    def __init__(self):
        self.llm = AzureChatOpenAIUtil("gpt4o").llm

    def handle_error(self, future):
        try:
            result = future.result()
            return result
        except Exception as e:
            return {'error': str(e)}    
    def handle(self, file_name: str):


        AZURE_STORAGE_ACCOUNT = os.environ["AZURE_STORAGE_ACCOUNT"]
        AZURE_STORAGE_ACCOUNT_key = os.environ["AZURE_STORAGE_ACCOUNT_key"]
        CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT};AccountKey={AZURE_STORAGE_ACCOUNT_key};EndpointSuffix=core.windows.net"
        blob_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        # Load OCRed Tender Doc
        blob_name = file_name + ".pkl"
        container_name = "tenderdocs"
        print(f"processing container_name:{container_name},blob_name: {blob_name}")
        downloader = blob_client.get_blob_client(container_name, blob_name).download_blob()
        docs = pickle.loads(downloader.read())
        docs = docs[0].page_content

        # Convert doc data to a dictionary
        # Use multithreaded parallel processing
        with ThreadPoolExecutor() as executor:
            future_schedule = executor.submit(self.handle_Schedule, docs)
            future_acceptance = executor.submit(self.handle_Acceptance, docs)
            future_structure = executor.submit(self.handle_Team, docs)
            future_functional = executor.submit(self.handle_Functional, docs)
            # Wait for all threads to complete and handle errors
            results = {
                'schedule': self.handle_error(future_schedule),
                'team': self.handle_error(future_structure),
            }
            print('first 2 processed')
            results['acceptance'] = self.handle_error(future_acceptance)
            results['functional'] = self.handle_error(future_functional)


            # Prepare response data with error information
            response_data = {}
            # Add results to response_data, checking for errors
            for key, value in results.items():
                if isinstance(value, dict) and 'error' in value:
                    response_data[key] = value['error']
                else:
                    response_data[key] = value
        print("response_data:",response_data)  

        #开始入向量库
        print("🔄 正在初始化向量库...")
        vector_store = init_vector_store("brian-test")
        print("🔄 正在处理分类结果...")
        documents = create_documents_from_results(response_data)
        print(f"✅ 成功创建 {len(documents)} 个文档")
        print("🔄 正在写入数据...")
        vector_store.add_documents(documents)
        print("✅ 数据写入完成")
        return (response_data)

    # Schedule List
    def handle_Schedule(self,docs):
        class Request_2list(BaseModel):
        
            class RequestItem(BaseModel):
                Milestone: str = Field(..., description="project milestone")
                End_of_Date: list[str] = Field(..., description="date of the end of the project milestone")
                deliverables: list[str] = Field(..., description="deliverables in the milestone")
            request_list: list[RequestItem] = Field(
                    ..., description="list of schedule with detailed information"
            )
        parser = JsonOutputParser(pydantic_object=Request_2list)
        prompt = PromptTemplate(
            template="""providing details for each schedule in a list format
            \n{format_instructions}\n{query}\n""",
            input_variables=["query"],
            partial_variables={"format_instructions":parser.get_format_instructions()},
        )

        schedule_chain = prompt | self.llm | parser
        request_input = self.llm.invoke(f"""
                            OCR_text:
                            {docs}
                            Request:
                            "show Project Schedule in tabular table"
                            """)
        schedule_dicts = schedule_chain.invoke({"query": request_input})
        def convert_deliverables(data):
            """Converts deliverables list within a dictionary to a string with '<br>' as separator.
            Args:
                data: A list of dictionaries containing 'deliverables' as a list and 'Milestone' as a string.
            Returns:
                A list of dictionaries with 'deliverables' converted to a string with '<br>' as separator.
            """
            new_data = []
            for item in data:
                item['deliverables'] = ', '.join(item['deliverables'])
                new_data.append(item)
            return new_data
        return convert_deliverables(schedule_dicts["request_list"])
    # ACCEPTANCE
    def handle_Acceptance(self,docs):
        class Request_2list(BaseModel):
        
            class RequestItem(BaseModel):
                Milestone: str = Field(..., description="ACCEPTANCE CRITERIA milestone")
                Deliverables: list[str] = Field(..., description="List of Deliverables for acceptance criteria")
                Acceptance_Criteria: list[str] = Field(..., description="List of Acceptance Criteria for acceptance criteria")
            request_list: list[RequestItem] = Field(
                    ..., description="list of acceptance criteria with detailed information"
            )
        parser = JsonOutputParser(pydantic_object=Request_2list)
        prompt = PromptTemplate(
            template="""providing details for each acceptance criterion in a list format
            \n{format_instructions}\n{query}\n""",
            input_variables=["query"],
            partial_variables={"format_instructions":parser.get_format_instructions()},
        )

        acceptance_chain = prompt | self.llm | parser
        request_input = self.llm.invoke(f"""
                            OCR_text:
                            {docs}
                            Request:
                            "show acceptance criteria in tabular table"
                            """)
        acceptance_dicts = acceptance_chain.invoke({"query": request_input})

        return acceptance_dicts

        # Team Structure
    def handle_Team(self,docs):
        class Request_2list(BaseModel):
            class RequestItem(BaseModel):  # Define a separate model for each request item #"experience"
                Role: str = Field(..., description="role")
                Requirement: list[str] = Field(..., description="Role requirement")
            request_list: list[RequestItem] = Field(
                ..., description="List of role with detailed requirements"
            )
        # Define the prompt template with instructions for multiple skillsets
        parser = JsonOutputParser(pydantic_object=Request_2list)
        prompt = PromptTemplate(
            template="""providing details for each role in a list format
            \n{format_instructions}\n{query}\n""",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        # Create the chain with the updated prompt and model
        structure_chain = prompt | self.llm | parser

        request_input = self.llm.invoke(f"""
                            OCR_text:
                            {docs}

                            Request:
                            "show Team structure in tabular table"
                            """)
        structure_dicts = structure_chain.invoke({"query": request_input})
        return structure_dicts

    # Functional Points
    def handle_Functional(self,docs):   
        class Request_2list(BaseModel):
            class RequestItem(BaseModel):  # Define a separate model for each request item #"experience"
                Functional_point_title: str = Field(..., description="Functional point title, simplify within 5 words")
                Functional_point_detail: str = Field(..., description="full Functional point description")
            Functional_point_list: list[RequestItem] = Field(
                ..., description="List of functional point"
            )
        # Define the prompt template with instructions for multiple skillsets
        parser = JsonOutputParser(pydantic_object=Request_2list)
        prompt = PromptTemplate(
            template="""providing details for each functional point in a list format
            \n{format_instructions}\n{query}\n""",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        # Create the chain with the updated prompt and model
        functional_chain = prompt | self.llm | parser
        request_input = self.llm.invoke(f"""
                            OCR_text:
                            {docs}

                            Request:
                            "show Functional Point in tabular table"
                            """)
        functional_dicts = functional_chain.invoke({"query": request_input}) 
        return functional_dicts