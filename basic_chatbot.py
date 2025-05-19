import os
from typing import Annotated
import uuid

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from IPython.display import Image, display
import random
import string
from langchain_community.tools.tavily_search import TavilySearchResults
from helpers import save_graph

from dotenv import load_dotenv
load_dotenv(override=True)


llm  = AzureChatOpenAI(
    azure_endpoint=os.getenv('OPENAI_API_ENDPOINT'),
    azure_deployment=os.getenv('OPENAI_API_MODEL_DEPLOYMENT_NAME'),
    api_version=os.getenv('OPENAI_API_VERSION'),
    temperature=0,
    streaming=True
)
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

image_path = __file__.replace(".py", ".png")
save_graph(image_path,graph)


def main():
    run()

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

def run():
    while True:
        try:
            print("")
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input)
        except Exception as e:
            print("An error occurred:", e)
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break


if __name__ == "__main__":
    main()