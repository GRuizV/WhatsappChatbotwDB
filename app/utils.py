# Third-party imports
from twilio.rest import Client
from decouple import config

# Internal imports
import logging


# CONSTANS
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
ACCOUNT_SID = config("TWILIO_ID")
AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = config('TWILIO_NUMBER')

# Twilio's Client Creation
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Sending message logic through Twilio Messaging API
def send_message(to_number:str, body_text:str) -> None:

    try:
        message = client.messages.create(
            from_=TWILIO_NUMBER,
            body=body_text,
            to=to_number
            )
        
        logger.info(f"Message sent to {to_number}: {message.body}")

    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")




# CHATBOT LOGIC
def generate_response(message:str) -> str:
    return 'This is a replying test message'













'Proposal of new Utils.py definition'
'#####################################################################################'
# # utils.py

# # Third-party imports
# from twilio.rest import Client
# from decouple import config
# import logging

# # Internal imports
# from sqlalchemy.orm import Session
# import database, models
# import datetime

# # CONSTANS
# ACCOUNT_SID = config("TWILIO_ID")
# AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
# TWILIO_NUMBER = config('TWILIO_NUMBER')

# # Twilio's Client Creation
# client = Client(ACCOUNT_SID, AUTH_TOKEN)

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Sending message logic through Twilio Messaging API
# def send_message(to_number: str, body_text: str, quick_replies: list = None) -> None:
#     try:
#         message_data = {
#             'from_': TWILIO_NUMBER,
#             'body': body_text,
#             'to': to_number,
#         }
        
#         if quick_replies:
#             message_data['persistent_action'] = [f'{reply}' for reply in quick_replies]

#         message = client.messages.create(**message_data)
#         logger.info(f"Message sent to {to_number}: {message.body}")

#     except Exception as e:
#         logger.error(f"Error sending message to {to_number}: {e}")

# # Response generation logic
# def generate_response(user_input: str) -> (str, list):
#     if user_input.lower() in ["confirm", "cancel"]:
#         chat_response = "Your appointment has been confirmed." if user_input.lower() == "confirm" else "Your appointment has been canceled."
#         quick_replies = ["Confirm another appointment", "Cancel another appointment"]
#     else:
#         chat_response = "Appointment Reminder\nYour appointment is coming up on July 21 at 3PM"
#         quick_replies = ["Confirm", "Cancel"]
    
#     return chat_response, quick_replies

# # Handle incoming message and generate response
# def handle_message(user_input: str, user_number: str, db: Session):
#     # Check if there's an ongoing conversation
#     ongoing_conversation = db.query(models.Conversation).filter(
#         models.Conversation.user_id == user_number, 
#         models.Conversation.end_time == None
#     ).first()

#     if not ongoing_conversation:
#         # Create a new conversation
#         conversation_id = database.create_conversation(db, user_id=user_number)
#     else:
#         conversation_id = ongoing_conversation.id

#     # Store the received message
#     database.add_message(db, conversation_id, sender=user_number, message=user_input)

#     # Generate a response
#     chat_response, quick_replies = generate_response(user_input)

#     # Store the response message
#     database.add_message(db, conversation_id, sender="bot", message=chat_response)

#     # Send the response back via Twilio with quick replies
#     send_message(user_number, chat_response, quick_replies)

#     # If the conversation is over, update the end_time (you can define your own logic to determine this)
#     if chat_response.lower() in ["bye", "goodbye", "see you"]:
#         database.end_conversation(db, conversation_id)
    
#     return chat_response
'#####################################################################################'





