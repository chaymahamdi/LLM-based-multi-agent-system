import operator
from typing import Annotated, Sequence, TypedDict,Union,List,Tuple
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
import functools
from langchain_core.messages import AIMessage
from langgraph.graph import END, StateGraph
#Import Agents:
from agents.research_market_agent import research_agent
from agents.usecase_agent import usecase_agent
from agents.resource_asset_agent import resource_assets_agent
#Import custom functions from utils.py
from utils import extract_use_cases,Colors
#Define the state of the graph
class MultiAgentState(TypedDict):
    user_query: str
    messages:Annotated[str,operator.add]
    results: List[dict]
#define agent Node 
def ResearchMarketAgent(state:MultiAgentState):
    input=state["user_query"]
    query=f"this is the company {input}"
    log={"Current agent":"Research Market Agent"}
    print(Colors.purble(f">>>{log}"), end="\n\n")
    response=research_agent.invoke({"input":query})["output"]
    return {"messages":response}

def UseCaseGenerationAgent(state:MultiAgentState):
    messages=state["messages"]
    log={"Current agent":"Use Case Generation Agent"}
    print(Colors.purble(f">>>{log}"), end="\n\n")
    response=usecase_agent.invoke({"input":messages[-1]})["output"]
    usecases=[]
    usecases=extract_use_cases(response)
    return {"messages":response,"results":usecases}

def AssetCollectionAgent(state:MultiAgentState):
    messages=state["messages"]
    log={"Current agent":"Asset Collection Agent"}
    print(Colors.purble(f">>>{log}"), end="\n")
    response=resource_assets_agent.invoke({"input":messages[-1]})["output"]
    return {"messages":response}

graph= StateGraph(MultiAgentState)
graph.add_node("ResearchMarketAgent", ResearchMarketAgent)
graph.add_node("UseCaseGenerationAgent", UseCaseGenerationAgent)
graph.add_node("AssetCollectionAgent",AssetCollectionAgent)

graph.set_entry_point("ResearchMarketAgent")
graph.add_edge("ResearchMarketAgent", "UseCaseGenerationAgent")
graph.add_edge("UseCaseGenerationAgent","AssetCollectionAgent")
graph.add_edge("AssetCollectionAgent", END)
system = graph.compile()
company="ABC steel"
for s in system.stream({"user_query": company}):
    print(s)
    print("--------------------")

