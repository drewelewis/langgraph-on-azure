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

from dotenv import load_dotenv
load_dotenv(override=True)


os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('OPENAI_API_BASE')
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = AzureChatOpenAI(
    azure_deployment=os.getenv('OPENAI_API_MODEL_DEPLOYMENT_NAME'),
    api_version=os.getenv('OPENAI_API_VERSION')
)

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

def save_graph(graph):
    try:
        # Generate a random filename
        import os

        # Ensure the images directory exists
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        
        # Generate a random filename
        random_filename = os.path.join(images_dir, str(uuid.uuid4()) + ".png")
        
        # Save the image as a file
        with open(random_filename, "wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())
   
    except Exception:
        # This requires some extra dependencies and is optional
        pass

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

# save_graph(graph)

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