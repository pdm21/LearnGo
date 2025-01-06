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

# Agent 1: chatbot 
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return messages
    # return {"messages": [llm.invoke(state["messages"])]}

# Agent 2: 
# take content from Agent 1, summarize it and 
# identify key points (for potential DB store)
def summarize_content(state: State):
    print()

# Agent 3: fetch current DB info
# Agent 4: compare cur_DB with potential_new content

# need to provide DB access for chatbot agent (for during conversation)

# Defining the graph
workflow.set_entry_point("chatbot")
workflow.add_node("chatbot", chatbot)
workflow.add_edge("chatbot", END)
graph = workflow.compile()

conversation_history = {}
id = 0

def stream_graph_updates(user_input: str):
    # id += 1

    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
            maintain_memory(conversation_history, id, value["messages"][-1].content, user_input)


def maintain_memory(conversation_history, id, AIMessage, HumanMessage):
    conversation_history[id] = [f"AIMessage: {AIMessage}" + f"HumanMessage: {HumanMessage}"]

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