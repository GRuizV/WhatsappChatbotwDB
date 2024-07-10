# # Third-party imports
# from twilio.rest import Client
# from decouple import config

# Internal imports
import logging
from random import randint, sample


# # CONSTANS
#     # Find your Account SID and Auth Token at twilio.com/console
#     # and set the environment variables. See http://twil.io/secure
# ACCOUNT_SID = config("TWILIO_ID")
# AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
# TWILIO_NUMBER = config('TWILIO_NUMBER')

# # Twilio's Client Creation
# client = Client(ACCOUNT_SID, AUTH_TOKEN)

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)





# This class will be the one who manage the patient's info storing, generating appointment variables and functions related with the chat
class MessageHandler:

    # CLASS VARIABLES - Variables Pools
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
        'names': ['John', 'David', 'Michael', 'Stephen', 'Edward', 'Jennifer', 'Susan', 'Elizabeth', 'Christina', 'Margaret'],
        'last_names':['Patel', 'Miller', 'Johnson', 'Davis', 'Garcia', 'Martin', 'Brooks', 'Collins', 'Harris', 'Cheng']
        }
    
    weekday_pool = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    time_pool = ['1:00 PM', '10:30 AM', '4:45 PM', '8:15 AM', '7:20 AM', '2:40 PM']
    med_cent_pool = ['Mayo Clinic - Rochester', 'Cleveland Clinic', 'The Johns Hopkins Hospital', 'Massachusetts General Hospital', 'Stanford Health Care - Stanford Hospital']




    # INSTANCE DEFINITION - Instance variables
    def __init__(self) -> None:
        self.user_number:str = None
        self.patient_id:str = None
        self.patient_name:str = None
        self.patient_discomfort:str = None
        self.patient_pre_existence:str = None
        self.patient_ailment:str = None
        self.treating_dr:str = None
        self.appointment_day_and_time:str = None
        self.appointment_type:str = None
        self.appointment_location:str = None




    # CHAT FUNCTIONS
    def send_message(self, body_text:str) -> None:

        '''This function send a message to the user through Twilio's API'''

        '# ORIGINAL VERSION'
        # try:
        #     message = client.messages.create(
        #         from_=TWILIO_NUMBER,
        #         body=body_text,
        #         to=self.user_number
        #         )
            
        #     logger.info(f"Message sent to {self.user_number}: {message.body}")

        # except Exception as e:
        #     logger.error(f"Error sending message to {self.user_number}: {e}")

        
        '# CLI VERSION'
        print(body_text)
    
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
            non_complying_reply = f'''Sorry! I didn't understand that. Could you please answer with the options provided?'''

            '# ORIGINAL VERSION'
            # self.send_message(non_complying_reply)
            
            
            '# CLI VERSION'
            print(non_complying_reply)
            
    def early_exit(self) -> str:

        '''
        This function Finishes the chat with the user if it's detected that the user intents to close the chat.

            - This must include an early closing message sent to the customer and the DB closing.           
        '''
        
        early_closing_message = f'''Alright! I will close this query now.

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹
'''
        
        '# ORIGINAL VERSION'
        # PENDING...
        
        '# CLI VERSION'
        return print(early_closing_message)




    # CHAT STEPS

    #   1. Greeting
    def handle_greeting(self) -> None:

        #   Greeting Message
        greeting_message = f'''Hi there! 👋

🧑‍⚕️​ Welcome to St. John's Health Group Virtual Assistant.✝️​⛪​ 

I'm here to help you with any questions or issues you might have regarding your health. 

Before we move on, could you please provide your ID followed by your full name so I can address your request properly?

Please reply as follows: *ID's Number*, *Patient's Full Name*'''
        

        '# ORIGINAL VERSION'
        # #   Send the greeting message to the user
        # self.send_message(greeting_message)

        # #   Need to figure how to capture the response from the server
        # user_response = '''Something to take the User's response from the server '''


        '# CLI VERSION'
        user_response = input(greeting_message)

        # Check if the user's answer is valid
        while True:

            if user_response.count(',') == 1:
                break

            print(f'''\nSorry, I didn't understand that. Let's try again!\n''')

            user_response = input(f'''Could you please provide your ID followed by your full name so I can address your request properly?

Please reply as follows: *ID's Number*, *Patient's Full Name''')


        #   Process the patient response to the greeting
        self.patient_id, self.patient_name = [' '.join(elem.strip().split()).lower().title() for elem in user_response.split(',')]

    #   2. Symptoms Handling (Patient's discomfort)
    def handle_symptoms(self) -> None:

        # Confirm with a message using patient's name, instruct for the following step and capture the patient's discomfort 
        new_message = f'''Alright, {self.patient_name}, thanks for reaching out. 😊​

⚠️ Note: You can end this chat any time by replying with 'exit' and your query will be closed. 

Now, could you please describe with this options your symptoms?

    1. General Discomfort
    2. Respiratory Difficulties
    3. Gastrointestinal Issues
    4. Joint/Muscular Discomfort
    5. Other Health Issues'''    
        
        # Check the user's reply is within expected
        user_response = self.check_reply(new_message, ['general discomfort', 'respiratory difficulties', 'gastrointestinal issues', 'joint/muscular discomfort', 'other health issues', '1', '2', '3', '4', '5'])

            # If early exit occurred
        if not user_response:
            return
        

        # Save the Patient Discomfort
            # If the answer is a number
        if user_response in '12345':

            if user_response == '1':
                self.patient_discomfort = 'general discomfort'

            elif user_response == '2':
                self.patient_discomfort = 'respiratory difficulties'

            elif user_response == '3':
                self.patient_discomfort = 'gastrointestinal issues'
            
            elif user_response == '4':
                self.patient_discomfort = 'joint/muscular discomfort'
            
            elif user_response == '5':
                self.patient_discomfort = 'other health issues'

            # if the answer is not a number
        else:        
            self.patient_discomfort = user_response


    #  Check if the patient has a pre-existing diagnosis for their discomfort 
        new_message = f'''Do you have a previous diagnosis for your current {self.patient_discomfort}? (Yes/No)'''       
    
        # Check the user's reply is within expected
        user_response = self.check_reply(new_message, ['yes', 'no'])
        
        # If early exit occurred
        if not user_response:
            return
        

        # Generating a pre-existing ailment
        if user_response.lower() == 'yes':

            # pre_existences_pool dict Class var, in 'patient_discomfort' instance var. 
            pre_existing_ailments = self.pre_existences_pool[self.patient_discomfort]

            # Generate a random index to have a pre-existing ailment
            ailment_index = randint(0, len(pre_existing_ailments)-1)  

            # Save the randomly generated patient pre-existence
            self.patient_pre_existence = pre_existing_ailments[ailment_index]
  
    #   3. Treating doctor selection
    def select_doctor(self) -> None:

        # Define patient's ailment (Gral or specific, if there is a pre-existence)
        self.patient_ailment = self.patient_pre_existence if self.patient_pre_existence else self.patient_discomfort

        # Check if the patient want to be treated by their "current treating doctor"
        new_message = f'''Would you like your current treating doctor to review your {self.patient_ailment}? (Yes/No)'''    

        # Check the user's reply is within expected
        user_response = self.check_reply(new_message, ['yes', 'no'])
        
            # If early exit occurred
        if not user_response:
            return


        # Generating a dr's full name
        if user_response.lower() == 'yes':

            # Generate dr's names and last names options. 
            dr_names_options = self.drs_names_and_last_names_pool['names']
            dr_last_names_options = self.drs_names_and_last_names_pool['last_names']

            # Generate the seeds of the resulting dr's name and last name
            dr_names_index = randint(0, len(dr_names_options)-1)
            dr_last_name_index = randint(0, len(dr_last_names_options)-1)

            # Define the actual dr's name and last name
            user_response = f'{dr_names_options[dr_names_index]} {dr_last_names_options[dr_last_name_index]}'        

        else:
            
            # Generate a doctor's speciality based on patient discomfort
            dr_speciality = self.drs_specialities_pool[self.patient_discomfort]

            # Generate dr's names and last names options. 
            dr_names_options = self.drs_names_and_last_names_pool['names']
            dr_last_names_options = self.drs_names_and_last_names_pool['last_names']

            # Generate seeds to randomly generate 3 different options for drs names and last names
            name_op1, name_op2, name_op3 = sample(dr_names_options,3)
            lastname_op1, lastname_op2, lastname_op3 = sample(dr_last_names_options,3)

            # Define the actual 3 options of drs for the user to choose
            dr_op_1 = f'{name_op1} {lastname_op1}'
            dr_op_2 = f'{name_op2} {lastname_op2}'
            dr_op_3 = f'{name_op3} {lastname_op3}'

            # Generate the text body that will be sent to the user
            #   the 'dr_speciality[:-1]' is to name the singular of the dr specialities
            new_message = f'''We currently count with this {dr_speciality} that can check on your {self.patient_ailment}:

1. {dr_op_1}
2. {dr_op_2}
3. {dr_op_3}

Which {dr_speciality[:-1]} would you like be attended by?'''
            
            # Create the list of possible replies
            user_options = [dr_op_1.lower(), dr_op_2.lower(), dr_op_3.lower(), '1', '2', '3']

            # Check the user's reply is within expected
            user_response = self.check_reply(new_message, user_options)
            
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
        self.treating_dr = user_response.title()

        # Prompt the User the name of the treating doctor
        self.send_message(f'''Ok! Dr. {self.treating_dr} will attend you''')

    #   4. Appointment Day and Time setting
    def appointment_time_booking(self) -> None:

        # Define the day and the time of the appointment randomly
        #   Generate day and time options. 
        time_options = self.time_pool
        day_options = self.weekday_pool

        #   Generate seeds to randomly generate 2 different options for day and time for the appointment
        time_op1, time_op2, = sample(time_options, 2)
        day_op1, day_op2 = sample(day_options, 2)

        #   Define the actual 2 options of day/time for the user to choose
        day_and_time_op_1 = f'{day_op1} {time_op1}'
        day_and_time_op_2 = f'{day_op2} {time_op2}'
            

        # Create the day/time availability message
        new_message = f'''Currently Dr. {self.treating_dr} has the following time availability:
1. {day_and_time_op_1}
2. {day_and_time_op_2}

Which one would fit best for you?
'''    
        
        # Check the user's reply is within expected
        user_response = self.check_reply(new_message, [day_op1, day_op2, '1', '2'])
        
            # If early exit occurred
        if not user_response:
            return
            

        # Convert the user's choice into the actual dr's full name
        if user_response in '12':

            if user_response == '1':
                self.appointment_day_and_time = day_and_time_op_1
            
            else:
                self.appointment_day_and_time = day_and_time_op_2
        
        
        # Prompt the User the day and time of the appointment.
        self.send_message(f'''Ok! the appointment with Dr. {self.treating_dr} to check on your {self.patient_ailment.title()} is booked for next {self.appointment_day_and_time}''')
    
    #   5. Appointment type setting
    def select_appointment_type(self) -> None:

        #   Check whether the patient wants a virtual or presential appointment"
        new_message = f'''Would you rather having your medical appointment with Dr. {self.treating_dr} presentially or virtually?

1. Presentially
2. Virtually'''    

        # Check the user's reply is within expected
        user_response = self.check_reply(new_message, ['presentially', 'virtually', '1', '2'])

            # If early exit occurred
        if not user_response:
            return

        # Save patient's appointment type
        if user_response in '12':

            if user_response == '1':
                self.appointment_type = 'presentially'
            
            else:
                self.appointment_type = 'virtually'

        else:   
            self.appointment_type = user_response


        # Configure the closing message according to the appointment type selected
        if self.appointment_type == 'presentially':

            # Generte a seed to randomly choose a medical center
            med_center_index = randint(0,len(self.med_cent_pool)-1)

            # Set the appointment location
            self.appointment_location = self.med_cent_pool[med_center_index]

            # Generate the closing message
            new_message = f'''Alright! The medical appointment for the patient {self.patient_name}, identified with ID #{self.patient_id} was booked with Dr. {self.treating_dr} at {self.appointment_location} next {self.appointment_day_and_time} to check patient's {self.patient_ailment.title()}.

Please remember to be present at reception 15 minutes prior to your appointment with your valid ID.

Thank you for contacting St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹 '''


        else:

            # Generate the closing message
            new_message = f'''Alright! The medical appointment for the patient {self.patient_name}, identified with ID #{self.patient_id} was booked with Dr. {self.treating_dr} virtually for the next {self.appointment_day_and_time} to check patient's {self.patient_ailment.title()}.

Please remember be online 10 minutes prior to the appointment and also be sure to have a stable connection, access to a webcam and microphone to make sure the appointment will happen without inconvenience.

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹'''


        '# ORIGINAL VERSION'
        # Send the message to the user
        self.send_message(new_message)









# Example Usage

# Create a Handler that takes care of the chatbot ops
chatbot_session = MessageHandler()

# Save the User Number
chatbot_session.user_number = '3205503934'





# Conversation Flow

# #   1. GREETING
chatbot_session.handle_greeting()

# #   2. PATIENT DISCOMFORT 
chatbot_session.handle_symptoms()

# #   3. TREATING DOCTOR
# chatbot_session.patient_discomfort = 'respiratory difficulties' # Manual definition for testing purposes
# chatbot_session.patient_pre_existence = 'Pneumonia' # Manual definition for testing purposes
chatbot_session.select_doctor()

# #   4. APPOINTMENT TYPE
# chatbot_session.patient_ailment = 'Pneumonia' # Manual definition for testing purposes
# chatbot_session.treating_dr = 'Leon Sardi' # Manual definition for testing purposes
chatbot_session.appointment_time_booking()

#   5. APPOINTMENT TYPE
# chatbot_session.patient_ailment = 'Pneumonia' # Manual definition for testing purposes
# chatbot_session.treating_dr = 'Leon Sardi' # Manual definition for testing purposes
# chatbot_session.appointment_day_and_time = 'Wednesday 4:45 PM' # Manual definition for testing purposes
chatbot_session.select_appointment_type()

x=0





# # Close the DB session 
# Write the code to close the DB session
