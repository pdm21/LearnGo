from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from agent.utils.nodes import call_model, should_continue, tool_node
from agent.utils.state import AgentState

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