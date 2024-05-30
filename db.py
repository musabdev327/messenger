import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv() 

# PostgreSQL connection details
db_config = {
    'dbname': os.environ.get("DB_NAME", default="messenger_db"),
    'user': os.environ.get("DB_USERNAME", default="messenger_owner"),
    'password': os.environ.get("DB_PASSWORD", default="123"),
    'host': os.environ.get("DB_HOST", default="localhost"),
    'port': os.environ.get("DB_PORT", default="5432")
}


class DBClient:
    def __init__(self):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.create_tables_if_not_exist()

    def create_tables_if_not_exist(self):
        # Create users table if not exists
        users_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE
            )
        """)
        self.cursor.execute(users_query)
        
        # Create chatrooms table if not exists
        chatrooms_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS chatrooms (
                chatroom_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE
            )
        """)
        self.cursor.execute(chatrooms_query)
        
        # Create messages table if not exists
        messages_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id SERIAL PRIMARY KEY,
                chatroom_id INTEGER NOT NULL,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message TEXT,
                attachment_urls TEXT[],
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chatroom_id) REFERENCES chatrooms(chatroom_id),
                FOREIGN KEY (sender_id) REFERENCES users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES users(user_id)
            )
        """)
        self.cursor.execute(messages_query)
        self.conn.commit()

    def insert_chatroom(self, chatroom_id, name):
        query = sql.SQL(
            "INSERT INTO chatrooms (chatroom_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        )
        self.cursor.execute(query, (chatroom_id, name))
        self.conn.commit()

    def insert_message(self, chatroom_id, sender_id, receiver_id, message, attachment_urls):
        query = sql.SQL(
            "INSERT INTO messages (chatroom_id, sender_id, receiver_id, message, attachment_urls) VALUES (%s, %s, %s, %s, %s)"
        )
        self.cursor.execute(query, (chatroom_id, sender_id, receiver_id, message, attachment_urls))
        self.conn.commit()

    def get_user_id(self, name):
        query = sql.SQL("SELECT user_id FROM users WHERE name = %s")
        self.cursor.execute(query, (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        self.cursor.execute(sql.SQL("INSERT INTO users (name) VALUES (%s) RETURNING user_id"), (name,))
        self.conn.commit()
        return self.cursor.fetchone()[0]

    def retrieve_messages(self, chatroom_id):
        retrieve_messages_query = sql.SQL("""
            SELECT m.message_id, m.chatroom_id, u1.name as sender, u2.name as receiver, m.message, m.attachment_urls, m.timestamp
            FROM messages m
            JOIN users u1 ON m.sender_id = u1.user_id
            JOIN users u2 ON m.receiver_id = u2.user_id
            WHERE m.chatroom_id = %s
            ORDER BY m.message_id ASC
        """)
        self.cursor.execute(retrieve_messages_query, (chatroom_id,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
