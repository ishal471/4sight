Instructions:

1. .env file should be setup in root directory based on .env_sample
2. Download client_secret.josn after setting up gmail api via google cloud (OAUTH 2.0)
3. After initializing the Gmail class for the first time, it creates a gmail_token.json
4. pip install dependecies based on requirments.txt

About the files

Analyze script has both email recruiters with resume, move email to folder scripts combined in 1 api call.
There are 3 Analyze script files one for each llm (openai,anthropic,google)
And one more Analyze script to integrate langsmith(trace runs)

crew_ai.py has task scripts
