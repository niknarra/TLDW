import os
from deta import Deta
import uuid

# Load environment variables
from dotenv import load_dotenv
load_dotenv(".env")

# Fetch the DETA_KEY for database connection
DETA_KEY = os.getenv("DETA_KEY")

# Initialize Deta with the key and connect to the chat database
deta = Deta(DETA_KEY)
chat_db = deta.Base("Chats")

def generate_unique_chat_id():
    return str(uuid.uuid4())

def insert_chat_message(video_id, user_id, user_message, bot_message):
    #chat_id = generate_unique_chat_id()  # Generate a unique chat ID
    return chat_db.put({"video_id": video_id, "user_id": user_id, "user_message": user_message, "bot_message": bot_message})

def fetch_chat_history(video_id, user_id):
    # Fetch all messages for a specific video and user
    res = chat_db.fetch({"video_id": video_id, "user_id": user_id})
    #print(res.items)
    #print({"video_id": video_id, "user_id": user_id})
    return res.items

def clear_chat_history(video_id,user_id):
    res = chat_db.fetch({"video_id": video_id, "user_id": user_id})
    chat_records = res.items

    # Loop through the fetched records and delete each one
    for record in chat_records:
        chat_db.delete(record["key"])


#insert_chat_message(2,1,"To be Deleted","TBD")
#clear_chat_history(2,1)
#print(fetch_chat_history(1,1))