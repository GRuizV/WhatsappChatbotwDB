
# Third-party imports
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.orm import Session

# Internal imports
import utils, models, database



app = FastAPI()


@app.post("/message")
async def reply(request: Request, db: Session = Depends(database.get_db)) -> dict:

    try:
        # Parse the form data from the request
        form_data = await request.form()
        Body = form_data.get('Body')
        From = form_data.get('From')

        if not Body:
            raise HTTPException(status_code=400, detail="No message body found")

        if not From:
            raise HTTPException(status_code=400, detail="No sender number found")


        # Check if there's an ongoing conversation
        ongoing_conversation = db.query(models.Conversation).filter(
            models.Conversation.user_id == From, 
            models.Conversation.end_time == None
        ).first()



        if not ongoing_conversation:
            # Create a new conversation
            conversation_id = database.create_conversation(db, user_id=From)
        else:
            conversation_id = ongoing_conversation.id



        # Store the received message
        database.add_message(db, conversation_id, sender=From, message=Body)

        # Generate a response (this is where your chatbot logic will go)
        chat_response = utils.generate_response(Body)  # You will define this function

        # Store the response message
        database.add_message(db, conversation_id, sender="bot", message=chat_response)

        # Send the response back via Twilio
        utils.send_message(From, chat_response)


        # If the conversation is over, update the end_time (you can define your own logic to determine this)
        # For example, if the chat_response is a closing statement, you can end the conversation
        if chat_response.lower() in ["bye", "goodbye", "see you"]:
            database.end_conversation(db, conversation_id)

        # Return the response for logging purposes
        return {"message": chat_response}


    except Exception as e:
        utils.logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    







