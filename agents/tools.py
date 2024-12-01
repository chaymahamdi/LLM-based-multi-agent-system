from langchain_community.tools import TavilySearchResults,tool
import os

# define and customise the reserch_engine tool: tavily_tool
tavily_tool = TavilySearchResults(
    max_results=2,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=False, #our specific case doesn't require to retrieve images
)
