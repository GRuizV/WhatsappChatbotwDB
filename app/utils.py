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