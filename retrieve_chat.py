import os
import zipfile
import argparse
from db import DBClient
from utils import format_date
from s3 import S3Client

def main():
    parser = argparse.ArgumentParser(description="Fetch messages from DB and store them in ZIP files.")
    parser.add_argument("chatroom_id", type=int, help="The chatroom ID for which to create the ZIP files.")
    args = parser.parse_args()
    
    db_client = DBClient()
    s3_client = S3Client()
    messages = db_client.retrieve_messages(args.chatroom_id)

    # Check if there aren't any messages in DB
    if not len(messages):
        print("No messages available to pull.")
        return

    # Create temporary directory for text files
    temp_dir = 'temp_text_files'
    os.makedirs(temp_dir, exist_ok=True)

    txt_count = 0
    messages_count = 0
    txt_filename = f'{txt_count}.txt'
    txt_path = os.path.join(temp_dir, txt_filename)
    zip_name = f'chatroom_{args.chatroom_id}.zip'
    zip_path = os.path.join(temp_dir, zip_name)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        txtf = open(txt_path, 'w')
        
        for message in messages:
            _, chatroom_id, sender, receiver, message_text, attachment_urls, timestamp = message
            txtf.write(f"{format_date(timestamp)}\n{sender} to {receiver}: {message_text}\n")
            if attachment_urls:
                txtf.write(f"Attachments:\n")
                for url in attachment_urls:
                    txtf.write(f"{url}\n")
            
            txtf.write(f"\n")
            messages_count += 1

            # Create a new text file after processing 100 messages
            if messages_count % 100 == 0:
                txtf.close()
                zipf.write(txt_path, arcname=txt_filename)
                os.remove(txt_path)
                txt_count += 1
                txt_filename = f'{txt_count}.txt'
                txt_path = os.path.join(temp_dir, txt_filename)
                txtf = open(txt_path, 'w')
        
        # Write the last text file to the ZIP file
        if messages_count % 100 != 0:
            txtf.close()
            zipf.write(txt_path, arcname=txt_filename)
            os.remove(txt_path)

    # Upload the ZIP file to S3
    s3_url = s3_client.upload_to_s3(zip_name, zip_path)

    # Clean up temporary directory and zip file
    os.remove(zip_path)
    os.rmdir(temp_dir)
    print(f"{len(messages)} messages exported to {s3_url}")

if __name__ == "__main__":
    main()
