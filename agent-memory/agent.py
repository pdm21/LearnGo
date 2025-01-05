from dotenv import load_dotenv
load_dotenv()
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

# # # # # # # # # # # # # # # # # # # # # # # # # # # 
class State(TypedDict):
    messages: Annotated[list, add_messages]

workflow = StateGraph(State)
llm = ChatOpenAI(temperature=0, streaming=True)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

workflow.set_entry_point("chatbot")
workflow.add_node("chatbot", chatbot)
workflow.add_edge("chatbot", END)
graph = workflow.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
