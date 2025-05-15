import random
from typing import Annotated, Literal, TypedDict
from langgraph.graph import Graph,StateGraph, START, END
from langgraph.graph.message import add_messages
from helpers import save_graph

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.prompts import load_mcp_prompt
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio

# https://github.com/paulrobello/mcp_langgraph_tools/blob/main/src/mcp_langgraph_tools/__main__.py
# https://tirendazacademy.medium.com/mcp-with-langchain-cabd6199e0ac

headers = {
  "accept": "application/json, text/plain, */*",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "en-US,en;q=0.9",
  "cache-control": "no-cache",
  "pragma": "no-cache",
  "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="118", "Google Chrome";v="118"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": '"Windows"',
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "content-type": "application/json",  # Added to allow POST method
}

async def main():
   async with sse_client("http://localhost:8000/sse/",headers=headers) as (read, write):
    # Open an MCP session to interact with the math_server.py tool.
    async with ClientSession(read, write) as session:
      # Initialize the session.
      await session.initialize()
      # Load tools
      tools = await load_mcp_tools(session)
        
        # Print tools from coroutine
      print("Tools: ", tools)
       
  


if __name__ == "__main__":
  asyncio.run(main())