import os
import random
import argparse
import string
import psycopg2
from psycopg2 import sql

# List of random user names
user_pool = ["Alice", "Bob", "Charlie", "Dave", "Eve"]

# Static pool of attachments
attachment_pool = [
    "image1.jpg", "image2.png", "song1.mp3", "document1.pdf", "video1.mp4"
]

# PostgreSQL connection details
db_config = {
    'dbname': os.environ.get("DB_NAME", default="messenger_db"),
    'user': os.environ.get("DB_USERNAME", default="messenger_owner"),
    'password': os.environ.get("DB_PASSWORD", default="123"),
    'host': os.environ.get("DB_HOST", default="localhost"),
    'port': os.environ.get("DB_PORT", default="5432")
}

def connect_db():
    return psycopg2.connect(**db_config)

def generate_random_message():
    # Randomly decide whether to generate a message
    if random.random() < 0.8:  
        message_length = random.randint(10, 70)
        message = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=message_length))
        return message.strip()
    return None

def generate_random_attachment():
    # Randomly decide whether to include an attachment
    if random.random() < 0.2:
        return random.choice(attachment_pool)
    return None

def create_tables_if_not_exist(cursor):
    # Check if users table exists, create if not
    users_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE
        )
    """)
    cursor.execute(users_query)
    
    # Check if messages table exists, create if not
    messages_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            message TEXT,
            attachment VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    cursor.execute(messages_query)


def get_user_id(cursor, username):
    query = sql.SQL("SELECT user_id FROM users WHERE username = %s")
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        insert_query = sql.SQL("INSERT INTO users (username) VALUES (%s) RETURNING user_id")
        cursor.execute(insert_query, (username,))
        return cursor.fetchone()[0]

def insert_message(cursor, user_id, message, attachment):
    query = sql.SQL(
        "INSERT INTO messages (user_id, message, attachment) VALUES (%s, %s, %s)"
    )
    cursor.execute(query, (user_id, message, attachment))

def generate_chat_messages(num_messages):
    chat_history = []
    last_user = None

    for _ in range(num_messages):
        user = random.choice(user_pool)
        
        # Ensure the same user does not send two consecutive messages
        while user == last_user:
            user = random.choice(user_pool)
        
        last_user = user
        
        message = generate_random_message()
        attachment = generate_random_attachment()
        
        # Ensure there is at least a message or an attachment
        while not message and not attachment:
            message = generate_random_message()
            attachment = generate_random_attachment()
        
        chat_entry = {"user": user}
        if message:
            chat_entry["message"] = message
        if attachment:
            chat_entry["attachment"] = attachment
        
        chat_history.append(chat_entry)

    return chat_history

def main():
    parser = argparse.ArgumentParser(description="Generate N chat messages between random users.")
    parser.add_argument("N", type=int, help="The number of messages to generate.")
    args = parser.parse_args()
    
    num_messages = args.N
    chat_messages = generate_chat_messages(num_messages) 
    
    conn = connect_db()
    cursor = conn.cursor()

    # Create tables if they don't exist
    create_tables_if_not_exist(cursor)

    for msg in chat_messages:
        user_id = get_user_id(cursor, msg['user'])
        message = msg.get('message')
        attachment = msg.get('attachment')
        insert_message(cursor, user_id, message, attachment)
        
        if "message" in msg and "attachment" in msg:
            print(f"{msg['user']}: {msg['message']} [Attachment: {msg['attachment']}]")
        elif "message" in msg:
            print(f"{msg['user']}: {msg['message']}")
        elif "attachment" in msg:
            print(f"{msg['user']}: [Attachment: {msg['attachment']}]")
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
