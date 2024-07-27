# St. John's Health Group Virtual Assistant

This project is a WhatsApp chatbot built using FastAPI and PostgreSQL. The chatbot assists users with their health-related queries, guiding them through a series of questions to provide relevant information or redirect them to the appropriate healthcare professional. It stores conversation logs in a PostgreSQL database.

## Features

- **Interactive Chatbot**: Engages users in a guided conversation to gather relevant health information.
- **Twilio Integration**: Utilizes Twilio's API for WhatsApp messaging.
- **Session Tracking**: Tracks user conversations and stores them in a PostgreSQL database.
- **Emoji Support**: Includes support for emojis in responses (with some limitations).
- **Extensible Architecture**: Designed to easily add new features and functionalities.

## Requirements

- Python 3.8+
- PostgreSQL
- Twilio Account
- FastAPI
- SQLAlchemy
- Decouple

### Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Create and Activate a Virtual Environment**:

    ```bash
    python -m venv whatsapp_chatbot_env
    source whatsapp_chatbot_env/bin/activate  # On Windows use `whatsapp_chatbot_env\Scripts\activate`

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt

4. **Configure Environment Variables**:

    Create a .env file in the project root directory.

    Add the following variables:

    ```plaintext
    DB_USER=<your_db_user>
    DB_PASSWORD=<your_db_password>
    DB_NAME=<your_db_name>
    TWILIO_ID=<your_twilio_id>
    TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
    TWILIO_NUMBER=<your_twilio_number>
    
5. **Set Up the Database**:

    - Make sure PostgreSQL is running and the database is created.
    - The necessary tables will be created automatically when the application starts.


## Running the Application

1. **Start the FastAPI Server**:

    ```bash
    uvicorn main:app --reload

2. **Expose Localhost to the Internet**:

    Use ngrok to expose your local server to the internet. This is necessary for Twilio to interact with your application.

    ```bash
    
    ngrok http 8000

3. **Set Up Twilio Webhook**:

    In your Twilio console, set the webhook URL to the ngrok URL provided, with the path /message.
    
    Usage: Once the server is running and the webhook is set up, you can interact with the chatbot via WhatsApp using the Twilio number.


## Project Structure

- **main.py**: The entry point of the FastAPI application.

- **utils.py**: Contains utility functions, including message handling and chatbot logic.

- **database.py**: Manages database connections and operations.

- **models.py**: Defines the database schema using SQLAlchemy.


## Contributions

Contributions are welcome! Please fork this repository and submit a pull request with your changes.



## License

This project is licensed under the MIT License.

_Feel free to adjust the content based on your specific implementation and requirements. Add more details or instructions as needed, especially in the sections on setting up environment variables, running the application, and any unique features your chatbot offers._