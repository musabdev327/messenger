import os
import random
import argparse
import string
from db import DBClient
from s3 import S3Client

# List of random user names
user_pool = ["Alice", "Bob", "Charlie", "Dave", "Eve"]

# Static pool of attachments
attachment_pool = [
    "image1.png", "image2.png"
]
# Can add more assets into the pool by adding them into the same directory
# and updating the above array

def generate_random_message():
    if random.random() < 0.8:  
        message_length = random.randint(10, 70)
        message = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=message_length))
        return message.strip()
    return None

def generate_random_attachments():
    if random.random() < 0.2:
        num_attachments = random.randint(1, len(attachment_pool))
        return random.sample(attachment_pool, num_attachments)
    return []

def generate_chat_messages(num_messages, num_users=None):
    active_pool = user_pool
    
    if num_users:
        if num_users > len(user_pool):
            raise ValueError("Number of users requested exceeds the available user pool.")
        if num_users < 2:
            raise ValueError("Number of users requested must two or more.")

        active_pool = random.sample(user_pool, num_users)

    chat_history = []
    chatroom_id = random.randint(1, 1000)

    for _ in range(num_messages):
        sender = random.choice(active_pool)
        receiver = random.choice(active_pool)

        while receiver == sender:
            receiver = random.choice(active_pool)

        message = generate_random_message()
        attachments = generate_random_attachments()
        
        while not message and not attachments:
            message = generate_random_message()
            attachments = generate_random_attachments()
        
        chat_entry = {"chatroom_id": chatroom_id, "sender": sender, "receiver": receiver}
        if message:
            chat_entry["message"] = message
        if attachments:
            chat_entry["attachments"] = attachments
        
        chat_history.append(chat_entry)

    return chat_history, chatroom_id

def main():
    parser = argparse.ArgumentParser(description="Generate N chat messages between random users.")
    parser.add_argument("N", type=int, help="The number of messages to generate.")
    parser.add_argument("--users", type=int, help="The number of users to generate messages between.")
    args = parser.parse_args()
    
    num_messages = args.N
    num_users = args.users if args.users else None
    chat_messages, chatroom_id = generate_chat_messages(num_messages, num_users) 
    
    db_client = DBClient()
    s3_client = S3Client()

    db_client.insert_chatroom(chatroom_id, f"Chatroom_{chatroom_id}")

    for msg in chat_messages:
        sender_id = db_client.get_user_id(msg['sender'])
        receiver_id = db_client.get_user_id(msg['receiver'])
        message = msg.get('message')
        attachment_urls = None
        if 'attachments' in msg:
            attachments = msg['attachments']
            attachment_urls = []
            for attachment in attachments:
                attachment_path = os.path.join('attachments', attachment)
                attachment_url = s3_client.upload_to_s3(f"attachment-{attachment}", attachment_path)
                attachment_urls.append(attachment_url)
        
        db_client.insert_message(msg['chatroom_id'], sender_id, receiver_id, message, attachment_urls)
        
        if message and attachment_urls:
            print(f"{msg['sender']}-to-{msg['receiver']}: {message} \n[Attachments: {', '.join(attachment_urls)}]")
        elif message:
            print(f"{msg['sender']}-to-{msg['receiver']}: {message}")
        elif attachment_urls:
            print(f"{msg['sender']}-to-{msg['receiver']}: [Attachments: {', '.join(attachment_urls)}]")
        print("\n")
    db_client.close()

    print(f"Chatroom ID: {chatroom_id}")

if __name__ == "__main__":
    main()
