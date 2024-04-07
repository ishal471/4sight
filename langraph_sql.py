import psycopg2
import os
import json
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import Annotated, Sequence, TypedDict
import gradio as gr
import functools
import operator

# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangGraph Research Agents"

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
# Initialize model
llm = ChatOpenAI(api_key=api_key)

# Get database connection details from environment variables
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Define custom tools
@tool("execute_sql_command")
def execute_sql_command(command: str):
    """Execute SQL commands on a PostgreSQL database."""
    try:
        # Establish a connection
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

        # Create a cursor
        cursor = conn.cursor()

        # Execute the SQL command
        cursor.execute(command)

        # Commit the changes (if it's a DML statement)
        conn.commit()

        # Fetch and return the results (if it's a SELECT statement)
        if command.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while executing SQL command:", error)
        return error

tools = [execute_sql_command]

# Helper function for creating agents
def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

# Define agent nodes
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

# Create Agent Supervisor
members = ["postgress_agent"]
system_prompt = (
    "As a supervisor, your role is to oversee a dialogue between these"
    " workers: {members}. Based on the user's request,"
    " determine which worker should take the next action. Each worker is responsible for"
    " executing a specific task and reporting back their findings and progress. Once all tasks are complete,"
    " indicate with 'FINISH'."
)

options = ["FINISH"] + members
function_def = {
    "name": "route",
    "description": "Select the next role.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {"next": {"title": "Next", "anyOf": [{"enum": options}] }},
        "required": ["next"],
    },
}

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Given the conversation above, who should act next? Or should we FINISH? Select one of: {options}"),
]).partial(options=str(options), members=", ".join(members))

supervisor_chain = (prompt | llm.bind_functions(functions=[function_def], function_call="route") | JsonOutputFunctionsParser())

# Define the Agent State and Graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

postgress_agent = create_agent(llm, tools, "You are a SQL database admin, capable of performing search queries and CRUD operations.")
postgress_node = functools.partial(agent_node, agent=postgress_agent, name="postgress_agent")

workflow = StateGraph(AgentState)
workflow.add_node("postgress_agent", postgress_node)
workflow.add_node("supervisor", supervisor_chain)

# Define edges
for member in members:
    workflow.add_edge(member, "supervisor")

conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
workflow.set_entry_point("supervisor")

graph = workflow.compile()

# Run the graph
def run_graph(input_message):
    response = graph.invoke({
        "messages": [HumanMessage(content=input_message)]
    })
    output_messages = response['messages']
    output_text = "\n\n".join([f"{msg.name}: {msg.content}" for msg in output_messages])
    return output_text

iface = gr.Interface(
    fn=run_graph,
    inputs=gr.Textbox(lines=2, placeholder="Enter your SQL Task or Query here..."),
    outputs="text",
    title="SQL Command Executor",
    description="Execute SQL commands or tasks on a PostgreSQL database."
)

iface.launch()