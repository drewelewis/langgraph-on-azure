from typing import Annotated
import uuid

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI
from IPython.display import Image, display
import random
import string

llm = ChatOpenAI(model="gpt-35-turbo")

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