from langchain.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import Field, BaseModel
# load the LLM model
from llm import model

# load the create_agent 
from agent import create_agent

# load tools
from .tools import tavily_tool
tools = [tavily_tool]

# define the prompt for the first agent : "Research the Industry or the Company"
#Leverage the power of prompt engineering
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert market research assistant"
            "Your task is to research the industry and segment the company is working in."
            "Identify the company’s key offerings, strategic focus areas(e.g., operations, supply chain, customer experience, etc.)"
            "Respond with a detailed report with all the information gathered. A vision and product information on the industry should be fine as well."
            "Make sure to use the tavily_search_results_json tool for information.",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
research_agent=create_agent(model,tools,prompt)
"""Conduct a deep market research for"""
"""response=research_agent.invoke({"input": "this is the company ABC Steel"})
print(type(response["output"]))
print(response)
"""
