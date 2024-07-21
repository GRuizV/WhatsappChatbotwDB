from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

# Internal imports
import utils, models, database
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the server app
app = FastAPI()

# Initialize the chatbot handler
chatbot_handler = utils.MessageHandler()



# "message" Endpoint definition
@app.post("/message")
async def reply(request: Request, db: Session = Depends(database.get_db)) -> dict:

    try:

        # Parse the form data from the request
        form_data = await request.form()
        Body = form_data.get('Body')
        From = form_data.get('From')

        logger.info(f"\n\nMessage received: {Body}\n") # Log the message received  

        # Message guard
        if not Body:
            raise HTTPException(status_code=400, detail="No message body found")

        if not From:
            raise HTTPException(status_code=400, detail="No sender number found")

        'DB Functionalities: For later on'
        # def db_functions():

        #     # Check if there's an ongoing conversation
        #     ongoing_conversation = db.query(models.Conversation).filter(
        #         models.Conversation.user_id == From, 
        #         models.Conversation.end_time == None
        #     ).first()

        #     if not ongoing_conversation:
        #         # Create a new conversation
        #         conversation_id = database.create_conversation(db, user_id=From)
        #     else:
        #         conversation_id = ongoing_conversation.id

        #     # Store the received message
        #     database.add_message(db, conversation_id, sender=From, message=Body)

        #     # Generate a response (this is where your chatbot logic will go)
        #     chat_response = utils.generate_response(Body)  # You will define this function

        #     # Store the response message
        #     database.add_message(db, conversation_id, sender="bot", message=chat_response)

        #     # Send the response back via Twilio
        #     utils.send_message(From, chat_response)

        #     # If the conversation is over, update the end_time (you can define your own logic to determine this)
        #     # For example, if the chat_response is a closing statement, you can end the conversation
        #     if Body.lower() in ["bye", "goodbye", "see you"]:
        #         database.end_conversation(db, conversation_id)

        # Set the user number in the chatbot handler
        chatbot_handler.user_number = From

        # Process the incomming message
        chatbot_handler.conversation_input['user_response'] = Body.lower()        
        chatbot_handler.process_message()

        # Return the response for logging purposes
        return {"message": chatbot_handler.conversation_stage}


    except Exception as e:
        utils.logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")