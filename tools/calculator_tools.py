from typing import List, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ArgsSchema
from pydantic import BaseModel, Field
from operations.math_operations import MathOperations

math_Operations=MathOperations()

# Encompass your custom tools in a toolkit class
class CalculatorTools():
    # Note: It's important that every field has type hints. BaseTool is a
    # Pydantic class and not having type hints can lead to unexpected behavior.
    class AdditionTool(BaseTool):
        name: str = "AdditionTool"
        description: str = "useful for when you need to add 2 numbers"
        return_direct: bool = True
        class AdditionInputModel(BaseModel):
            a: int = Field(description="first number")
            b: int = Field(description="second number")
        args_schema: Optional[ArgsSchema] = AdditionInputModel

        def _run(self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
           result = math_Operations.add(a, b)
           return str(result)

    class SubtractionTool(BaseTool):
        name: str = "SubtractionTool"
        description: str = "useful for when you need to add 2 numbers"
        return_direct: bool = True
        class SubtractionInputModel(BaseModel):
            a: int = Field(description="first number")
            b: int = Field(description="second number")
        args_schema: Optional[ArgsSchema] = SubtractionInputModel

        def _run(
            self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
            """Use the tool"""
            return str(a - b)

        async def _arun(
            self,
            a: int,
            b: int,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        ) -> str:
            """Use the tool asynchronously."""
            # If the calculation is cheap, you can just delegate to the sync implementation
            # as shown below.
            # If the sync calculation is expensive, you should delete the entire _arun method.
            # LangChain will automatically provide a better implementation that will
            # kick off the task in a thread to make sure it doesn't block other async code.
            return self._run(a, b, run_manager=run_manager.get_sync())    

    # Init above tools and make available
    def __init__(self) -> None:
        self.tools = [self.AdditionTool(), self.SubtractionTool()]

    # Method to get tools (for ease of use, made so class works similarly to LangChain toolkits)
    def tools(self) -> List[BaseTool]:
        return self.tools