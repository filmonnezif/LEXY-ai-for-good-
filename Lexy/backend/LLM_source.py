from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq  
import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI configuration
azure_openai_deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")  
azure_api_base = os.getenv("AZURE_API_BASE") 
azure_api_key = os.getenv("AZURE_API_KEY")  
azure_api_version = "2024-05-01-preview"  

# Initialize Azure OpenAI model via LangChain
llm = AzureChatOpenAI(
    azure_deployment=azure_openai_deployment_name,
    openai_api_version=azure_api_version,
    azure_endpoint=azure_api_base,
    openai_api_key=azure_api_key,
    model_name="gpt-4", 
)

# Groq configuration
groq_api_key = os.getenv("GROQ_API_KEY")#revoked for security reasons:)

llm_groq = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192",
)
