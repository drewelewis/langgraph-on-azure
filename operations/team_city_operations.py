import os
from typing import List, Optional
from pydantic import BaseModel, Field

from dohq_teamcity import TeamCity
from dotenv import load_dotenv
load_dotenv(override=True)

TEAMCITY_URL=os.getenv('TEAMCITY_URL')
TEAMCITY_ADMIN=os.getenv('TEAMCITY_ADMIN')
TEAMCITY_ADMIN_PASSWORD=os.getenv('TEAMCITY_ADMIN_PASSWORD')


class TeamcityOperations():
    def get_projects(self) -> str:
        try:
            tc = TeamCity(TEAMCITY_URL, auth=(TEAMCITY_ADMIN, TEAMCITY_ADMIN_PASSWORD))
            # connect to TeamCity server
            projects = tc.projects.get_projects()
            return projects
        except Exception as e:
            print(f"An error occurred with TeamcityOperations.get_projects: {e}")
            return []
        finally:
            pass
    

TeamcityOperations = TeamcityOperations()
projects=TeamcityOperations.get_projects()
print(projects)
    
