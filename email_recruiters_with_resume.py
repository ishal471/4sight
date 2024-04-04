from simplegmail import Gmail
from simplegmail.query import construct_query
from dotenv import load_dotenv
import os
import openai
import re


# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Initialize Gmail
gmail = Gmail()


def extract_email(sender):
    return re.search(r'<([^<>]+)>', sender).group(1)

def send_attachment_email(msg,receiver_email='ishalabhishek93@gmail.com'):
    params = {
    "to": receiver_email,
    "sender": "ishalabhishek2000@gmail.com",
    "subject": "Please find my resume attached.",
    "msg_html": "Hi\n I am interested in the position \n Please find my resume my resume attached.\n" + msg,
    "attachments": ["C:/Users/Abhishek/Documents/career/current_full_time_resume/ishal's.pdf"],
    "signature": True  # use my account signature
    }
    message = gmail.send_message(**params)  # equivalent to send_message(to="you@youremail.com", sender=...)




def analyze_message_for_job_opportuinity(message):
    # Check if the plaintext body is available
    if message.plain is not None:
        # Define the prompt using the message body or snippet
        prompt = "Analyze below email and Is this a potential oppurtunity from an recruiter \n" + message.plain

        # Call OpenAI's chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )

        # Extract the completion text from the response
        completion_text = response["choices"][0]["message"]["content"]

        # Analyze the completion text from OpenAI
        if "yes" in completion_text.lower():
            return True
    return False





# Parameters for email to be searched
query_params = {
    "newer_than": (3, "month"),
    "older_than": (2, "month"),
    "label": 'INBOX'
}

# Retrieve messages
messages = gmail.get_messages(query=construct_query(query_params))

# Iterate through the messages
for message in messages:
    # Analyze each message for a job offer using OpenAI
    if analyze_message_for_job_opportuinity(message):
        print("Message with Message-ID {} has job_opportuinity.".format(message.headers.get('Message-ID')))
        # receiver_email = message.sender
        receiver_email = message.sender
        email = extract_email(receiver_email)
        msg = email + message.snippet
        send_attachment_email(msg,email) # use (msg) for testing
        # print(message.plain)