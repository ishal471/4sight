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
    if message.plain is not None:
        # Define the prompt to analyze both job offer and potential opportunity
        prompt = (
            "Analyze below email:\n"
            "1. Is the recipient receiving a job offer letter from the company? True or False\n"
            "2. Is this a potential opportunity from a recruiter? True or False\n"
            "answer in 1. format offer_detected True or False, 2. format opportunity_detected True or False \n"
            + message.plain
        )

        # Call OpenAI's chat completion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        print(response)
        completion_text = response["choices"][0]["message"]["content"]
        
        offer_detected, opportunity_detected = parse_gpt_response(completion_text)
        
        return offer_detected, opportunity_detected
    else:
        # Decide what to return when the message doesn't have a plaintext body
        return False, False


def test_analyze_message():
    # Mock message with a plain text body
    class MockMessage:
        def __init__(self, plain):
            self.plain = plain

    # Test case 1: Message containing a job offer
    message_with_offer = MockMessage(
        "Congratulations! We are pleased to offer you a position as a data scientist at our company. Plese find more details in the offer letter."
    )
    offer_detected, opportunity_detected = analyze_message(message_with_offer)
    assert offer_detected == True
    assert opportunity_detected == False

    # Test case 2: Message containing a potential opportunity
    message_with_opportunity = MockMessage(
        "Hello, we have reviewed your resume and would like to discuss potential opportunities."
    )
    offer_detected, opportunity_detected = analyze_message(message_with_opportunity)
    assert offer_detected == False
    assert opportunity_detected == True

    # Test case 3: Message containing neither a job offer nor a potential opportunity
    message_no_offer_or_opportunity = MockMessage(
        "Thank you for your application. We will keep your resume on file for future openings."
    )
    offer_detected, opportunity_detected = analyze_message(message_no_offer_or_opportunity)
    assert offer_detected == False
    assert opportunity_detected == False

    print("All test cases passed!")

# Run the test
test_analyze_message()