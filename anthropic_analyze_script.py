# ################################################## Anthropic_analyze script

# from simplegmail import Gmail
# from simplegmail.query import construct_query
# from dotenv import load_dotenv
# import os
# import anthropic
# import re

# # Load environment variables from .env file
# load_dotenv()

# # Initialize  your API key
# api_key = os.getenv("x-api-key")

# # Initialize Gmail
# gmail = Gmail()

# def extract_email(sender):
#     return re.search(r'<([^<>]+)>', sender).group(1)


# def send_attachment_email(email,msg,receiver_email='ishalabhishek93@gmail.com'):
#     email_body = (
#         "<p>Hi,</p>"
#         "<p>I am interested in the position.</p>"
#         "<p>Please find my resume attached.</p>"
#         "<p>" + email + "</p>"
#         "<p>" + msg + "</p>"
#     )
#     params = {
#     "to": receiver_email,
#     "sender": "ishalabhishek2000@gmail.com",
#     "subject": "Please find my resume attached.",
#     "msg_html": email_body,
#     "attachments": ["C:/Users/Abhishek/Documents/career/current_full_time_resume/ishal's.pdf"],
#     "signature": True  # use my account signature
#     }
#     message = gmail.send_message(**params)  # equivalent to send_message(to="you@youremail.com", sender=...)

# def parse_gpt_response(response):
#     parts = response.split()
#     offer_detected = False
#     opportunity_detected = False

#     for i in range(len(parts)):
#         if parts[i] == "offer_detected":
#             offer_detected = parts[i + 1] == "True"
#         elif parts[i] == "opportunity_detected":
#             opportunity_detected = parts[i + 1] == "True"
#     return offer_detected, opportunity_detected


# def analyze_message(message):
#     # ln = len(message.plain)
#     if message.plain is not None:
#         # Define the prompt to analyze both job offer and potential opportunity
#         prompt = (
#             "Analyze below email:\n"
#             "1. Is the recipient receiving a job offer letter from the company? True or False\n"
#             "2. Is this a potential opportunity from a recruiter? True or False\n"
#             "answer in 1. format offer_detected True or False, 2. format opportunity_detected True or False \n"
#             + message.plain
#         )

        
#         response = anthropic.Anthropic(api_key = api_key ).messages.create(
#         model="claude-2.1",
#         max_tokens=1024,
#         messages=[
#         {"role": "user", "content": prompt}
#         ]
#         )
#         # print(response)
#         completion_text = response.content[0].text
#         offer_detected, opportunity_detected = parse_gpt_response(completion_text)
        
#         return offer_detected, opportunity_detected
    
#     else:
#         # Decide what to return when the message doesn't have a plaintext body

#         return False, False




# # Retrieve messages
# query_params = {
#     "newer_than": (11, "month"),
#     "older_than": (10, "month"),
#     "label": 'INBOX'
# }
# messages = gmail.get_messages(query=construct_query(query_params))

# # Get all labels
# labels = gmail.list_labels()

# # Check if the label "job_offers" exists
# job_offers_label = None
# for label in labels:
#     if label.name == "job_offers":
#         job_offers_label = label
#         break

# # If the label doesn't exist, create it
# if job_offers_label is None:
#     job_offers_label = gmail.create_label("job_offers")

# # Iterate through the messages
# msg_cnt = 0
# offer_cnt = 0
# for message in messages:
#     msg_cnt += 1
#     # print("This is message number:", msg_cnt)
#     offer_detected, opportunity_detected = analyze_message(message)
#     # print("Offer Detected: {}, Opportunity Detected: {}".format(offer_detected, opportunity_detected))
#     if offer_detected:
#         offer_cnt += 1
#         message.add_label(job_offers_label)
#         print("Offer found in message with Message-ID {} and moved to job_offers folder.".format(message.headers.get('Message-ID')))
#         print("Offer number:", offer_cnt)
#     if opportunity_detected:
#         print("Message with Message-ID {} has a job opportunity.".format(message.headers.get('Message-ID')))
#         receiver_email = message.sender
#         email = extract_email(receiver_email)
#         # print("******",email)
#         msg = message.snippet
#         send_attachment_email(email,msg)  # Uncomment to send an email with attachment to the sender

# print("Total messages analyzed:", msg_cnt)
# print("Total offers found:", offer_cnt)



# ################################################## # ################################################## # ################################################## 




from simplegmail import Gmail
from simplegmail.query import construct_query
from dotenv import load_dotenv
import os
import re
from langchain_anthropic import ChatAnthropic
from langchain.callbacks import tracing_v2_enabled

# Load environment variables from .env file
load_dotenv()

# Initialize  your API key
api_key = os.getenv("x-api-key")

# Initialize Gmail
gmail = Gmail()

def extract_email(sender):
    return re.search(r'<([^<>]+)>', sender).group(1)


def send_attachment_email(email,msg,receiver_email='ishalabhishek93@gmail.com'):
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
    message = gmail.send_message(**params)  # equivalent to send_message(to="you@youremail.com", sender=...)

def parse_gpt_response(response):
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
    # ln = len(message.plain)
    with tracing_v2_enabled(project_name="anthropic_analyze_script_gmail"):      # Change here for changing project in langsmith
        if message.plain is not None:
            # Define the prompt to analyze both job offer and potential opportunity
            prompt = (
                "Analyze below email:\n"
                "1. Is the recipient receiving a job offer letter from the company? True or False\n"
                "2. Is this a potential opportunity from a recruiter? True or False\n"
                "answer in 1. format offer_detected True or False, 2. format opportunity_detected True or False \n"
                + message.plain
            )

            model = ChatAnthropic(model='claude-3-opus-20240229', anthropic_api_key = api_key)
            response =  model.predict(prompt)
            # print(response)
            # completion_text = response.content[0].text
            offer_detected, opportunity_detected = parse_gpt_response(response)
            
            return offer_detected, opportunity_detected
        
        else:
            # Decide what to return when the message doesn't have a plaintext body

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
        # print("******",email)
        msg = message.snippet
        send_attachment_email(email,msg)  # Uncomment to send an email with attachment to the sender

print("Total messages analyzed:", msg_cnt)
print("Total offers found:", offer_cnt)