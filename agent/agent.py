from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition 
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from config.configs import OPENAI_API_KEY, GROQ_API_KEY, NEO4J_CONNECTION_URL, NEO4J_USER, NEO4J_API_KEY

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from tools.retrieve_detail_obat import retrieve_detail_obat_tool
from states.state import GraphState

model_groq = ChatGroq(model="llama-3.1-70b-versatile",groq_api_key = GROQ_API_KEY)
model_oai = ChatOpenAI(model="gpt-4o-mini",openai_api_key = OPENAI_API_KEY)

tools = [retrieve_detail_obat_tool]
llm_with_tools = model_oai.bind_tools(tools)

def reasoner(state: GraphState):
    query = state["query"]
    messages = state["messages"]
    system_message = SystemMessage(content=
                            """You're a helpful assistant designed for medical question answering system. 
                            You should think step by step, if there's multiple question, you must decompose the initial question. 
                            There's one tool that you must use in order to answer the question, don't try to answer it by yourself"""
                            )
    human_message = HumanMessage(content=query)
    messages.append(human_message)
    result = [llm_with_tools.invoke([system_message] + messages)]
    return {"messages": result}


# Graph
workflow = StateGraph(GraphState)

# Add Nodes
workflow.add_node("reasoner", reasoner)
workflow.add_node("tools", ToolNode(tools)) 

# Add Edges
workflow.add_edge(START, "reasoner")
workflow.add_conditional_edges("reasoner",tools_condition)
workflow.add_edge("tools", "reasoner")

react_graph = workflow.compile()
