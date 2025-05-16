import os
from typing import List, Optional
from pydantic import BaseModel, Field

from github import Github
from github import Auth
from dotenv import load_dotenv
load_dotenv(override=True)

class MathOperations():
    def add(self, number1: int, number2) -> int:
            try:
                return number1 + number2
            except Exception as e:
                print(f"An error occurred: {e}")
          
