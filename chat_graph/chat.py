from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]
llm = init_chat_model(model_provider="openai", model="gpt-4.1")

    
def chat_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


graph_builder = StateGraph(State)

graph_builder.add_node("chat_node", chat_node)

graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)

graph = graph_builder.compile()

def main():
    query = input(">")
    
    result = graph.invoke({"messages": [{"role": "user", "content": query}]})
    print(result)
    
main()