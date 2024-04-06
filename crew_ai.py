##############  Crewai test

# import os
# from crewai import Agent, Task, Crew, Process
# from crewai_tools import SerperDevTool
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# from crewai_tools import SerperDevTool
# os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
# search_tool = SerperDevTool()

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# # You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# # os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# # os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# # os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

# search_tool = SerperDevTool()

# # Define your agents with roles and goals
# researcher = Agent(
#   role='Senior Research Analyst',
#   goal='Uncover cutting-edge developments in AI and data science',
#   backstory="""You work at a leading tech think tank.
#   Your expertise lies in identifying emerging trends.
#   You have a knack for dissecting complex data and presenting actionable insights.""",
#   verbose=True,
#   allow_delegation=False,
#   tools=[search_tool]
#   # You can pass an optional llm attribute specifying what mode you wanna use.
#   # It can be a local model through Ollama / LM Studio or a remote
#   # model like OpenAI, Mistral, Antrophic or others (https://docs.crewai.com/how-to/LLM-Connections/)
#   #
#   # import os
#   # os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'
#   #
#   # OR
#   #
#   # from langchain_openai import ChatOpenAI
#   # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
# )
# writer = Agent(
#   role='Tech Content Strategist',
#   goal='Craft compelling content on tech advancements',
#   backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
#   You transform complex concepts into compelling narratives.""",
#   verbose=True,
#   allow_delegation=True
# )

# # Create tasks for your agents
# task1 = Task(
#   description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
#   Identify key trends, breakthrough technologies, and potential industry impacts.""",
#   expected_output="Full analysis report in bullet points",
#   agent=researcher
# )

# task2 = Task(
#   description="""Using the insights provided, develop an engaging blog
#   post that highlights the most significant AI advancements.
#   Your post should be informative yet accessible, catering to a tech-savvy audience.
#   Make it sound cool, avoid complex words so it doesn't sound like AI.""",
#   expected_output="Full blog post of at least 4 paragraphs",
#   agent=writer
# )

# # Instantiate your crew with a sequential process
# crew = Crew(
#   agents=[researcher, writer],
#   tasks=[task1, task2],
#   verbose=2, # You can set it to 1 or 2 to different logging levels
# )

# # Get your crew to work!
# result = crew.kickoff()

# print("######################")
# print(result)




##################################################################################################


# Final Code without code interpreter to generate code



# import os
# from crewai import Agent, Task, Crew, Process
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI

# # Load environment variables from .env file
# load_dotenv()

# # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# # Define your agents with roles and goals
# data_engineer = Agent(
#   role='Data Engineer',
#   goal=" Your script should be meticulously commented, explaining the significance of each section and the rationale behind your error handling strategies. This level of detail will not only assist in debugging and future development efforts but also enhance the overall readability and maintainability of your code",
#   backstory="""You work at a ForgeAI , Your expertise lies in MongoDB
#   You have a knack for dissecting complex data formats and writing code for databases""",
#   verbose=False,
#   allow_delegation=False,
#   llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# )


# # Create tasks for your agents
# task1 = Task(
#   description="""Act as a software engineer tasked with designing a Python script for managing database interactions with MongoDB. Your challenge involves crafting a detailed implementation encompassing two crucial functionalities:
# Connection Verification: Develop a function named check_connection that accepts a MongoDB connection string as an input. This function should attempt to establish a connection to the MongoDB server using the provided string. Utilize the MongoClient class from the pymongo library for this purpose. The function should return a boolean value: True if the connection is successfully established (indicating the MongoDB server is accessible and responsive), and False if the connection attempt fails due to a ConnectionFailure exception. This distinction is crucial for ensuring the reliability and availability of the database server before attempting any data operations.
# Query Execution: Implement another function called execute_query that is designed to perform an insert operation into a specified collection within a MongoDB database. This function should accept four parameters: the connection string, the database name, the collection name, and the query (in the form of a dictionary representing the document to be inserted). The function should attempt to connect to the specified database and collection, then execute an insert_one operation with the provided query. Proper error handling should be in place to catch any exceptions that might arise during this operation, ensuring the function's robustness in various scenarios.
# For both functions, include comprehensive docstrings detailing the purpose, arguments, and the return value of each function. This documentation is essential for future maintainability and ease of understanding by other developers or your future self.
# """,
#   expected_output="Python script should be meticulously commented, explaining the significance of each section and the rationale behind your error handling strategies. This level of detail will not only assist in debugging and future development efforts but also enhance the overall readability and maintainability of your code",
#   agent= data_engineer
# )


# # Instantiate your crew with a sequential process
# crew = Crew(
#   agents=[data_engineer],
#   tasks=[task1],
#   verbose=2, # You can set it to 1 or 2 to different logging levels
# )

# # Get your crew to work!
# result = crew.kickoff()

# print("######################")
# print(result)









##############################################################################################################


# CrewAI + Interpreter without user interfaace


# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os


# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)
# interpreter.auto_run = True
# interpreter.llm.model = "openai/gpt-3.5-turbo"

# class CLITool:
#     @tool("Executor")
#     def execute_cli_command(command: str):
#         """Create and Execute code using Open Interpreter."""
#         result = interpreter.chat(command)
#         return result

# # 2. Creating an Agent for CLI tasks
# cli_agent = Agent(
#     role='Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code.',
#     tools=[CLITool.execute_cli_command],
#     verbose=True,
#     llm=llm 
# )

# # 3. Defining a Task for CLI operations
# cli_task = Task(
#     description='Identify the OS and then empty my recycle bin',
#     expected_output='Recycle bin emptied successfully.',  # Adding expected output
#     agent=cli_agent,
#     tools=[CLITool.execute_cli_command]
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent],
#     tasks=[cli_task],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Run the Crew
# result = cli_crew.kickoff()
# print(result)





#################################################################


# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os


# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo",api_key = api_key)
# interpreter.auto_run = True
# interpreter.llm.model = "openai/gpt-3.5-turbo"

# class CLITool:
#     @tool("Executor")
#     def execute_cli_command(command: str):
#         """Create and Execute code using Open Interpreter."""
#         result = interpreter.chat(command)
#         return result

# # 2. Creating an Agent for CLI tasks
# cli_agent = Agent(
#     role='Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code.',
#     tools=[CLITool.execute_cli_command],
#     verbose=True,
#     llm=llm 
# )

# # 3. Defining a Task for CLI operations
# cli_task = Task(
#     description='Identify the OS and then empty my recycle bin',
#     agent=cli_agent,
#     tools=[CLITool.execute_cli_command]
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent],
#     tasks=[cli_task],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Run the Crew

# import gradio as gr

# def cli_interface(command):
#     cli_task.description = command  
#     result = cli_crew.kickoff()
#     return result

# iface = gr.Interface(
#     fn=cli_interface, 
#     inputs=gr.Textbox(lines=2, placeholder="What action to take?"), 
#     outputs="text",
#     title="CLI Command Executor",
#     description="Execute CLI commands via a natural language interface."
# )

# iface.launch()


####################################################################################################################################

# # CrewAI + Interpreter with Gradio Interface and code generation

# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os


# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)  
# interpreter.auto_run = True
# interpreter.llm.model = "openai/gpt-3.5-turbo"

# class CLITool:
#     @tool("Executor")
#     def execute_cli_command(command: str):
#         """Create and Execute code using Open Interpreter."""
#         print("###########################################################","  Entered Interpreter")
#         result = interpreter.chat(command)
#         return result

# # 2. Creating an Agent for CLI tasks
# cli_agent = Agent(
#     role='Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code.',
#     tools=[CLITool.execute_cli_command],
#     verbose=True,
#     llm=llm 
# )

# # 3. Defining a Task for CLI operations
# cli_task = Task(
#     description='This will be replced by user prompt',
#     expected_output='Execute the Code',  # Adding expected output
#     agent=cli_agent,
#     tools=[CLITool.execute_cli_command]
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent],
#     tasks=[cli_task],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Define CLI interface function
# def cli_interface(command):
#     cli_task.description = command  
#     result = cli_crew.kickoff()
#     return result

# # 6. Define and launch Gradio interface
# import gradio as gr

# iface = gr.Interface(
#     fn=cli_interface, 
#     inputs=gr.Textbox(lines=2, placeholder="What action to take?"), 
#     outputs="text",
#     title="CLI Command Executor",
#     description="Execute CLI commands via a natural language interface."
# )

# iface.launch()




#########################################################################




# # CrewAI + Interpreter with Gradio Interface and code generation

# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os


# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)  
# interpreter.auto_run = True
# # interpreter.llm.model = "openai/gpt-3.5-turbo"

# class CLITool:
#     @tool("Executor")
#     def execute_cli_command(command: str):
#         """Create and Execute code using Open Interpreter."""
#         print("###########################################################","  Entered Interpreter")
#         result = interpreter.chat(command)
#         return result

# # 2. Creating an Agent for CLI tasks
# cli_agent = Agent(
#     role='Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code.',
#     tools=[CLITool.execute_cli_command],
#     verbose=True,
#     llm=llm 
# )

# # 3. Defining a Task for CLI operations
# cli_task = Task(
#     description='This will be replced by user prompt',
#     expected_output='Execute the Code',  # Adding expected output
#     agent=cli_agent,
#     tools=[CLITool.execute_cli_command]
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent],
#     tasks=[cli_task],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Define CLI interface function
# def cli_interface(command):
#     cli_task.description = command  
#     result = cli_crew.kickoff()
#     return result

# # 6. Define and launch Gradio interface
# import gradio as gr

# iface = gr.Interface(
#     fn=cli_interface, 
#     inputs=gr.Textbox(lines=2, placeholder="What action to take?"), 
#     outputs="text",
#     title="CLI Command Executor",
#     description="Execute CLI commands via a natural language interface."
# )

# iface.launch()



#############################################################################


# # CrewAI + Interpreter with Gradio Interface and code generation

# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os


# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)  
# interpreter.auto_run = True
# # interpreter.llm.model = "openai/gpt-3.5-turbo"

# class CLITool:
#     @tool("Executor")
#     def execute_cli_command(command: str):
#         """Create and Execute code using Open Interpreter."""
#         print("###########################################################","  Entered Interpreter")
#         result = interpreter.chat(command)
#         return result

# # 2. Creating an Agent for CLI tasks
# cli_agent = Agent(
#     role='Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code.',
#     tools=[CLITool.execute_cli_command],
#     verbose=True,
#     llm=llm 
# )



# # 3. Defining a Task for CLI operations
# cli_task = Task(
#     description='This will be replced by user prompt',
#     expected_output='Execute the Code',  # Adding expected output
#     agent=cli_agent,
#     tools=[CLITool.execute_cli_command]
# )

# cli_task2 = Task(
#     description='This will be replced by user prompt',
#     expected_output='Execute the Code  using tools',  # Adding expected output
#     agent=cli_agent,
#     tools=[CLITool.execute_cli_command]
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent],
#     tasks=[cli_task,cli_task2],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Define CLI interface function
# def cli_interface(command):
#     cli_task.description = command  
#     result = cli_crew.kickoff()
#     return result

# # 6. Define and launch Gradio interface
# import gradio as gr

# iface = gr.Interface(
#     fn=cli_interface, 
#     inputs=gr.Textbox(lines=2, placeholder="What action to take?"), 
#     outputs="text",
#     title="CLI Command Executor",
#     description="Execute CLI commands via a natural language interface."
# )

# iface.launch()



######################################################################



# CrewAI + Interpreter with Gradio Interface and code generation with 2 agents looping itself

# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os


# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)  
# interpreter.auto_run = True
# # interpreter.llm.model = "openai/gpt-3.5-turbo"

# class CLITool:
#     @tool("Executor")
#     def execute_cli_command(command: str):
#         """Create and Execute code using Open Interpreter."""
#         print("###########################################################","  Entered Interpreter")
#         result = interpreter.chat(command)
#         return result

# # 2. Creating an Agent for CLI tasks
# cli_agent1 = Agent(
#     role='Software Engineer',
#     goal='Can Write code in various languages',
#     backstory='Expert in creating  code.',
#     tools=[CLITool.execute_cli_command],
#     verbose=True,
#     llm=llm 
# )


# cli_agent2 = Agent(
#     role=' SR Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code. Rectify if errors',
#     tools=[CLITool.execute_cli_command],
#     verbose=True,
#     llm=llm 
# )



# # 3. Defining a Task for CLI operations
# cli_task1 = Task(
#     description='Write code based on user request and pass it to next task',
#     expected_output='Give code to next agent to be executed',  # Adding expected output
#     agent=cli_agent1,
#     tools=[CLITool.execute_cli_command]
# )

# cli_task2 = Task(
#     description='execute code based on user request an output based on his request',
#     expected_output='Execute the Code  using tools rectify if any errors , output based on user request',  # Adding expected output
#     agent=cli_agent2,
#     tools=[CLITool.execute_cli_command]
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent1,cli_agent2],
#     tasks=[cli_task1,cli_task2],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Define CLI interface function
# def cli_interface(command):
#     cli_task1.description = command  
#     result = cli_crew.kickoff()
#     return result

# # 6. Define and launch Gradio interface
# import gradio as gr

# iface = gr.Interface(
#     fn=cli_interface, 
#     inputs=gr.Textbox(lines=2, placeholder="What action to take?"), 
#     outputs="text",
#     title="CLI Command Executor",
#     description="Execute CLI commands via a natural language interface."
# )

# iface.launch()



###################################################################################################


# # CrewAI + Interpreter with Gradio Interface and code generation still looping

# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os
# from crewai_tools import SerperDevTool



# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")
# os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)  
# interpreter.auto_run = True
# search_tool = SerperDevTool()
# interpreter.llm.model = "openai/gpt-3.5-turbo"

# class CLITool:
#     @tool("Executor")
#     def execute_cli_command(command: str):
#         """Create and Execute code using Open Interpreter."""
#         print("###########################################################","  Entered Interpreter")
#         result = interpreter.chat(command)
#         return result

# # 2. Creating an Agent for CLI tasks
# cli_agent = Agent(
#     role='Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code.',
#     tools=[CLITool.execute_cli_command,search_tool],
#     verbose=True,
#     llm=llm 
# )



# # 3. Defining a Task for CLI operations
# cli_task = Task(
#     description='This will be replced by user prompt',
#     expected_output='Generate code',  # Adding expected output
#     agent=cli_agent,
#     # tools=[search_tool]
# )

# cli_task2 = Task(
#     description='From code generated from previous task execute the code ',
#     expected_output='Execute the Code  using tools for exectuion and debuging',  # Adding expected output
#     agent=cli_agent,
#     tools=[CLITool.execute_cli_command,search_tool]
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent],
#     tasks=[cli_task,cli_task2],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Define CLI interface function
# def cli_interface(command):
#     cli_task.description = command  
#     result = cli_crew.kickoff()
#     return result

# # 6. Define and launch Gradio interface
# import gradio as gr

# iface = gr.Interface(
#     fn=cli_interface, 
#     inputs=gr.Textbox(lines=2, placeholder="What action to take?"), 
#     outputs="text",
#     title="CLI Command Executor",
#     description="Execute CLI commands via a natural language interface."
# )

# iface.launch()


#####################################################################################


# #  CrewAI  with Gradio Interface and code generation no execution

# from crewai import Agent, Task, Crew, Process
# from interpreter import interpreter
# from langchain.tools import tool
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os
# from crewai_tools import SerperDevTool



# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI API with your API key
# api_key = os.getenv("OPENAI_API_KEY")
# os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# # 1. Configuration and Tools
# llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)  
# # interpreter.auto_run = True
# search_tool = SerperDevTool()
# # interpreter.llm.model = "openai/gpt-3.5-turbo"

# # class CLITool:
# #     @tool("Executor")
# #     def execute_cli_command(command: str):
# #         """Create and Execute code using Open Interpreter."""
# #         result = interpreter.chat(command)
# #         generated_code =result.choices[0].message.content
# #         # prompt_tokens = result['usage']['prompt_tokens']
# #         # completion_tokens = result['usage']['completion_tokens']
# #         # total_tokens = result['usage']['total_tokens']
# #         # with open("function.py", "w") as file:
# #         #     file.write(generated_code)
# #         return generated_code

# # 2. Creating an Agent for CLI tasks
# cli_agent1 = Agent(
#     role='Software Engineer Manager',
#     goal='Generate report and a plan how the code can be used to generate code, Always use  Tools. Ability to researching the question and giving the detailed report to software engineer',
#     backstory='Expert in researching the task and giving the detailed report to software engineer',
#     tools=[search_tool],
#     verbose=True,
#     llm=llm 
# )

# cli_agent2 = Agent(
#     role='Software Engineer',
#     goal='Always use Executor Tool. Ability to perform CLI operations, write programs and execute using Exector Tool',
#     backstory='Expert in command line operations, creating and executing code.',
#     verbose=True,
#     llm=llm 
# )


# # 3. Defining a Task for CLI operations
# cli_task1 = Task(
#     description='This will be replced by user prompt',
#     expected_output='Generate report and a plan how the code can be used to generate code',  # Adding expected output
#     agent=cli_agent1,
#     tools=[search_tool]
# )

# cli_task2 = Task(
#     description='From report generated from previous task generate the script ',
#     expected_output='Execute the generated Code using tools for exectuion if no errors return the well commented code',  # Adding expected output
#     agent=cli_agent2
# )

# # 4. Creating a Crew with CLI focus
# cli_crew = Crew(
#     agents=[cli_agent1,cli_agent2],
#     tasks=[cli_task1,cli_task2],
#     process=Process.sequential,
#     manager_llm=llm
# )

# # 5. Define CLI interface function
# def cli_interface(command):
#     cli_task1.description = command  
#     result = cli_crew.kickoff()
#     return result

# # 6. Define and launch Gradio interface
# import gradio as gr

# iface = gr.Interface(
#     fn=cli_interface, 
#     inputs=gr.Textbox(lines=2, placeholder="What action to take?"), 
#     outputs="text",
#     title="CLI Command Executor",
#     description="Execute CLI commands via a natural language interface."
# )

# iface.launch()




#######################################################################
