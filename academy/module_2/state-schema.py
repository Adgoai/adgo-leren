# In the video worden meerdere optie getoond, ik heb alleen Pydantic opgenomen

from pydantic import BaseModel, field_validator, ValidationError
from langgraph.graph import StateGraph, START, END
import random
from typing import Literal

class PydanticState(BaseModel):
    name: str
    mood: str # "happy" or "sad"

    @field_validator('mood')
    @classmethod
    def validate_mood(cls, value):
        # Ensure the mood is either "happy" or "sad"
        if value not in ["happy", "sad"]:
            raise ValueError("Each mood must be either 'happy' or 'sad'")
        return value

def part1():
    try:
        state = PydanticState(name="John Doe", mood="mad")
    except ValidationError as e:
        print("Validation Error:", e)

def node_1(state):
    print("---Node 1---")
    return {"name": state.name + " is ... "}

def node_2(state):
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(state):
    print("---Node 3---")
    return {"mood": "sad"}

def decide_mood(state) -> Literal["node_2", "node_3"]:

    # Here, let's just do a 50 / 50 split between nodes 2, 3
    if random.random() < 0.5:
        # 50% of the time, we return Node 2
        return "node_2"

    # 50% of the time, we return Node 3
    return "node_3"


# Build graph
builder = StateGraph(PydanticState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

print(graph.get_graph().draw_ascii())
graph.get_graph().draw_mermaid_png(output_file_path="state-schema.png")


if __name__ == "__main__":
   # part1()
    try:
       response = graph.invoke(PydanticState(name="Lance", mood="sad"))
       print("---------------------------------------------")
       print(response)
       response = graph.invoke(PydanticState(name="Lance", mood="crazy"))
       print("---------------------------------------------")
       print(response)
    except ValidationError as e:
        print("Validation Error:", e)
