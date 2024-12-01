from langchain.tools import StructuredTool
from typing import List,Dict,Any
import re
import json

def make_tool(data:Dict[str,Any]) -> List:
    custom_tool= StructuredTool.from_function(
        func=data.get('func'),
        name=data['name'],
        description=data['description'],
        args_schema=data['args'],
        )
    return custom_tool
from enum import Enum
GLOBAL_COLORS = True
class Colors(Enum):
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    purble= '\033[95m'
    def __call__(self, message):
        if GLOBAL_COLORS:
            return f"{self.value}{message}\033[0m"
        return message

def extract_use_cases(output:str):
    use_cases=[]
    try:
      json_data=re.search(r'\[.*\]',output,re.DOTALL)
      if json_data:
         data=json_data.group(0)
         data = data.replace("'", '"')
         use_cases=json.loads(data)
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Error parsing JSON data: {e}")
    return use_cases
