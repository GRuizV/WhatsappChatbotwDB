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



# CHATBOT LOGIC
# This class will be who manage the patient's info storing, generating appointment variables and functions related with the chat
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

        self.conversation_stage:str = '' # Stages are: '' / 'greeting' / 'symptoms' / 'previous_diagnosis' / 'select_doctor' -> opt:'doctor_speciality' / 'appointment_time' / 'appointment_type' / 'completed'
        self.conversation_input:dict = {
            'user_response': None,
            'last_message': None,
            'replying_options': None
        }        
        self.user_number:str = None
        self.patient_id:str = None
        self.patient_name:str = None
        self.patient_discomfort:str = None
        self.patient_pre_existence:str = None
        self.patient_ailment:str = None
        self.treating_dr:str = None
        self.dr_speciality:str = None
        self.appointment_day_and_time:str = None
        self.appointment_type:str = None
        self.appointment_location:str = None


    def reset_state(self):

        '''This function resets the conversation state for a new query'''

        self.conversation_stage = ''
        self.conversation_input = {
            'user_response': None,
            'last_message': None,
            'replying_options': None
        }
        self.user_number = None
        self.patient_id = None
        self.patient_name = None
        self.patient_discomfort = None
        self.patient_pre_existence = None
        self.patient_ailment = None
        self.treating_dr = None
        self.dr_speciality = None
        self.appointment_day_and_time = None
        self.appointment_type = None
        self.appointment_location = None
    


    # CHAT FUNCTIONS
    def process_message(self) -> None:

        '''This function process the incoming message and directs the execution to its respective stage'''

        if self.conversation_stage == '':
            
            # Greeting Message
            greeting_message = f'''Hi there! 👋

🧑‍⚕️​ Welcome to St. John's Health Group Virtual Assistant.✝️​⛪​ 

I'm here to help you with any questions or issues you might have regarding your health. 

Before we move on, could you please provide your ID followed by your full name so I can address your request properly?

Please reply as follows: _ID's Number_, _Patient's Full Name_'''
            
            # Send the greeting message
            self.send_message(greeting_message)

            # Change the stage to when the user responds it goes to the handle_greeting func
            self.conversation_stage = 'greeting' 
        
        elif self.conversation_stage == 'greeting':
            self.handle_greeting()
        
        elif self.conversation_stage == 'symptoms':
             self.handle_symptoms()

        elif self.conversation_stage == 'previous_diagnosis':
            self.previous_diagnosis()

        elif self.conversation_stage == 'select_doctor':
            self.select_doctor()
           
        elif self.conversation_stage == 'doctor_speciality':
            self.doctor_speciality()
                   
        elif self.conversation_stage == 'appointment_time':
            self.appointment_time_booking()
       
        elif self.conversation_stage == 'appointment_type':
            self.select_appointment_type()

        elif self.conversation_stage == 'completed':
            self.send_message(f'''_Your query has been completed, if you would like to start a new one, please type anything start a new conversation_''')
            self.reset_state()
    
    def send_message(self, body_text:str) -> None:

        '''This function send a message to the user through Twilio's API'''

        try:
            message = client.messages.create(
                from_=TWILIO_NUMBER,
                body=body_text,
                to=self.user_number
                )
            
            logger.info(f"\n\nMessage sent to {self.user_number}: {message.body}\n")

        except Exception as e:
            logger.error(f"\n\nError sending message to {self.user_number}: {e}\n")
    
    def check_reply(self) -> str:

        '''This function validates that the user's response are within expected.'''
        
        # Check for early exit
        if self.conversation_input['user_response'] == 'exit':
            return self.early_exit()

        # Check if the user's response is within expected
        elif self.conversation_input['user_response'] in self.conversation_input['replying_options']:

            # Return 'True' to continue to the rest of the conversation stage
            return True                  
        
        else:
            # Define the Non-complying user's reply
            non_complying_reply = f'''Sorry! I didn't understand that. Could you please answer with the options provided?'''

            # Send the Non-complying user's reply
            self.send_message(non_complying_reply)

            # Send the last question asked to remind the user the valid responses                 
            self.send_message(self.conversation_input['last_message'])
    
    def early_exit(self) -> None:

        '''
        This function finishes the chat with the user if it's detected that the user intents to close the chat.

            - This must include an early closing message sent to the customer and the DB closing.           
        '''
        
        # Create the early closing message
        early_closing_message = f'''Alright! I will close this query now.

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹'''
        
        # Send the early closing message
        self.send_message(early_closing_message)

        # Close the conversation in the DB
        'Write the DB conversation closing'

        # Reset the conversation stage for future queries
        self.reset_state()




    # CHAT STAGES / 'stage_name'
    #   1. Greeting / 'geeting'
    def handle_greeting(self) -> None:

        '''This function handles the first contact validation, capture the ID and the name of the patient and prompts the message for the next step'''

        # Check if the user response met the '*ID's Number*, *Patient's Full Name' criteria
        if self.conversation_input['user_response'].count(',') != 1:
            
            self.send_message(f'''\nSorry, I didn't understand that. Let's try again!\n''')

            self.send_message(f'''Could you please provide your ID followed by your full name so I can address your request properly?

Please reply as follows: _ID's Number_, _Patient's Full Name_''')

        else:

            # Save the patient's name and ID provided in the greeting response
            self.patient_id, self.patient_name = [' '.join(elem.strip().split()).lower().title() for elem in self.conversation_input['user_response'].split(',')]

            # Move on to the next stage
            self.conversation_stage = 'symptoms'

            # Log the stage change
            logger.info(f"\nStage chaged to: {self.conversation_stage}\n")

            # Define the message to confirm their input and to lead to the next stage
            new_message = f'''Alright, {self.patient_name.split()[0]}, thanks for reaching out. 😊​

Now, Let's start checking on your symptoms.
                            
⚠️ Note: You can end this chat any time by replying with *'exit'* and your query will be closed
                            
Could you please describe your symptoms with the following options?

    1. General Discomfort
    2. Respiratory Difficulties
    3. Gastrointestinal Issues
    4. Joint/Muscular Discomfort
    5. Other Health Issues'''
            
            # Send the message
            self.send_message(new_message)

            # Define the last message for if it's needed to be reminded to the user if in the next stage it fails the reply cheking
            self.conversation_input['last_message'] = f'''Could you please describe your symptoms with the following options?

    1. General Discomfort
    2. Respiratory Difficulties
    3. Gastrointestinal Issues
    4. Joint/Muscular Discomfort
    5. Other Health Issues'''

            # Define the replying options for the next stage checking
            self.conversation_input['replying_options'] = ['general discomfort', 'respiratory difficulties', 'gastrointestinal issues', 'joint/muscular discomfort', 'other health issues', '1', '2', '3', '4', '5']

    #   2. Symptoms Handling / 'symptoms'
    def handle_symptoms(self) -> None:

        # Check the user's reply is within expected
        if self.check_reply():    

            # Save the Patient Discomfort
            #   If the answer is a number
            if self.conversation_input['user_response'] in '12345':

                if self.conversation_input['user_response'] == '1':
                    self.patient_discomfort = 'general discomfort'

                elif self.conversation_input['user_response'] == '2':
                    self.patient_discomfort = 'respiratory difficulties'

                elif self.conversation_input['user_response'] == '3':
                    self.patient_discomfort = 'gastrointestinal issues'
                
                elif self.conversation_input['user_response'] == '4':
                    self.patient_discomfort = 'joint/muscular discomfort'
                
                elif self.conversation_input['user_response'] == '5':
                    self.patient_discomfort = 'other health issues'

            #   If the answer is not a number
            else:        
                self.patient_discomfort = self.conversation_input['user_response']


            # Move on to the next stage
            self.conversation_stage = 'previous_diagnosis'

            # Log the stage change
            logger.info(f"\nStage chaged to: {self.conversation_stage}\n")

            # Define the message to lead to the next stage
            new_message = f'''Do you have a previous diagnosis for your current {self.patient_discomfort.title()}? (Yes/No)'''
            
            # Send the message
            self.send_message(new_message)

            # Define the last message for if it's needed to be reminded to the user if in the next stage it fails the reply cheking
            self.conversation_input['last_message'] = new_message

            # Define the replying options for the next stage checking
            self.conversation_input['replying_options'] = ['yes', 'no']

    #   2.1. Pre-Existence Handling / 'previous_diagnosis'
    def previous_diagnosis(self) -> None:
        
        # Check the user's reply is within expected
        if self.check_reply():   

            # Generating a pre-existing ailment
            if self.conversation_input['user_response'] == 'yes':

                # Calling the predetermined ailments according to each type of symptom
                pre_existing_ailments = self.pre_existences_pool[self.patient_discomfort]

                # Generate a random index to define the pre-existing ailment
                ailment_index = randint(0, len(pre_existing_ailments)-1)  

                # Save the randomly generated patient pre-existence
                self.patient_pre_existence = pre_existing_ailments[ailment_index]


            # Set the patient's ailment according to whether the user said about having a previous diagnosis
            self.patient_ailment = self.patient_pre_existence.title() if self.patient_pre_existence else self.patient_discomfort.title()

            # Move on to the next stage
            self.conversation_stage = 'select_doctor'

            # Log the stage change
            logger.info(f"\nStage chaged to: {self.conversation_stage}\n")
            
            # Define the message to lead to the next stage
            new_message = f'''Would you like your current treating doctor to review your {self.patient_ailment}? (Yes/No)'''
            
            # Send the message
            self.send_message(new_message)

            # Define the last message for if it's needed to be reminded to the user if in the next stage it fails the reply cheking
            self.conversation_input['last_message'] = new_message

            # Define the replying options for the next stage checking
            self.conversation_input['replying_options'] = ['yes', 'no']

    #   3. Treating doctor: Doctor Selecting / 'select_doctor'
    def select_doctor(self) -> None:

        # Check the user's reply is within expected
        if self.check_reply():

            # Generate a doctor's speciality based on patient discomfort
            self.dr_speciality = self.drs_specialities_pool[self.patient_discomfort]

            # Generating a dr's full name
            if self.conversation_input['user_response'] == 'yes':

                # Generate dr's names and last names options. 
                dr_names_options = self.drs_names_and_last_names_pool['names']
                dr_last_names_options = self.drs_names_and_last_names_pool['last_names']

                # Generate the seeds of the resulting dr's name and last name
                dr_names_index = randint(0, len(dr_names_options)-1)
                dr_last_name_index = randint(0, len(dr_last_names_options)-1)

                # Define the actual dr's name and last name
                dr_full_name = f'{dr_names_options[dr_names_index]} {dr_last_names_options[dr_last_name_index]}'        

                # Save dr's selection
                self.treating_dr = dr_full_name

            
            # Change the stage depending on if a Doctor has already been selected
            self.conversation_stage = 'appointment_time' if self.treating_dr else 'doctor_speciality'

            # Log the stage change
            logger.info(f"\nStage chaged to: {self.conversation_stage}\n")


            # Direct the next step depending on if the patient want to select a new doctor or they don't
            if self.conversation_stage == 'appointment_time':

                # First, confirm the name of the current treating doctor
                self.send_message(f'''Ok, it's confirmed that Dr. {self.treating_dr} will check your {self.patient_ailment}''')

                # Next, Define the day and the time of the appointment randomly
                #   Generate day and time options. 
                time_options = self.time_pool
                day_options = self.weekday_pool

                #   Generate seeds to randomly generate 2 different options for day and time for the appointment
                time_op1, time_op2, = sample(time_options, 2)
                day_op1, day_op2 = sample(day_options, 2)

                #   Define the actual 2 options of day/time for the user to choose
                day_and_time_op_1 = f'{day_op1} {time_op1}'
                day_and_time_op_2 = f'{day_op2} {time_op2}'

                # And finally, Define the message to lead to the next stage
                new_message = f'''Currently Dr. {self.treating_dr} has the following time availability:

1. {day_and_time_op_1}
2. {day_and_time_op_2}

Which one would fit best for you?'''
                
                # Send the message
                self.send_message(new_message)

                # Define the last message for if it's needed to be reminded to the user if in the next stage it fails the reply cheking
                self.conversation_input['last_message'] = new_message

                # Define the replying options for the next stage checking
                self.conversation_input['replying_options'] = [day_and_time_op_1, day_and_time_op_2, '1', '2']

            else:

                # Create a message confirming that a new doctor will be selected
                new_message = f'''No problem, in that case we will now select a new doctor for you'''
                    
                # Send the message
                self.send_message(new_message)

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
                new_message = f'''We currently count with this {self.dr_speciality} that can check on your {self.patient_ailment}:

    1. {dr_op_1}
    2. {dr_op_2}
    3. {dr_op_3}

    Which {self.dr_speciality[:-1]} would you like be attended by?'''
            
                # Send the message
                self.send_message(new_message)

                # Define the last message for if it's needed to be reminded to the user if in the next stage it fails the reply cheking
                self.conversation_input['last_message'] = new_message

                # Define the replying options for the next stage checking
                self.conversation_input['replying_options'] = [dr_op_1.lower(), dr_op_2.lower(), dr_op_3.lower(), '1', '2', '3']

    #   3.1. Doctor Speciality / 'doctor_speciality'
    def doctor_speciality(self) -> None:
        
        '''This function will guide the user to select a new treating doctor during the conversation'''

        # if the conversation already offered doctors options, check the user's reply is within expected
        if self.check_reply():            

            # Convert the user's choice into the actual dr's full name
            if self.conversation_input['user_response'] in '123':

                if self.conversation_input['user_response'] == '1':
                    dr_chosen = self.conversation_input['replying_options'][0]
                
                elif self.conversation_input['user_response'] == '2':
                    dr_chosen = self.conversation_input['replying_options'][1]
                
                else:
                    dr_chosen = self.conversation_input['replying_options'][2]
            

            # Save the user's chosen doctor
            self.treating_dr = dr_chosen.title()
            
            # Confirm to the user the name of the current treating doctor
            self.send_message(f'''Ok, it's confirmed that Dr. {self.treating_dr} will check your {self.patient_ailment}''')

            # Move on to the next stage
            self.conversation_stage = 'appointment_time'

            # Log the stage change
            logger.info(f"\nStage chaged to: {self.conversation_stage}\n")

            # Next, Define the day and the time of the appointment randomly
            #   Generate day and time options. 
            time_options = self.time_pool
            day_options = self.weekday_pool

            #   Generate seeds to randomly generate 2 different options for day and time for the appointment
            time_op1, time_op2, = sample(time_options, 2)
            day_op1, day_op2 = sample(day_options, 2)

            #   Define the actual 2 options of day/time for the user to choose
            day_and_time_op_1 = f'{day_op1} {time_op1}'
            day_and_time_op_2 = f'{day_op2} {time_op2}'

            # And finally, create the message for the user to confirm their input and leading to the next stage
            new_message = f'''Currently Dr. {self.treating_dr} has the following time availability:
    
1. {day_and_time_op_1}
2. {day_and_time_op_2}

Which one would fit best for you?'''
            
            # Send the message
            self.send_message(new_message)

            # Define the last message for if it's needed to be reminded to the user if in the next stage it fails the reply cheking
            self.conversation_input['last_message'] = new_message

            # Define the replying options for the next stage checking
            self.conversation_input['replying_options'] = [day_and_time_op_1, day_and_time_op_2, '1', '2']

    #   4. Appointment Day and Time Setting / 'appointment_time'
    def appointment_time_booking(self) -> None:

        # Check the user's reply is within expected        
        if self.check_reply(): 
                
            # Convert the user's choice into the actual dr's full name
            if self.conversation_input['user_response'] in '12':

                if self.conversation_input['user_response'] == '1':
                    self.appointment_day_and_time = self.conversation_input['replying_options'][0]
                
                else:
                    self.appointment_day_and_time = self.conversation_input['replying_options'][1]        
            
            # Confirm to the user the day and time of the appointment.
            self.send_message(f'''Ok! the appointment with Dr. {self.treating_dr} to check on your {self.patient_ailment} is booked for next *{self.appointment_day_and_time}*''')

            # Move on to the next stage
            self.conversation_stage = 'appointment_type'

            # Log the stage change
            logger.info(f"\nStage chaged to: {self.conversation_stage}\n")

            # Create the message for the user to confirm their input and leading to the next stage
            new_message = f'''Would you rather having your medical appointment with Dr. {self.treating_dr} presentially or virtually?

1. Presentially
2. Virtually'''
            
            # Send the message
            self.send_message(new_message)

            # Define the last message for if it's needed to be reminded to the user if in the next stage it fails the reply cheking
            self.conversation_input['last_message'] = new_message

            # Define the replying options for the next stage checking
            self.conversation_input['replying_options'] = ['presentially', 'virtually', '1', '2']

    #   5. Appointment type setting / 'appointment_type'
    def select_appointment_type(self) -> None:

        # Check the user's reply is within expected        
        if self.check_reply(): 

            # Save patient's appointment type
            #   If the user's response is a number
            if self.conversation_input['user_response'] in '12':

                if self.conversation_input['user_response'] == '1':
                    self.appointment_type = 'presentially'
                
                else:
                    self.appointment_type = 'virtually'

            else:   
                self.appointment_type = self.conversation_input['user_response']


            # Confirm to the user the type of the appointment.
            self.send_message(f'''Ok! your appointment will be attended *{self.appointment_type}*''')

            # Move on to the next stage
            self.conversation_stage = 'completed'

            # Log the stage change
            logger.info(f"\nStage chaged to: {self.conversation_stage}\n")


            # Configure the closing message according to the appointment type selected
            if self.appointment_type == 'presentially':

                # Generte a seed to randomly choose a medical center
                med_center_index = randint(0, len(self.med_cent_pool)-1)

                # Set the appointment location
                self.appointment_location = self.med_cent_pool[med_center_index]

                # Generate the closing message
                new_message = f'''Alright! The medical appointment for the patient *{self.patient_name}*, identified with ID #{self.patient_id} was booked with the {self.dr_speciality[:-1]} *Dr. {self.treating_dr}* at *{self.appointment_location}* next *{self.appointment_day_and_time}* to check patient's *{self.patient_ailment}*.

*Please remember to be present at reception 15 minutes prior to your appointment with your valid ID.*

Thank you for contacting St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹 '''

            else:

                # Generate the closing message
                new_message = f'''Alright! The medical appointment for the patient *{self.patient_name}*, identified with ID #{self.patient_id} was booked with the {self.dr_speciality[:-1]} with *Dr. {self.treating_dr}* virtually for the next *{self.appointment_day_and_time}* to check patient's *{self.patient_ailment}*.

*Please remember be online 10 minutes prior to the appointment and also be sure to have a stable connection, access to a webcam and microphone to make sure the appointment will happen without inconvenience.*

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹'''


            # Confirm the summary of the query to the user
            self.send_message(new_message)














