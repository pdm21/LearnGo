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

def main():
    try:
        print("Welcome to the Agent conversation!")
        print("Type 'exit', 'quit', or 'q' to end the conversation.")

        while True:
            # Get input from the user
            user_input = input("You: ").strip()

            # Exit condition
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            # Run the agent with the user's input
            inputs = {"messages": [HumanMessage(content=user_input)]}  # HumanMessage object
            results = graph.invoke(inputs)

            # Check if `results` contains the expected data
            if isinstance(results, dict) and 'messages' in results:
                messages = results['messages']  # Extract messages
                for message in messages:
                    if hasattr(message, 'content') and isinstance(message, AIMessage):
                        print(f"Assistant: {message.content}")
            else:
                print("Assistant: I couldn't process the response.")
    
    except Exception as e:
        print("There was an error in the process. More info:", e)

if __name__ == '__main__':
    main()


# # # # # # # # # # # # # # # # # # # # # #





# # Pretty print each message with labels
# inputs = {"messages": [HumanMessage(content="what is the weather in the capital of the state that had the team which won the superbowl in 2018?")]}
# results = graph.invoke(inputs)

# # Extract messages from results
# messages = results.get('messages', [])

# # Pretty print function
# def org_output(messages):
#     for msg in messages:
#         if isinstance(msg, HumanMessage):
#             print("\n[Human]:", msg.content)
#         elif msg.additional_kwargs.get("tool_calls"):
#             print("\n[AI - Tool Call]:")
#             print(json.dumps(msg.additional_kwargs, indent=2)) 
#         elif isinstance(msg, ToolMessage):
#             print("\n[Tool Response]:")
#             print(json.dumps(msg.artifact, indent=2))  
#         elif isinstance(msg, AIMessage):
#             print("\n[AI]:", msg.content)

# # Call pretty print
# org_output(messages)