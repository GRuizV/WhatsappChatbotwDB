# Third-party imports
from twilio.rest import Client
from decouple import config

# Internal imports
import logging
from random import randint, sample


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
        'general discomfort':['Allergies', 'Diarrhea', 'Headaches'],
        'respiratory difficulties':['Asthma', 'Chronic Bronchitis', 'Pneumonia'],
        'gastrointestinal issues':['Gastritis', 'Celiac Disease', 'Irritable Bowel Syndrom (IBS)'],
        'joint or muscular discomfort':['Osteoarthritis', 'Gout', 'Muscle Pain (Myalgia)'],
        'others': ['Urticaria', 'Cystitis', 'Earache']
    }
    drs_specialities_pool = {
        'general discomfort': 'Primary Care Doctors',
        'respiratory difficulties':'Pulmonologists',
        'gastrointestinal issues':'Gastroenterologists',
        'joint or muscular discomfort':'Orthopedists',
        'others': 'Physicians'
        
        }
    drs_names_and_last_names_pool = {
        'names': ['John', 'David', 'Michael', 'Jennifer', 'Susan', 'Elizabeth'],
        'last_names':['Patel', 'Miller', 'Johnson', 'Davis', 'Garcia', 'Martin']
        }
    weekday_pool = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    time_pool = ['1:00 PM', '10:30 AM', '4:45 PM', '8:15 AM']
    med_cent_pool = ['Mayo Clinic - Rochester', 'Cleveland Clinic', 'The Johns Hopkins Hospital', 'Massachusetts General Hospital', 'Stanford Health Care - Stanford Hospital']


    def __init__(self) -> None:
        self.user_number:str = None
        self.patient_id:str = None
        self.patient_name:str = None
        self.patient_discomfort: str = None
        self.patient_pre_existence: str = None
        self.treating_dr:str = None
        self.appointment_type:str = None


    def send_message(self, body_text:str) -> None:

        '''This function send a message to the user through Twilio's API'''

        try:
            message = client.messages.create(
                from_=TWILIO_NUMBER,
                body=body_text,
                to=self.user_number
                )
            
            logger.info(f"Message sent to {self.user_number}: {message.body}")

        except Exception as e:
            logger.error(f"Error sending message to {self.user_number}: {e}")
    


    def check_reply(self, messange:str, reply_options:list[str]) -> str:

        '''
        This function validates that the user's response are within expected.
        '''

        while True:

            # Send the greeting message to the user
            self.send_message(messange)
        
            # Need to figure how to capture the response from the server
            user_response = ''' Something to take the User's response from the server '''
            
            # Check for early exit
            if user_response.lower() == 'exit':
                return self.early_exit() # Early exit the conversation
            
            # Check if the user's response is within expected
            if user_response.lower() in reply_options:
                return user_response
            
            # Non-complying user's reply
            non_complying_reply = f'Sorry! you reply is not one of the available options.'
            self.send_message(non_complying_reply)


            
    def early_exit(self) -> str:

        '''
        This function Finishes the chat with the user if it's detected that the user intents to close the chat.

            - This must include an early closing message sent to the customer and the DB closing.           
        '''
                
        pass











# Conversation Flow

def conversation(user_number:str):


    # Create a Handler that takes care of the chatbot ops
    chatbot_session = MessageHandler()

    # Save the User Number
    chatbot_session.user_number = user_number




    # 1. GREETING
    #    Greeting Message
    greeting_message = f'''Hi there! 👋

🧑‍⚕️​ Welcome to St. John's Health Group Virtual Assistant.✝️​⛪​ 

I'm here to help you with any questions or issues you might have regarding your health. 

Before we move on, could you please provide your ID followed by your full name so I can address your request appropiately?

Please reply as follows: *ID's Number*, *Patient's Full Name*
'''
    
    #   Send the greeting message to the user
    chatbot_session.send_message(greeting_message)

    #   Need to figure how to capture the response from the server
    user_response = ''' Something to take the User's response from the server '''
    
    #   Process the patient response to the greeting
    chatbot_session.patient_id, chatbot_session.patient_name = [elem.strip().title() for elem in user_response.split(',')]




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

    user_response = chatbot_session.check_reply(new_message, ['general discomfort', 'respiratory difficulties', 'gastrointestinal issues', 'joint/muscular discomfort', 'others'])
    
    #   Save the Patient Discomfort
    chatbot_session.patient_discomfort = user_response




    # 3. PATIENT'S PRE-EXISTING DIAGNOSIS
    #   Check if the patient has a pre-existing diagnosis for their discomfort 
    new_message = f'''Do you have a previous diagnosis for your current ailment?
- Yes
- No'''        
   
    user_response = chatbot_session.check_reply(new_message, ['yes', 'no'])

    # Generating a pre-existing ailment
    if user_response.lower() == 'yes':

        # pre_existences_pool dict Class var, in 'patient_discomfort' instance var. 
        pre_existing_ailments = chatbot_session.pre_existences_pool[chatbot_session.patient_discomfort]

        ailment_index = randint(0, len(pre_existing_ailments))  # Generate a random index to have a pre-existing ailment

        # Save the random generated patient pre-existence
        chatbot_session.patient_pre_existence = pre_existing_ailments[ailment_index]




    # 4. PATIENT'S TREATING DOCTOR
    #   Check if the patient want to be treated by their "current treating doctor"
    new_message = f'''Would you like to be attended by your current treating doctor?
- Yes
- No'''    

    user_response = chatbot_session.check_reply(new_message, ['yes', 'no'])

    # Generating a dr's name and last name
    if user_response.lower() == 'yes':

        # Generate dr's names and last names options. 
        dr_names_options = chatbot_session.drs_names_and_last_names_pool['names']
        dr_last_names_options = chatbot_session.drs_names_and_last_names_pool['last_names']

        # Generate the seeds of the resulting dr's name and last name
        dr_names_index = randint(0, len(dr_names_options))
        dr_last_name_index = randint(0, len(dr_last_names_options))

        # Set the actual dr's name and last name
        chatbot_session.treating_dr = f'{dr_names_options[dr_names_index]} {dr_last_names_options[dr_last_name_index]}'
    

    else:
        
        # Generate a doctor's speciality based on patient discomfort
        dr_speciality = chatbot_session.drs_specialities_pool[chatbot_session.patient_discomfort]

        # Generate dr's names and last names options. 
        dr_names_options = chatbot_session.drs_names_and_last_names_pool['names']
        dr_last_names_options = chatbot_session.drs_names_and_last_names_pool['last_names']

        # Generate seeds to randomly generate 3 different options for drs names and last names
        name_op1, name_op2, name_op3 = sample(range(dr_names_options),3)
        lastname_op1, lastname_op2, lastname_op3 = sample(range(dr_last_names_options),3)

        # Define the actual 3 options of drs for the user to choose
        dr_op_1 = f'{dr_names_options[name_op1]} {dr_last_names_options[lastname_op1]}'
        dr_op_2 = f'{dr_names_options[name_op2]} {dr_last_names_options[lastname_op2]}'
        dr_op_3 = f'{dr_names_options[name_op3]} {dr_last_names_options[lastname_op3]}'

        # Generate the text body that will be sent to the user
        new_message = f'''Ok! Currently we count with this {dr_speciality} to take care of you ailment:
1. {dr_op_1}
2. {dr_op_2}
3. {dr_op_3}

Which {dr_speciality[:-1]} would you like be attended by?
''' # the 'dr_speciality[:-1]' is to name the singular of the dr specialities
        
    # Create the list of possible replies
    users_replies = [dr_op_1.lower(), dr_op_2.lower(), dr_op_3.lower(), '1', '2', '3']

    # Check the user's reply is within expected
    user_response = chatbot_session.check_reply(new_message, users_replies)

    # Save the user's choosen dr
    chatbot_session.treating_dr = user_response.title()




    # 5. TYPE OF APPOINTMENT
    #   Check whether the patient wants a virtual or presential appointment"
    new_message = f'''Would you rather having the appointment virtuall or presentially?

- Presential
- Virtual'''    

    # Check the user's reply
    user_response = chatbot_session.check_reply(new_message, ['presential', 'virutal'])

    # Determine patient's ailment (Gral or specific, if there is a pre-existence)
    patient_ailment = chatbot_session.patient_pre_existence if chatbot_session.patient_pre_existence else chatbot_session.patient_discomfort

    # Configure the closing message according to the appointment type selected
    if user_response.lower() == 'presential':

        # Determine the day, the time and location of the appointment randomly
        #   Seeds
        time_index = randint(0,len(chatbot_session.time_pool))
        weekday_index = randint(0,len(chatbot_session.weekday_pool))
        med_center_index = randint(0,len(chatbot_session.med_cent_pool))

        #   Actual time, weekday and location
        appointment_time = chatbot_session.time_pool[time_index]
        appointment_weekday = chatbot_session.time_pool[weekday_index]
        appointment_med_center = chatbot_session.med_cent_pool[med_center_index]

        # Generate the closing message
        new_message = f'''Alright! Thank you for reaching out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️

The medical appointment for the patient {chatbot_session.patient_name}, identified with ID #{chatbot_session.patient_id} was booked with Dr. {chatbot_session.treating_dr}
in {appointment_med_center} the next {appointment_weekday} at {appointment_time} to review patient's {patient_ailment.title()}.

Please remember to be present at reception 15 minutes prior to your appointment with your valid ID.

Thanks for preferring our services! 😊​
We hope you get better in no time ❤️‍🩹​'''


    else:

        # Generate the closing message
        new_message = f'''Alright! Thank you for reaching out St. John's Health Group Virtual Assistance Service. ✝️🧑‍⚕️

The medical appointment for the patient {chatbot_session.patient_name}, identified with ID #{chatbot_session.patient_id} was booked with Dr. {chatbot_session.treating_dr}
virtually to review patient's {patient_ailment.title()}.

Please remember be online 10 minutes prior to the appointment and also be sure to have a stable connection, access to a webcam and microphone to make sure the appointment will happen without inconvenience.

Thanks for preferring our services! 😊​
We hope you get better in no time ❤️‍🩹​'''


    # Send the message to the user
    chatbot_session.send_message(new_message)


    # Close the DB session 
    #Write the code to close the DB session










