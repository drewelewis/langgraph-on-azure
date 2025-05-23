import os
from typing import List, Optional, Type
from langchain_core.callbacks import  CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field, field_validator

from github import Github
from github import Auth
from dotenv import load_dotenv
load_dotenv(override=True)

from operations.elastic_search_operations import ElasticSearchOperations

elasticsearch_Operations=ElasticSearchOperations()

class ElasticsearchTools():
    class ElasticsearchSearchTool(BaseTool):
        name: str = "ElasticsearchSearchTool"
        description: str = """useful for when you need get items from an elasticsearch index.
        This tool can be used to search for logs in the elasticsearch index.
        The input to this tool should be a query string that is used to search the index.
        The query string should be in the format of a JSON object.
        Here are some examples: 
        # Example 1:  Get all log entries with levelname 'Error'
        {'match': {'levelname': 'Error'}}
        """
        return_direct: bool = True
        
        class ElasticsearchSearchToolInputModel(BaseModel):
            query: str = Field(description="query")

             # Validation method to check parameter input from agent
            @field_validator("query")
            def validate_query_param(query):
                if not query:
                    raise ValueError("ElasticsearchSearchTool tool error: query parameter is empty")
                else:
                    return query
            
        args_schema: Optional[ArgsSchema] = ElasticsearchSearchToolInputModel

        
                
        def _run(self,query) -> str:
            logs=elasticsearch_Operations.search(query)
            return str(logs)


    # Init above tools and make available
    def __init__(self) -> None:
        self.tools = [self.ElasticsearchSearchTool()]

    # Method to get tools (for ease of use, made so class works similarly to LangChain toolkits)
    def tools(self) -> List[BaseTool]:
        return self.tools