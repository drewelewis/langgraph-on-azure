import random
from typing import Annotated, Literal, TypedDict
from langgraph.graph import Graph,StateGraph, START, END
from langgraph.graph.message import add_messages
from helpers import save_graph


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

def weather(str):
  return "Hi! Well.. I have no idea... But... "


def rainy_weather(str):
  return str + " Its going to rain today. Carry an umbrella."

def sunny_weather(str):
  return str + " Its going to be sunny today. Wear sunscreen."


def forecast_weather(str)->Literal["rainy", "sunny"]:
  if random.random() < 0.5:
    return "rainy"
  else:
    return "sunny"
  
graph_builder = Graph()

graph_builder.add_node("weather", weather)

graph_builder.add_node("rainy", rainy_weather)
graph_builder.add_node("sunny", sunny_weather)

graph_builder.add_edge(START, "weather")
graph_builder.add_conditional_edges("weather", forecast_weather)
graph_builder.add_edge("rainy", END)
graph_builder.add_edge("sunny", END)

graph = graph_builder.compile()

save_graph("weather.png",graph)

# ouput=graph.invoke(state["messages"])
print(graph.invoke('Hi! What does the weather look like? '))