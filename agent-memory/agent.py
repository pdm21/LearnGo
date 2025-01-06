from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from agent.utils.nodes import call_model, should_continue, tool_node
from agent.utils.state import AgentState
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
import json


# Define the config
class GraphConfig(TypedDict):
    # must be openai (have not added support for other models)
    model_name: Literal["openai"]

# Define a new graph
workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue, 
    {
        "continue": "action",
        "end": END,
    },
)
workflow.add_edge("action", "agent")

graph = workflow.compile()

# Pretty print each message with labels
inputs = {"messages": [HumanMessage(content="what is the weather in the capital of the state that had the team which won the superbowl in 2018?")]}
results = graph.invoke(inputs)

# Extract messages from results
messages = results.get('messages', [])

# Pretty print function
def org_output(messages):
    for msg in messages:
        if isinstance(msg, HumanMessage):
            print("\n[Human]:", msg.content)
        elif msg.additional_kwargs.get("tool_calls"):
            print("\n[AI - Tool Call]:")
            print(json.dumps(msg.additional_kwargs, indent=2)) 
        elif isinstance(msg, ToolMessage):
            print("\n[Tool Response]:")
            print(json.dumps(msg.artifact, indent=2))  
        elif isinstance(msg, AIMessage):
            print("\n[AI]:", msg.content)

# Call pretty print
org_output(messages)
