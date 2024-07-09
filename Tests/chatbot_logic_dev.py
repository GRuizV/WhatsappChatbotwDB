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





# This class will be the one who manage the patient's info storing, generating appointment variables and functions related with the chat
class MessageHandler:

    # Variables Pools
    pre_existences_pool = {
        'general discomfort':['Allergies', 'Diarrhea', 'Headaches'],
        'respiratory difficulties':['Asthma', 'Chronic Bronchitis', 'Pneumonia'],
        'gastrointestinal issues':['Gastritis', 'Celiac Disease', 'Irritable Bowel Syndrom (IBS)'],
        'joint/muscular discomfort':['Osteoarthritis', 'Gout', 'Muscle Pain (Myalgia)'],
        'other health issues': ['Urticaria', 'Cystitis', 'Earache']
    }
    drs_specialities_pool = {
        'general discomfort': 'Primary Care Doctors',
        'respiratory difficulties':'Pulmonologists',
        'gastrointestinal issues':'Gastroenterologists',
        'joint/muscular discomfort':'Orthopedists',
        'other health issues': 'Physicians'
        
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

        '''This function validates that the user's response are within expected.'''

        while True:
            
            '# ORIGINAL VERSION'
            # # Send the greeting message to the user
            # self.send_message(messange)

            '# CLI VERSION'
            user_response = input(messange)
        

            # # Need to figure how to capture the response from the server
            # user_response = ''' Something to take the User's response from the server '''
            

            # Check for early exit
            if user_response.lower() == 'exit':
                return self.early_exit() # Early exit the conversation
            

            # Check if the user's response is within expected
            if user_response.lower() in reply_options:
                return user_response.lower()
            
            
            # # Non-complying user's reply
            non_complying_reply = f'Sorry! you reply is not one of the available options.'

            '# ORIGINAL VERSION'
            # self.send_message(non_complying_reply)
            
            
            '# CLI VERSION'
            print(non_complying_reply)


            
    def early_exit(self) -> str:

        '''
        This function Finishes the chat with the user if it's detected that the user intents to close the chat.

            - This must include an early closing message sent to the customer and the DB closing.           
        '''
        
        early_closing_message = f'''Alright! We will close this query now.

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹
'''
        
        '# ORIGINAL VERSION'
        # PENDING...
        
        '# CLI VERSION'
        return print(early_closing_message)











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
    
    '# ORIGINAL VERSION'
    # #   Send the greeting message to the user
    # chatbot_session.send_message(greeting_message)

    # #   Need to figure how to capture the response from the server
    # user_response = '''Something to take the User's response from the server '''


    '# CLI VERSION'
    user_response = input(greeting_message)

    # Check if the user's answer is valid
    while True:

        if user_response.count(',') == 1:
            break

        print(f'''\nSorry, that is not a valid answer!\n''')

        user_response = input(f'''Could you please provide your ID followed by your full name so I can address your request appropiately?

Please reply as follows: *ID's Number*, *Patient's Full Name*

''')


    #   Process the patient response to the greeting
    chatbot_session.patient_id, chatbot_session.patient_name = [' '.join(elem.strip().split()).lower().title() for elem in user_response.split(',')]


    # 2. PATIENT DISCOMFORT
    #   Confirm with a message using patient's name, instruct for the following step and capture the patient's discomfort 
    new_message = f'''Alright, {chatbot_session.patient_name}, thanks for reaching out. 😊​

⚠️ Note: You can end this chat any time by replying with 'exit' and your query will be closed. 

Now, what is the reason for your query?

    1. General Discomfort
    2. Respiratory Difficulties
    3. Gastrointestinal Issues
    4. Joint/Muscular Discomfort
    5. Other Health Issues

'''    
    
    # Check the user's reply is within expected
    user_response = chatbot_session.check_reply(new_message, ['general discomfort', 'respiratory difficulties', 'gastrointestinal issues', 'joint/muscular discomfort', 'other health issues', '1', '2', '3', '4', '5'])

        # If early exit occurred
    if not user_response:
        return
    

    # Save the Patient Discomfort
        # If the answer is a number
    if user_response in '12345':

        if user_response == '1':
            chatbot_session.patient_discomfort = 'general discomfort'

        elif user_response == '2':
            chatbot_session.patient_discomfort = 'respiratory difficulties'

        elif user_response == '3':
            chatbot_session.patient_discomfort = 'gastrointestinal issues'
        
        elif user_response == '4':
            chatbot_session.patient_discomfort = 'joint/muscular discomfort'
        
        elif user_response == '5':
            chatbot_session.patient_discomfort = 'other health issues'

        # if the answer is not a number
    else:        
        chatbot_session.patient_discomfort = user_response




    # 3. PATIENT'S PRE-EXISTING DIAGNOSIS
    #   Check if the patient has a pre-existing diagnosis for their discomfort 
    new_message = f'''Do you have a previous diagnosis for your current {chatbot_session.patient_discomfort}?
- Yes
- No

'''       
   
    # Check the user's reply is within expected
    user_response = chatbot_session.check_reply(new_message, ['yes', 'no'])
    
        # If early exit occurred
    if not user_response:
        return
    

    # Generating a pre-existing ailment
    if user_response.lower() == 'yes':

        # pre_existences_pool dict Class var, in 'patient_discomfort' instance var. 
        pre_existing_ailments = chatbot_session.pre_existences_pool[chatbot_session.patient_discomfort]

        # Generate a random index to have a pre-existing ailment
        ailment_index = randint(0, len(pre_existing_ailments)-1)  

        # Save the randomly generated patient pre-existence
        chatbot_session.patient_pre_existence = pre_existing_ailments[ailment_index]

    
    # Define patient's ailment (Gral or specific, if there is a pre-existence)
    patient_ailment = chatbot_session.patient_pre_existence if chatbot_session.patient_pre_existence else chatbot_session.patient_discomfort


    # 4. PATIENT'S TREATING DOCTOR
    #   Check if the patient want to be treated by their "current treating doctor"
    new_message = f'''Would you like your current treating doctor to review your {patient_ailment}?
- Yes
- No

'''    

    # Check the user's reply is within expected
    user_response = chatbot_session.check_reply(new_message, ['yes', 'no'])
    
        # If early exit occurred
    if not user_response:
        return


    # Generating a dr's name and last name
    if user_response.lower() == 'yes':

        # Generate dr's names and last names options. 
        dr_names_options = chatbot_session.drs_names_and_last_names_pool['names']
        dr_last_names_options = chatbot_session.drs_names_and_last_names_pool['last_names']

        # Generate the seeds of the resulting dr's name and last name
        dr_names_index = randint(0, len(dr_names_options)-1)
        dr_last_name_index = randint(0, len(dr_last_names_options)-1)

        # Define the actual dr's name and last name
        user_response = f'{dr_names_options[dr_names_index]} {dr_last_names_options[dr_last_name_index]}'
    

    else:
        
        # Generate a doctor's speciality based on patient discomfort
        dr_speciality = chatbot_session.drs_specialities_pool[chatbot_session.patient_discomfort]

        # Generate dr's names and last names options. 
        dr_names_options = chatbot_session.drs_names_and_last_names_pool['names']
        dr_last_names_options = chatbot_session.drs_names_and_last_names_pool['last_names']

        # Generate seeds to randomly generate 3 different options for drs names and last names
        name_op1, name_op2, name_op3 = sample(dr_names_options,3)
        lastname_op1, lastname_op2, lastname_op3 = sample(dr_last_names_options,3)

        # Define the actual 3 options of drs for the user to choose
        dr_op_1 = f'{name_op1} {lastname_op1}'
        dr_op_2 = f'{name_op2} {lastname_op2}'
        dr_op_3 = f'{name_op3} {lastname_op3}'

        # Generate the text body that will be sent to the user
        #   the 'dr_speciality[:-1]' is to name the singular of the dr specialities
        new_message = f'''Ok! We currently count with this {dr_speciality} that can check on your {patient_ailment}:
1. {dr_op_1}
2. {dr_op_2}
3. {dr_op_3}

Which {dr_speciality[:-1]} would you like be attended by?

'''
        
        # Create the list of possible replies
        user_options = [dr_op_1.lower(), dr_op_2.lower(), dr_op_3.lower(), '1', '2', '3']

        # Check the user's reply is within expected
        user_response = chatbot_session.check_reply(new_message, user_options)
        
            # If early exit occurred
        if not user_response:
            return
        

    # Convert the user's choice into the actual dr's full name
    if user_response in '123':

        if user_response == '1':
            user_response = dr_op_1
        
        elif user_response == '2':
            user_response = dr_op_2
        
        else:
            user_response = dr_op_3
    
    # Save the user's choosen doctor
    chatbot_session.treating_dr = user_response.title()




    # 5. TYPE OF APPOINTMENT
    #   Check whether the patient wants a virtual or presential appointment"
    new_message = f'''Would you rather having a virtual appointment or would you liked to be attended presentially?

- Presential
- Virtual

'''    

    # Check the user's reply is within expected
    user_response = chatbot_session.check_reply(new_message, ['presential', 'virtual'])

        # If early exit occurred
    if not user_response:
        return


    # Save patient's appointment type
    chatbot_session.appointment_type = user_response

    # Configure the closing message according to the appointment type selected
    if chatbot_session.appointment_type == 'presential':

        # Define the day, the time and location of the appointment randomly
        #   Seeds
        time_index = randint(0,len(chatbot_session.time_pool)-1)
        weekday_index = randint(0,len(chatbot_session.weekday_pool)-1)
        med_center_index = randint(0,len(chatbot_session.med_cent_pool)-1)

        #   Actual time, weekday and location
        appointment_time = chatbot_session.time_pool[time_index]
        appointment_weekday = chatbot_session.weekday_pool[weekday_index]
        appointment_med_center = chatbot_session.med_cent_pool[med_center_index]

        # Generate the closing message
        new_message = f'''Alright! The medical appointment for the patient {chatbot_session.patient_name}, identified with ID #{chatbot_session.patient_id} was booked with Dr. {chatbot_session.treating_dr}
in {appointment_med_center} the next {appointment_weekday} at {appointment_time} to review patient's {patient_ailment.title()}.

Please remember to be present at reception 15 minutes prior to your appointment with your valid ID.

Thank you for contacting St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹
​'''


    else:

        # Generate the closing message
        new_message = f'''Alright! The medical appointment for the patient {chatbot_session.patient_name}, identified with ID #{chatbot_session.patient_id} was booked with Dr. {chatbot_session.treating_dr} virtually to review patient's {patient_ailment.title()}.

Please remember be online 10 minutes prior to the appointment and also be sure to have a stable connection, access to a webcam and microphone to make sure the appointment will happen without inconvenience.

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹
​'''


    '# ORIGINAL VERSION'
    # # Send the message to the user
    # chatbot_session.send_message(new_message)


    '# CLI VERSION'
    print(new_message)

    # Close the DB session 
    #Write the code to close the DB session










conversation('3205503934')