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

from operations.github_operations import GitHubOperations

github_Operations=GitHubOperations()

class GithubTools():
    
    class GithubGetReposTool(BaseTool):
        name: str = "GithubGetReposTool"
        description: str = "useful for when you need get a list of repositories from a Github account"
        return_direct: bool = True
        
        class GithubRepoListToolInputModel(BaseModel):
            user_name: str = Field(description="user_name")

             # Validation method to check parameter input from agent
            @field_validator("user_name")
            def validate_query_param(user_name):
                if not user_name:
                    raise ValueError("GithubGetReposTool tool error: user_name parameter is empty")
                else:
                    return user_name
            
        args_schema: Optional[ArgsSchema] = GithubRepoListToolInputModel

        
                
        def _run(self, user_name: str) -> str:
            #return str(['repository1', 'repository2', 'repository3'])
            # repos=GitHubOperations.get_repo_list_by_username('drewelewis')
            repos=github_Operations.get_repo_list_by_username(user_name)
            return str(repos)


    class CodeSearchTool(BaseTool):
        name: str = "CodeSearchTool"
        description: str = "useful for when you need to search for code in a Github repository"
        return_direct: bool = True
        class CodeSearchQuery(BaseModel):
            query: str = Field(description="repository search query"),
            repository_name: str = Field(description="repository to search in")
        
        args_schema: Optional[ArgsSchema] = CodeSearchQuery

        def _run(self, query: str, repository_name: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
            """Use the tool"""

            # Public Web Github
            g = Github(auth=os.getenv('Github_PAT'))
            code=g.search_code(query, repository_name)


            # To close connections after use
            g.close()
            return str("")

    # Init above tools and make available
    def __init__(self) -> None:
        self.tools = [self.GithubGetReposTool()]

    # Method to get tools (for ease of use, made so class works similarly to LangChain toolkits)
    def tools(self) -> List[BaseTool]:
        return self.tools