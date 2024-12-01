import os
import json
from dotenv import load_dotenv
load_dotenv()
from langchain_community.tools import tool
from langchain.prompts import PromptTemplate, ChatPromptTemplate

# load the LLM model
from llm import model

# load the create_agent 
from agent import create_agent

### Define custom tool : "search_datasets_urls" ###
from exa_py import Exa
exa = Exa(api_key=os.environ["EXA_API_KEY"])
# specify the include_domains for the Exa search to platforms : Kaggle, github, huggingface
include_domains=["https://www.kaggle.com","https://github.com","https://huggingface.co"]
def search_and_contents(query: str):
    """Search for webpages based on the query and retrieve their contents."""
    # This combines two API endpoints: search and contents retrieval
    return exa.search_and_contents(
        query, use_autoprompt=True,include_domains=include_domains, num_results=6, text=True, highlights=True
    )
@tool
def search_datasets_urls(use_case):
    """Useful for when you need to search for datasets links for a given use case and returns back a list of urls.
       Input should be a use case query"""
    query=f"datasets for the use case {use_case}"
    response=search_and_contents(query)
    references = [result.url for result in response.results]
    asset=json.dumps({"Use Case":use_case,"Reference":references})
    with open("results/references.txt","a") as f:
        f.write(asset)
    return asset
tools=[search_datasets_urls]

### define the prompt for the first agent : "Resource Asset Collection" ###
#Leverage the power of prompt engineering
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert resource collection assistant, focused on gathering data and resources to support AI and GenAI use cases."
            "Based on the use cases provided from previous research: {input} "
            "For each use case, search for relevant datasets on platforms like Kaggle, HuggingFace, and GitHub"
            "Use the search_datasets_urls tool to search for datasets."
        ),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
resource_assets_agent=create_agent(model,tools,prompt)
"""response=research_agent.invoke({"input": "this is the company ABC Steel"})
print(response)"""

