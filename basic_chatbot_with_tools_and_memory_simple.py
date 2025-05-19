import os
import json
from time import sleep
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.utils.function_calling import format_tool_to_openai_function

from langchain_openai import AzureChatOpenAI
from IPython.display import Image, display
from langchain_community.tools.tavily_search import TavilySearchResults

from helpers import save_graph
from dotenv import load_dotenv

from tools.calculator_tools import CalculatorTools
from tools.github_tools import GithubTools

load_dotenv(override=True)

class GraphState(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

system_message = """You are a helpful assistant. Your name is Bob. Be very silly and funny.
When possible, use your tools to answer the user's questions.
If there is no tool available, you can answer the question directly.
If you are asked about GitHub repositories, you can use the GitHub tool to search for them.
If you are asked to list GitHub repositories, the default user_name is drewelewis
If you are asked to list GitHub repositories, the default repository is 'bny-msft-ai-colab'.
Before using the GitHub tool, you should check if the user has provided a user_name and repository.
Only call the GitHub tool if the user has provided a user_name and repository.
If you dont have the user_name and repository, you can use the default user_name and repository.


   """.strip()

llm  = AzureChatOpenAI(
    azure_endpoint=os.getenv('OPENAI_API_ENDPOINT'),
    azure_deployment=os.getenv('OPENAI_API_MODEL_DEPLOYMENT_NAME'),
    api_version=os.getenv('OPENAI_API_VERSION'),
    temperature=0,
    streaming=True
)

tavily_tool = TavilySearchResults(max_results=2)
calculator_tools = CalculatorTools()
github_tools = GithubTools()
tools= calculator_tools.tools + github_tools.tools
llm_with_tools = llm.bind_tools(tools)

# Define Nodes
def chat_node(state: GraphState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Init Graph
def build_graph():

    memory = MemorySaver()
    graph_builder = StateGraph(GraphState)
    graph_builder.add_node("chat_node", chat_node)
    graph_builder.add_edge(START, "chat_node")

    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges(
    "chat_node",
    tools_condition,
    )
    graph_builder.add_edge("tools", "chat_node")

    graph = graph_builder.compile(checkpointer=memory)
    image_path = __file__.replace(".py", ".png")
    save_graph(image_path,graph)
    return graph

graph=build_graph()


def stream_graph_updates(role: str, content: str):
    config = {"configurable": {"thread_id": "1"}}
    events = graph.stream(
        {"messages": [{"role": role, "content": content}]},
        config,
        stream_mode="values",
    )
    for event in events:
        # print(event)
        if "messages" in event:
            event["messages"][-1].pretty_print()

        last_message=event["messages"][-1]
    return last_message

def main():

    for _ in range(0, 3):
        sleep(0.5)
        print(".")
    print("How can I help you? (type '/q' to exit)")
    stream_graph_updates("system",system_message)
    
    while True:
        try:
            user_input = input("> ")
            print("")
            if user_input.lower() in ["/q"]:
                break
            ai_message=stream_graph_updates("user",user_input)
            # print(ai_message.content)

            
        except Exception as e:
            print("An error occurred:", e)
            break

if __name__ == "__main__":
    main()