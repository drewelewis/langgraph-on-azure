import os
from typing import List, Optional
from pydantic import BaseModel, Field

from github import Github
from github import Auth
from dotenv import load_dotenv
load_dotenv(override=True)

class GitHubOperations():
    def get_repo_list_by_username(self, user_name: str) -> str:
        try:
            g = Github(os.getenv('Github_PAT'), per_page=100)
            user=g.get_user(user_name)

            repo_list = []
            for repo in user.get_repos():
                repo_list.append(repo.name)
            
            g.close()
            return repo_list
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            g.close()
            
