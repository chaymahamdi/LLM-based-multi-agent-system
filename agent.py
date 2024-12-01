#import librairies:
from langchain.agents import AgentExecutor, create_tool_calling_agent
from typing import List
from langchain.prompts import PromptTemplate


def create_agent(llm, 
                 tools: List, 
                 prompt: PromptTemplate,
                 verbose=True):
    # Construct the tool calling agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    executor = AgentExecutor(
                       agent=agent,
                       tools=tools,
                       verbose=verbose,
                    )
    return executor