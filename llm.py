#Groq LLM model
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

# Access the API key from the environment
groq_api_key = os.getenv("GROQ_API_KEY")
#Load LLama3-8B-8bit
model = ChatGroq(model="llama3-8b-8192")

