import psycopg2
import openai
from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()


# Set environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Crew AI Agents"


# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get database connection details from environment variables
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# 1. Configuration and Tools
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai.api_key)

class PostgreSQLTool:
    @tool("PostgreSQL Executor")
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

# 2. Creating an Agent for SQL tasks
sql_agent = Agent(
    role='Database Engineer',
    goal='Execute SQL commands on a PostgreSQL database using the PostgreSQL Executor Tool',
    backstory='Expert in writing and executing SQL commands on PostgreSQL databases.',
    tools=[PostgreSQLTool.execute_sql_command],
    verbose=True,
    llm=llm
)

# 3. Defining a Task for SQL operations
sql_task = Task(
    description='This will be replaced by user prompt',
    expected_output='Execute SQL commands on the PostgreSQL database using the PostgreSQL Executor Tool',
    agent=sql_agent,
    tools=[PostgreSQLTool.execute_sql_command]
)

# 4. Creating a Crew with SQL focus
sql_crew = Crew(
    agents=[sql_agent],
    tasks=[sql_task],
    process=Process.sequential,
    manager_llm=llm
)

# 5. Define SQL interface function
def sql_interface(command):
    sql_task.description = command
    result = sql_crew.kickoff()
    return result

# 6. Define and launch Gradio interface
import gradio as gr

iface = gr.Interface(
    fn=sql_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter SQL command or task"),
    outputs="text",
    title="SQL Command Executor",
    description="Execute SQL commands or tasks on a PostgreSQL database via a natural language interface."
)

iface.launch()
