# Third-party imports
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

        # Log the message received  
        logger.info(f"\n\nMessage received: {Body}\n") 

        # Message guard
        if not Body:
            raise HTTPException(status_code=400, detail="No message body found")

        if not From:
            raise HTTPException(status_code=400, detail="No sender number found")

                
        # Check if there's an ongoing conversation for DB storing
        ongoing_conversation = db.query(models.Conversation).filter(
            models.Conversation.user_id == From, 
            models.Conversation.end_time == None
        ).first()

        # If the 'ongoing_conversation' variable does not exist it means there are no open conversation 
        if not ongoing_conversation:

            # Create a new conversation
            conversation_id = database.create_conversation(db, user_id=From)

            # Log that a new conversation is added to the DB 
            logger.info(f"\n\nNew conversation added to the DB with a new conversation ID: {conversation_id}\n") 
            

        else:
            conversation_id = ongoing_conversation.id

        # Store the received message
        database.add_message(db, conversation_id, sender=From, message=Body)

        # Log that the message receive was added to the message table with a conversation id 
        logger.info(f"\n\nReceived message added to the conversation #{conversation_id}\n")
        

        # Set the conversations variables for the chatbot handler
        chatbot_handler.user_number = From
        chatbot_handler.conversation_id = conversation_id
        chatbot_handler.database = db

        # Process the incomming message
        chatbot_handler.conversation_input['user_response'] = Body.lower()        
        chatbot_handler.process_message()

        # Return the response for logging purposes
        return {"Conversation Stage": chatbot_handler.conversation_stage, "Message Received": Body}


    except Exception as e:
        
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")