from simplegmail import Gmail
from simplegmail.query import construct_query
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to analyze a message for an offer using OpenAI
def analyze_message_for_offer(message):
    # Check if the plaintext body is available
    if message.plain is not None:
        # Define the prompt using the message body or snippet
        prompt = "Analyze below email and Is the recipient of this email receiving a job offer letter from the company? \n" + message.plain

        # Call OpenAI's chat completion endpoint
        response = openai.ChatCompletion.create(
            model=  "gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )

        # Extract the completion text from the response
        completion_text = response["choices"][0]["message"]["content"]

        # Analyze the completion text from OpenAI
        if "yes" in completion_text.lower():
            return True
    return False

# Initialize Gmail
gmail = Gmail()

# Get all labels
labels = gmail.list_labels()

# Check if the label "job_offers" exists
job_offers_label = None
for label in labels:
    if label.name == "job_offers":
        job_offers_label = label
        break

# If the label doesn't exist, create it
if job_offers_label is None:
    job_offers_label = gmail.create_label("job_offers")

query_params = {
    "newer_than": (2, "month"),
    "older_than": (1, "month"),
    "label": 'INBOX'
}

# Retrieve messages
messages = gmail.get_messages(query=construct_query(query_params))

msg_cnt = 0
offer_cnt = 0
# Iterate through the messages
for message in messages:
    msg_cnt = msg_cnt +1
    # Analyze each message for a job offer using OpenAI
    if analyze_message_for_offer(message):
        # Move the message to the "job_offers" folder
        offer_cnt = offer_cnt +1
        message.add_label(job_offers_label)
        print("Message with Message-ID {} moved to job_offers folder.".format(message.headers.get('Message-ID')))
        # print(message.plain)
        print("Offer number: ",offer_cnt)