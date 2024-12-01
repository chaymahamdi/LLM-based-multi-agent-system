from langchain.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import Field,BaseModel
# load the LLM model
from llm import model

# load the create_agent 
from agent import create_agent

# load tools
from .tools import tavily_tool
"""tools = [tavily_tool]"""
from langchain.tools import StructuredTool
from typing import List,Dict,Any

def search_engine(query:str):
    return tavily_tool.invoke({"query": query})
# Define the input schema

class Input(BaseModel):
    query: str = Field(description="search query string")
 
search_engine_tool= StructuredTool.from_function(
    func=search_engine,
    name="search_engine",
    description="""A search engine optimized for comprehensive, accurate, and trusted results. 
            Useful for when you need to answer questions about current events. Input should be a search query.""",
    args_schema=Input
)

# define the prompt for the first agent : "Market Standards & Use Case Generation"
#Leverage the power of prompt engineering
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert in market analysis and AI-driven innovation, collaborating with other assistants."
            "Based on the following reaserch market conducted : {input}"
            "Your task is to analyze industry trends and standards related to AI, ML, and automation."
            "Once your analysis and search are complete, respond only with a JSON-formatted list of use cases, each designed to help the company leverage GenAI, large language models (LLMs), and ML technologies to improve processes, enhance customer satisfaction, and boost operational efficiency."
            "Each use case should follow the JSON format:\n\n"
            "```{{\n"
            "  'Use Case': 'Use Case Title',\n"
            "  'Objective': 'Brief description of the objective or use case',\n"
            "  'AI Application': 'Explanation of how AI/ML/GenAI will be applied',\n"
            "  'Cross-Functional Benefit': {{\n"
            "    'Function 1': 'Explanation of benefit to this function',\n"
            "    'Function 2': 'Explanation of benefit to this function',\n"
            "    'Function n': 'Explanation'"        
            "  }}\n"
            "}}```\n"
            "Make sure to use the tavily_search_results_json tool for information."
        ),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
"""Ensure each use case has distinct objectives and applications relevant to the company's sector."""
tools=[tavily_tool]
usecase_agent=create_agent(model,tools,prompt)
input="""
Based on the information gathered from the tools, ABC Steel seems to be a company that operates in the steel industry, primarily manufacturing integrated steel products and selling them globally. They have multiple subsidiaries and brands, including CBC Steel Buildings, American Buildings Company, and Harris Steel Group, which focus on different aspects of the steel industry.

From the text, it appears that ABC Steel also has a sheet metal division, ABC Sheet Metal, which specializes in manufacturing and fabricating various metal products, including stainless steel and aluminum parts, for industries such as healthcare, medical, and commercial display.

Here is a summary of the information gathered:

* ABC Steel is a steel producer with global operations
* They have multiple subsidiaries and brands, including CBC Steel Buildings, American Buildings Company, and Harris Steel Group
* ABC Steel also has a sheet metal division, ABC Sheet Metal, which specializes in manufacturing and fabricating metal products

Please let me know if you would like me to continue gathering information or if you would like me to provide a summary of the industry and segment that ABC Steel operates in."""

"""response=usecase_agent.invoke({"input": input})
print(response)"""