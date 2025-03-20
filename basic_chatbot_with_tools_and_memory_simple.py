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


from langchain_openai import AzureChatOpenAI
from IPython.display import Image, display
from langchain_community.tools.tavily_search import TavilySearchResults

from helpers import save_graph
from dotenv import load_dotenv
load_dotenv(override=True)

class GraphState(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

llm = AzureChatOpenAI(
    azure_deployment=os.getenv('OPENAI_API_MODEL_DEPLOYMENT_NAME'),
    api_version=os.getenv('OPENAI_API_VERSION')
)
# Define Nodes
def chat_node(state: GraphState):
    return {"messages": [llm.invoke(state["messages"])]}

# Init Graph
def build_graph():
    memory = MemorySaver()
    graph_builder = StateGraph(GraphState)
    graph_builder.add_node("chat_node", chat_node)
    graph_builder.set_entry_point("chat_node")
    graph = graph_builder.compile(checkpointer=memory)
    return graph
graph=build_graph()

def main():
    run()

def stream_graph_updates(user_input: str):
    config = {"configurable": {"thread_id": "1"}}
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    for event in events:
        last_message=event["messages"][-1]
    return last_message

def run():
    for _ in range(0, 3):
        sleep(0.5)
        print(".")
    print("How can I help you? (type '/q' to exit)")

    while True:
        try:
            user_input = input("> ")
            print("")
            if user_input.lower() in ["/q"]:
                break
            ai_message=stream_graph_updates(user_input)
            print(ai_message.content)
        except Exception as e:
            print("An error occurred:", e)
            break

if __name__ == "__main__":
    main()