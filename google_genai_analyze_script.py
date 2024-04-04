import re
from simplegmail import Gmail
from simplegmail.query import construct_query
from dotenv import load_dotenv
import os
import google.generativeai as palm  # Import palm module

# Load environment variables from .env file
load_dotenv()

# Set your API key via google data studio
api_key = os.getenv("PALM_API_KEY")

# Configure the PALM module with your API key
palm.configure(api_key=api_key)

# Initialize Gmail
gmail = Gmail()

def extract_email(sender):
    return re.search(r'<([^<>]+)>', sender).group(1)

def send_attachment_email(email, msg, receiver_email='ishalabhishek93@gmail.com'):
    email_body = (
        "<p>Hi,</p>"
        "<p>I am interested in the position.</p>"
        "<p>Please find my resume attached.</p>"
        "<p>" + email + "</p>"
        "<p>" + msg + "</p>"
    )
    params = {
        "to": receiver_email,
        "sender": "ishalabhishek2000@gmail.com",
        "subject": "Please find my resume attached.",
        "msg_html": email_body,
        "attachments": ["C:/Users/Abhishek/Documents/career/current_full_time_resume/ishal's.pdf"],
        "signature": True  # use my account signature
    }
    message = gmail.send_message(**params)

def parse_palm_response(response):
    parts = response.split()
    offer_detected = False
    opportunity_detected = False

    for i in range(len(parts)):
        if parts[i] == "offer_detected":
            offer_detected = parts[i + 1] == "True"
        elif parts[i] == "opportunity_detected":
            opportunity_detected = parts[i + 1] == "True"

    return offer_detected, opportunity_detected

def analyze_message(message):
    if message.plain is not None:
        # print("This is the message ","*********************************************************************",message.plain)
        prompt = (
            "Analyze below email:\n"
            "1. Is the recipient receiving a job offer letter from the company? True or False\n"
            "2. Is this a potential opportunity from a recruiter? True or False\n"
            "answer in 1. format offer_detected True or False, 2. format opportunity_detected True or False \n"
            + message.plain
        )

        # Call PALM's generate_text method
        completion = palm.generate_text(
            model='models/text-bison-001',  # Replace 'model' with the appropriate model
            prompt=prompt,
            temperature=0,
            max_output_tokens=30,
        )

        completion_text = completion.result  # Adjust to extract the completion text from the completion object
        # print("This is the completion text ","###########################################################################################",completion_text)
        if completion_text is not None:
            offer_detected, opportunity_detected = parse_palm_response(completion_text)
            return offer_detected, opportunity_detected
        else:
            return False, False
    else:
        return False, False

# Retrieve messages
query_params = {
    "newer_than": (11, "month"),
    "older_than": (10, "month"),
    "label": 'INBOX'
}
messages = gmail.get_messages(query=construct_query(query_params))

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

# Iterate through the messages
msg_cnt = 0
offer_cnt = 0
for message in messages:
    msg_cnt += 1
    # print("This is message number:", msg_cnt)
    offer_detected, opportunity_detected = analyze_message(message)
    # print("Offer Detected: {}, Opportunity Detected: {}".format(offer_detected, opportunity_detected))
    if offer_detected:
        offer_cnt += 1
        message.add_label(job_offers_label)
        print("Offer found in message with Message-ID {} and moved to job_offers folder.".format(message.headers.get('Message-ID')))
        print("Offer number:", offer_cnt)
    if opportunity_detected:
        print("Message with Message-ID {} has a job opportunity.".format(message.headers.get('Message-ID')))
        receiver_email = message.sender
        email = extract_email(receiver_email)
        msg = message.snippet
        send_attachment_email(email,msg)

print("Total messages analyzed:", msg_cnt)
print("Total offers found:", offer_cnt)
