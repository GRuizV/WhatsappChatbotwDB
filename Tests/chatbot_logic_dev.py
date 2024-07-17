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

        self.conversation_input:dict = {
            'user_response':None,
            'last_response':None,
            'replying_options':None,
            'doctor_speciality': False
        }
        self.conversation_stage:str = '' # Stages are: '' / 'greeting' / 'symptoms' / 'previous_diagnosis' / 'select_doctor' -> opt:'doctor_speciality' / 'appointment_time' / 'appointment_type' / 'completed'
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




    # CHAT FUNCTIONS
    def process_message(self, message:str='') -> str:

        '''This function process the incoming message and directs the execution to its respective stage'''

        if self.conversation_stage == '':
            
            # Greeting Message
            greeting_message = f'''Hi there! 👋

🧑‍⚕️​ Welcome to St. John's Health Group Virtual Assistant.✝️​⛪​ 

I'm here to help you with any questions or issues you might have regarding your health. 

Before we move on, could you please provide your ID followed by your full name so I can address your request properly?

Please reply as follows: *ID's Number*, *Patient's Full Name*'''
            
            # Send the greeting message
            self.conversation_input['user_response'] = input(greeting_message)
            self.conversation_stage = 'greeting' # Change the stage to when the user responds it goes to the handle_greeting func

        
        elif self.conversation_stage == 'greeting':
            user_response, last_message, replying_options = self.handle_greeting(user_response=self.conversation_input['user_response'])
            self.conversation_input['user_response'] = user_response
            self.conversation_input['last_message'] = last_message
            self.conversation_input['replying_options'] = replying_options

            

        elif self.conversation_stage == 'symptoms':
            user_response, last_message, replying_options = self.handle_symptoms(user_response=self.conversation_input['user_response'], last_message=self.conversation_input['last_message'], replying_options=self.conversation_input['replying_options'])
            self.conversation_input['user_response'] = user_response
            self.conversation_input['last_message'] = last_message
            self.conversation_input['replying_options'] = replying_options


        elif self.conversation_stage == 'previous_diagnosis':
            user_response, last_message, replying_options = self.previous_diagnosis(user_response=self.conversation_input['user_response'], last_message=self.conversation_input['last_message'], replying_options=self.conversation_input['replying_options'])
            self.conversation_input['user_response'] = user_response
            self.conversation_input['last_message'] = last_message
            self.conversation_input['replying_options'] = replying_options


        elif self.conversation_stage == 'select_doctor':
            user_response, last_message, replying_options = self.select_doctor(user_response=self.conversation_input['user_response'], last_message=self.conversation_input['last_message'], replying_options=self.conversation_input['replying_options'])
            self.conversation_input['user_response'] = user_response
            self.conversation_input['last_message'] = last_message
            self.conversation_input['replying_options'] = replying_options
            

        elif self.conversation_stage == 'doctor_speciality':
            user_response, last_message, replying_options = self.doctor_speciality(user_response=self.conversation_input['user_response'], last_message=self.conversation_input['last_message'], replying_options=self.conversation_input['replying_options'])
            self.conversation_input['user_response'] = user_response
            self.conversation_input['last_message'] = last_message
            self.conversation_input['replying_options'] = replying_options

       
        elif self.conversation_stage == 'appointment_time':
            user_response, last_message, replying_options = self.appointment_time_booking(user_response=self.conversation_input['user_response'], last_message=self.conversation_input['last_message'], replying_options=self.conversation_input['replying_options'])
            self.conversation_input['user_response'] = user_response
            self.conversation_input['last_message'] = last_message
            self.conversation_input['replying_options'] = replying_options

       
        elif self.conversation_stage == 'appointment_type':
            self.select_appointment_type(user_response=self.conversation_input['user_response'], last_message=self.conversation_input['last_message'], replying_options=self.conversation_input['replying_options'])      
            x = 0

        return f'''current stage: {self.conversation_stage}'''
        









        

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
        user_response = input(body_text)

        return user_response
    
    def check_reply(self, user_response:str, last_message:str, reply_options:list[str]) -> str:

        '''This function validates that the user's response are within expected.'''
        
        # Check for early exit
        if user_response.lower() == 'exit':
            return self.early_exit() # Early exit the conversation

        # Check if the user's response is within expected
        if user_response.lower() in reply_options:
            return user_response.lower()                     
        
        # Define the Non-complying user's reply
        non_complying_reply = f'''Sorry! I didn't understand that. Could you please answer with the options provided?'''

        # Send the Non-complying user's reply
        self.send_message(non_complying_reply)

        # FOR THE INTEGRATED VERSION: Send again the last message to the user to refresh the options provided                 
        response = input(last_message)

        return response.lower()

    def early_exit(self) -> None:

        '''
        This function Finishes the chat with the user if it's detected that the user intents to close the chat.

            - This must include an early closing message sent to the customer and the DB closing.           
        '''
        
        early_closing_message = f'''Alright! I will close this query now.

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹'''
        
        return self.send_message(early_closing_message)



    # CHAT STAGES / 'stage_name'

    #   1. Greeting / 'geeting'
    def handle_greeting(self, user_response:str) -> tuple[str]:      

        # Check if the user's answer is valid
        while True:

            if user_response.count(',') == 1:
                break

            print(f'''\nSorry, I didn't understand that. Let's try again!\n''')

            user_response = input(f'''Could you please provide your ID followed by your full name so I can address your request properly?

Please reply as follows: *ID's Number*, *Patient's Full Name''')

        #   Process the patient response to the greeting
        self.patient_id, self.patient_name = [' '.join(elem.strip().split()).lower().title() for elem in user_response.split(',')]

        # Move on to the next stage
        self.conversation_stage = 'symptoms'

        # Prompt the user confirming their input and leading to the next stage
        new_message = f'''Alright, {self.patient_name}, thanks for reaching out. 😊​
Now, Let's start checking on your symptoms.
                          
⚠️ Note: You can end this chat any time by replying with 'exit' and your query will be closed
                          
Could you please describe your symptoms with the following options?

1. General Discomfort
2. Respiratory Difficulties
3. Gastrointestinal Issues
4. Joint/Muscular Discomfort
5. Other Health Issues'''
        
        # Send the message & capture response
        user_response = self.send_message(new_message)

        # Define the Last Message if is needed to be reminded to the user
        last_message = f'''Could you please describe your symptoms with the following options?

1. General Discomfort
2. Respiratory Difficulties
3. Gastrointestinal Issues
4. Joint/Muscular Discomfort
5. Other Health Issues'''

        # Define the replying options for the next stage checking
        replying_options = ['general discomfort', 'respiratory difficulties', 'gastrointestinal issues', 'joint/muscular discomfort', 'other health issues', '1', '2', '3', '4', '5']

        # The las message is returned in case is needed to be re sended to clarify options for the user
        return user_response, last_message, replying_options


    #   2. Symptoms Handling / 'symptoms'
    def handle_symptoms(self, user_response:str, last_message:str, replying_options:list[str]) -> tuple[str]:

        # Check the user's reply is within expected
        while user_response not in replying_options:
            
            user_response = self.check_reply(user_response, last_message, replying_options)

            # If early exit occurred
            if not user_response:

                # Change the stage to completed
                self.conversation_stage = 'completed'

                # Return in the same format expected to not break the chat logic
                return None, None, None
     

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


        # Move on to the next stage
        self.conversation_stage = 'previous_diagnosis'

        #   Prompt the user confirming their input and leading to the next stage
        new_message = f'''Do you have a previous diagnosis for your current {self.patient_discomfort}? (Yes/No)'''
        
        # Send the message & capture response
        user_response = self.send_message(new_message)

        # Define the Last Message if is needed to be reminded to the user
        last_message = new_message

        # Define the replying options for the next stage checking
        replying_options = ['yes', 'no']

        # The las message is returned in case is needed to be re sended to clarify options for the user
        return user_response, last_message, replying_options


    #   2.1. Pre-Existence Handling / 'previous_diagnosis'
    def previous_diagnosis(self, user_response:str, last_message:str, replying_options:list[str]) -> tuple[str]:
        
        # Check the user's reply is within expected
        while user_response not in replying_options:
            
            user_response = self.check_reply(user_response, last_message, replying_options)

            # If early exit occurred
            if not user_response:

                # Change the stage to completed
                self.conversation_stage = 'completed'

                # Return in the same format expected to not break the chat logic
                return None, None, None


        # Generating a pre-existing ailment
        if user_response.lower() == 'yes':

            # pre_existences_pool dict Class var, in 'patient_discomfort' instance var. 
            pre_existing_ailments = self.pre_existences_pool[self.patient_discomfort]

            # Generate a random index to have a pre-existing ailment
            ailment_index = randint(0, len(pre_existing_ailments)-1)  

            # Save the randomly generated patient pre-existence
            self.patient_pre_existence = pre_existing_ailments[ailment_index]

        # Set the patient's ailment
        self.patient_ailment = self.patient_pre_existence if self.patient_pre_existence else self.patient_discomfort


        # Move on to the next stage
        self.conversation_stage = 'select_doctor'

        # Prompt the user confirming their input and leading to the next stage
        new_message = f'''Would you like your current treating doctor to review your {self.patient_ailment}? (Yes/No)'''
        
        # Send the message & capture response
        user_response = self.send_message(new_message)

        # Define the Last Message if is needed to be reminded to the user
        last_message = new_message

        # Define the replying options for the next stage checking
        replying_options = ['yes', 'no']

        # The las message is returned in case is needed to be re sended to clarify options for the user
        return user_response, last_message, replying_options


    #   3. Treating doctor: Doctor Selecting / 'select_doctor'
    def select_doctor(self, user_response:str, last_message:str, replying_options:list[str]) -> tuple[str]:

    
        # Check the user's reply is within expected
        while user_response not in replying_options:
            
            user_response = self.check_reply(user_response, last_message, replying_options)

            # If early exit occurred
            if not user_response:

                # Change the stage to completed
                self.conversation_stage = 'completed'

                # Return in the same format expected to not break the chat logic
                return None, None, None


        # Generate a doctor's speciality based on patient discomfort
        self.dr_speciality = self.drs_specialities_pool[self.patient_discomfort]


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

            # Save dr's selection
            self.treating_dr = user_response


        
        # Change the stage depending on if a Doctor has already been selected
        self.conversation_stage = 'appointment_time' if self.treating_dr else 'doctor_speciality'


        # Direct the next step depending on if the patient want to select a new doctor or they don't
        if self.conversation_stage == 'appointment_time':


            # First, confirm the the name of the current treating doctor
            self.send_message(f'''Ok, it's confirmed that Dr. {self.treating_dr} will now be attending you''')


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
            
            # Send the message & capture response
            user_response = self.send_message(new_message)

            # Define the Last Message if is needed to be reminded to the user
            last_message = new_message

            # Define the replying options for the next stage checking
            replying_options = [day_and_time_op_1, day_and_time_op_2, '1', '2']

            # The las message is returned in case is needed to be re sended to clarify options for the user
            return user_response, last_message, replying_options
        

        else:   

            # Create the message leading to the next stage
            new_message = f'''No problem, in that case we will now select a new doctor for you'''
            
            # Send the message
            self.send_message(new_message)

            # Return None to no break the return structure in the process_message function
            return None, None, None


    #   3.1. Doctor Speciality / 'doctor_speciality'
    def doctor_speciality(self, user_response:str, last_message:str, replying_options:list[str]) -> tuple[str]:
        
        '''This function will guide the user to select a new treating doctor during the conversation

            - The 'self.conversation_input['doctor_speciality']' parameter is changed to check if the conversation already offered a doctor option and 
                the usear already picked one.
        '''
        
        # If the conversation hasn't passed over this part
        if not self.conversation_input['doctor_speciality']:
            
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
        
            # Send the message & capture response
            user_response = self.send_message(new_message)

            # Define the Last Message if is needed to be reminded to the user
            last_message = new_message

            # Define the replying options for the next stage checking
            replying_options = [dr_op_1.lower(), dr_op_2.lower(), dr_op_3.lower(), '1', '2', '3']

            # Change the 'doctor_speciality' parameter in the conversation_input instance variable to True
            self.conversation_input['doctor_speciality'] = True

            # The las message is returned in case is needed to be re sended to clarify options for the user
            return user_response, last_message, replying_options



        # if the conversation already offered doctors options, check the user's reply is within expected
        while user_response not in replying_options:
            
            user_response = self.check_reply(user_response, last_message, replying_options)

            # If early exit occurred
            if not user_response:
                
                # Change the stage to completed
                self.conversation_stage = 'completed'

                # Return in the same format expected to not break the chat logic
                return None, None, None
            

        # Convert the user's choice into the actual dr's full name
        if user_response in '123':

            if user_response == '1':
                user_response = replying_options[0]
            
            elif user_response == '2':
                user_response = replying_options[1]
            
            else:
                user_response = replying_options[2]
        

        # Save the user's choosen doctor
        self.treating_dr = user_response.title()
        
        # Prompt the user the name of the treating doctor
        self.send_message(f'''Ok, it's confirmed that Dr. {self.treating_dr} will now be attending you''')


        # Move on to the next stage
        self.conversation_stage = 'appointment_time'

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
        
        # Send the message & capture response
        user_response = self.send_message(new_message)

        # Define the Last Message if is needed to be reminded to the user
        last_message = new_message

        # Define the replying options for the next stage checking
        replying_options = [day_and_time_op_1, day_and_time_op_2, '1', '2']

        # The last message is returned in case is needed to be re sended to clarify options for the user
        return user_response, last_message, replying_options


    #   4. Appointment Day and Time Setting / 'appointment_time'
    def appointment_time_booking(self, user_response:str, last_message:str, replying_options:list[str]) -> tuple[str]:


        # Check the user's reply is within expected        
        while user_response not in replying_options:
            
            user_response = self.check_reply(user_response, last_message, replying_options)

            # If early exit occurred: This works for the integrated version
            if not user_response:

                # Change the stage to completed
                self.conversation_stage = 'completed'

                # Return in the same format expected to not break the chat logic
                return None, None, None
            

        # Convert the user's choice into the actual dr's full name
        if user_response in '12':

            if user_response == '1':
                self.appointment_day_and_time = replying_options[0]
            
            else:
                self.appointment_day_and_time = replying_options[1]        
        
        # Prompt the User the day and time of the appointment.
        self.send_message(f'''Ok! the appointment with Dr. {self.treating_dr} to check on your {self.patient_ailment.title()} is booked for next {self.appointment_day_and_time}''')


        # Move on to the next stage
        self.conversation_stage = 'appointment_type'

        #  create the message for the user to confirm their input and leading to the next stage
        new_message = f'''Would you rather having your medical appointment with Dr. {self.treating_dr} presentially or virtually?

1. Presentially
2. Virtually'''
        
        # Send the message & capture response
        user_response = self.send_message(new_message)    

        # Define the Last Message if is needed to be reminded to the user
        last_message = new_message

        # Define the replying options for the next stage checking
        replying_options = ['presentially', 'virtually', '1', '2']

        # The last message is returned in case is needed to be re sended to clarify options for the user
        return user_response, last_message, replying_options


    #   5. Appointment type setting / 'appointment_type'
    def select_appointment_type(self, user_response:str, last_message:str, replying_options:list[str]) -> None:


        # Check the user's reply is within expected
        while user_response not in replying_options:
            
            user_response = self.check_reply(user_response, last_message, replying_options)

            # If early exit occurred
            if not user_response:
                
                # Change the stage to completed
                self.conversation_stage = 'completed'

                # Return in the same format expected to not break the chat logic
                return None, None, None


        # Save patient's appointment type
        if user_response in '12':

            if user_response == '1':
                self.appointment_type = 'presentially'
            
            else:
                self.appointment_type = 'virtually'

        else:   
            self.appointment_type = user_response

        # Prompt the user the type of the appointment.
        self.send_message(f'''Ok! your appointment will be attended {self.appointment_type}''')


        # Move on to the next stage
        self.conversation_stage = 'completed'


        # Configure the closing message according to the appointment type selected
        if self.appointment_type == 'presentially':

            # Generte a seed to randomly choose a medical center
            med_center_index = randint(0, len(self.med_cent_pool)-1)

            # Set the appointment location
            self.appointment_location = self.med_cent_pool[med_center_index]

            # Generate the closing message
            new_message = f'''Alright! The medical appointment for the patient {self.patient_name}, identified with ID #{self.patient_id} was booked with the {self.dr_speciality[:-1]} Dr. {self.treating_dr} at {self.appointment_location} next {self.appointment_day_and_time} to check patient's {self.patient_ailment.title()}.

Please remember to be present at reception 15 minutes prior to your appointment with your valid ID.

Thank you for contacting St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹 '''


        else:

            # Generate the closing message
            new_message = f'''Alright! The medical appointment for the patient {self.patient_name}, identified with ID #{self.patient_id} was booked with the {self.dr_speciality[:-1]} with Dr. {self.treating_dr} virtually for the next {self.appointment_day_and_time} to check patient's {self.patient_ailment.title()}.

Please remember be online 10 minutes prior to the appointment and also be sure to have a stable connection, access to a webcam and microphone to make sure the appointment will happen without inconvenience.

Thank you for contacting out St. John's Health Group Virtual Assistance Service.✝️🧑‍⚕️
We value your preferrence for our services! 😊​
We hope you get better in no time ❤️‍🩹'''


        # Confirm the summary of the query to the user
        self.send_message(new_message)











# Example Usage

# Create a Handler that takes care of the chatbot ops
chatbot_session = MessageHandler()

# Save the User Number
chatbot_session.user_number = '3205503934'

# # Close the DB session 
# Write the code to close the DB session





'# Version 2'

'General Testing'
stage = ''

while 'completed' not in stage:

    stage = chatbot_session.process_message()

    print(stage)



'Testing the Stage 2: Symptoms'

# # Define input from previous stages
# chatbot_session.patient_id='1'
# chatbot_session.patient_name = 'G'

# # Defining the input for the stage
# chatbot_session.conversation_stage = 'symptoms'
# chatbot_session.conversation_input['user_response'] = f'''4'''
# chatbot_session.conversation_input['last_message'] = f'''Could you please describe your symptoms with the following options?

# 1. General Discomfort
# 2. Respiratory Difficulties
# 3. Gastrointestinal Issues
# 4. Joint/Muscular Discomfort
# 5. Other Health Issues'''
# chatbot_session.conversation_input['replying_options'] = ['general discomfort', 'respiratory difficulties', 'gastrointestinal issues', 'joint/muscular discomfort', 'other health issues', '1', '2', '3', '4', '5']

# # Running the Script
# chatbot_session.process_message()



'Testing the Stage 2.1: Pre-Existence'

# # Define input from previous stages
# chatbot_session.patient_id='1'
# chatbot_session.patient_name = 'G'
# chatbot_session.patient_discomfort = 'joint/muscular discomfort'

# # Define the input for the stage
# chatbot_session.conversation_stage = 'previous_diagnosis'
# chatbot_session.conversation_input['user_response'] = f'''dfgdf'''
# chatbot_session.conversation_input['last_message'] = f'''Do you have a previous diagnosis for your current {chatbot_session.patient_discomfort}? (Yes/No)'''
# chatbot_session.conversation_input['replying_options'] = ['yes', 'no']

# # Run the Script
# chatbot_session.process_message()



'Testing the Stage 3: Doctor Selecting'

# # Define input from previous stages
# chatbot_session.patient_id='1'
# chatbot_session.patient_name = 'G'
# chatbot_session.patient_discomfort = 'joint/muscular discomfort'
# chatbot_session.patient_pre_existence = 'Osteoarthritis'
# chatbot_session.patient_ailment = 'Osteoarthritis'

# # Define the input for the stage
# chatbot_session.conversation_stage = 'select_doctor'
# chatbot_session.conversation_input['user_response'] = f'''dfgdf'''
# chatbot_session.conversation_input['last_message'] = f'''Would you like your current treating doctor to review your {chatbot_session.patient_ailment}? (Yes/No)'''
# chatbot_session.conversation_input['replying_options'] = ['yes', 'no']

# # Run the Script
# chatbot_session.process_message()



'Testing the Stage 3.1: Doctor Speciality'

# # Define input from previous stages
# chatbot_session.patient_id='1'
# chatbot_session.patient_name = 'G'
# chatbot_session.patient_discomfort = 'joint/muscular discomfort'
# chatbot_session.patient_pre_existence = 'Osteoarthritis'
# chatbot_session.patient_ailment = 'Osteoarthritis'

# # Define the input for the stage
# chatbot_session.conversation_stage = 'doctor_speciality'
# chatbot_session.conversation_input['user_response'] = f'''dfgdf'''
# chatbot_session.conversation_input['last_message'] = f'''Ok, it's confirmed that Dr. Susan Miller will now be attending you
# Currently Dr. Susan Miller has the following time availability:
# 1. Monday 8:15 AM
# 2. Wednesday 1:00 PM'''
# chatbot_session.conversation_input['replying_options'] = ['1', '2']

# # Run the Script
# while True:
#     chatbot_session.process_message()

#     if chatbot_session.conversation_stage != 'doctor_speciality':
#         break
    
# x = 0



'Testing the Stage 4: Appointment Day and Time Setting'

# # Define input from previous stages
# chatbot_session.patient_id='1'
# chatbot_session.patient_name = 'G'
# chatbot_session.patient_discomfort = 'joint/muscular discomfort'
# chatbot_session.patient_pre_existence = 'Osteoarthritis'
# chatbot_session.patient_ailment = 'Osteoarthritis'
# chatbot_session.treating_dr = 'Susan Miller'

# # Define the input for the stage
# chatbot_session.conversation_stage = 'appointment_time'
# chatbot_session.conversation_input['user_response'] = f'''dfgd'''
# chatbot_session.conversation_input['last_message'] = f'''Currently Dr. Susan Miller has the following time availability:
# 1. Monday 8:15 AM
# 2. Wednesday 1:00 PM'''
# chatbot_session.conversation_input['replying_options'] = ['Monday 8:15 AM', 'Wednesday 1:00 PM', '1', '2']

# # Run the Script
# chatbot_session.process_message()



'Testing the Stage 5: Appointment type and closing'

# # Define input from previous stages
# chatbot_session.patient_id='1'
# chatbot_session.patient_name = 'G'
# chatbot_session.patient_discomfort = 'joint/muscular discomfort'
# chatbot_session.patient_pre_existence = 'Osteoarthritis'
# chatbot_session.patient_ailment = 'Osteoarthritis'
# chatbot_session.treating_dr = 'Susan Miller'
# chatbot_session.dr_speciality = 'Orthopedists'
# chatbot_session.appointment_day_and_time = 'Monday 8:15 AM'

# # Define the input for the stage
# chatbot_session.conversation_stage = 'appointment_type'
# chatbot_session.conversation_input['user_response'] = f'''dfgd'''
# chatbot_session.conversation_input['last_message'] = f'''Would you rather having your medical appointment with Dr. {chatbot_session.treating_dr} presentially or virtually?

# 1. Presentially
# 2. Virtually'''
# chatbot_session.conversation_input['replying_options'] = ['presentially', 'virtually', '1', '2']

# # Run the Script
# chatbot_session.process_message()





