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



class MessageHandler:

    # Variables Pools
    pre_existences_pool = {
        'General Discomfort':['Allergies', 'Diarrhea', 'Headaches'],
        'Respiratory Difficulties':['Asthma', 'Chronic Bronchitis', 'Pneumonia'],
        'Gastrointestinal Issues':['Gastritis', 'Celiac Disease', 'Irritable Bowel Syndrom (IBS)'],
        'Joint/Muscular Discomfort':['Osteoarthritis', 'Gout', 'Muscle Pain (Myalgia)'],
        'Others': ['Urticaria', 'Cystitis', 'Earache']
    }
    drs_names_pool = {
        'General Discomfort': 'Primary Care Doctors',
        'Respiratory Difficulties':'Pulmonologists',
        'Gastrointestinal Issues':'Gastroenterologists',
        'Joint/Muscular Discomfort':'Orthopedists',
        'Others': 'Physicians'
        
        }
    drs_specialities_pool = {
        'names': ['John', 'David', 'Michael', 'Jennifer', 'Susan', 'Elizabeth'],
        'last_names':['Patel', 'Miller', 'Johnson', 'Davis', 'Garcia', 'Martin']
        }
    weekday_pool = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    time_pool = ['1:00 PM', '10:30 AM', '4:45 PM', '8:15 AM']
    med_cent_pool = ['Mayo Clinic - Rochester', 'Cleveland Clinic', 'The Johns Hopkins Hospital', 'Massachusetts General Hospital', 'Stanford Health Care - Stanford Hospital']


    def __init__(self) -> None:
        self.patient_id:str = None
        self.patient_name:str = None
        self.patient_discomfort: str = None
        self.patient_pre_existence: str = None
        self.treating_dr:str = None
        self.appointment_type:str = None
        self.closing_message:str = None


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
    


    def check_reply(reply:str, reply_options:list[str]) -> bool:
        pass

            
    def early_exit() -> str:
        pass




def conversation(user_number:str):

    # Create a Handler that takes care of the chatbot ops
    chatbot_session = MessageHandler()


    # 1. GREETING
    #    Greeting Message
    greeting_message = f'''Hi there! 👋

Welcome to St. John Health Group Virtual Assistant. I'm here to help you with any questions or issues you might have regarding your health. 

Before we move on, could you please provide your ID followed by your full name so I can address your request appropiately?

Please reply as follows: *ID's Number*, *Patient's Full Name*
'''
    
    #   Send the greeting message to the user
    chatbot_session.send_message(user_number, greeting_message)

    #   Need to figure how to capture the response from the server
    user_response = ''' Something to take the User's response from the server '''
    
    #   Process the patient response to the greeting
    chatbot_session.patient_id, chatbot_session.patient_name = [elem.strip() for elem in user_response.split(',')]




    # 2. PATIENT DISCOMFORT
    #   Confirm with a message using patient's name, instruct for the following step and capture the patient's discomfort 
    new_message = f'''Alright, {chatbot_session.patient_name}, thanks for reaching out. 😊​

⚠️​Note: You can end this chat any time by replying with 'exit' and the query will be closed.

Now, what is the reason for your query?

    - General Discomfort
    - Respiratory Difficulties
    - Gastrointestinal Issues
    - Joint/Muscular Discomfort
    - Others
'''    
    
    #   Setting the loop to make sure the user's response is within expected
    user_response_validation = False

    while user_response_validation == False:

        #   Send the greeting message to the user
        chatbot_session.send_message(user_number, new_message)
    
        #   Need to figure how to capture the response from the server
        user_response = ''' Something to take the User's response from the server '''

        #   Make sure the reply is either one of the options or 'exit'
        user_response_validation = chatbot_session.check_reply(user_response, ['General Discomfort', 'Respiratory Difficulties', 'Gastrointestinal Issues', 'Joint/Muscular Discomfort', 'Others', 'exit'])

    #   Check for early exit
    if user_response.lower() == 'exit':
        return chatbot_session.early_exit() # Early exit the conversation
    
    #   Save the Patient Discomfort
    chatbot_session.patient_discomfort = user_response




    # 3. PATIENT'S PRE-EXISTING DIAGNOSIS
    #   Check if the patient has a pre-existing diagnosis for their discomfort 
    new_message = f'''Do you have a previous diagnosis for your current ailment?'''    
    
    #   Setting the loop to make sure the user's response is within expected
    user_response_validation = False

    while user_response_validation == False:

        #   Send the greeting message to the user
        chatbot_session.send_message(user_number, new_message)
    
        #   Need to figure how to capture the response from the server
        user_response = ''' Something to take the User's response from the server '''

        #   Make sure the reply is either one of the options or 'exit'
        user_response_validation = chatbot_session.check_reply(user_response, ['Yes', 'No', 'exit'])







print(f'''Alright X, thanks for reaching out. 😊​

Note: Please remember that you can finish this chat anytime by replying with 'exit' and the query will be closed.

Now, what is the reason for your query?

    - General Discomfort
    - Respiratory Difficulties
    - Gastrointestinal Issues
    - Joint/Muscular Discomfort
    - Others
''')

