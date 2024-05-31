import os
import shutil
import zipfile
import argparse
import csv
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

    # Create temporary directory for CSV files
    temp_dir = 'temp_csv_files'
    os.makedirs(temp_dir, exist_ok=True)

    csv_count = 0
    messages_count = 0
    csv_filename = f'{csv_count}.csv'
    csv_path = os.path.join(temp_dir, csv_filename)
    zip_name = f'chatroom_{args.chatroom_id}.zip'
    zip_path = os.path.join(temp_dir, zip_name)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        csv_file = open(csv_path, 'w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Timestamp', 'Sender', 'Receiver', 'Message', 'Attachments'])

        for message in messages:
            _, chatroom_id, sender, receiver, message_text, attachment_urls, timestamp = message
            attachments = ', '.join(attachment_urls) if attachment_urls else ''
            csv_writer.writerow([format_date(timestamp), sender, receiver, message_text, attachments])
            
            messages_count += 1

            # Create a new CSV file after processing 100 messages
            if messages_count % 100 == 0:
                csv_file.close()
                zipf.write(csv_path, arcname=csv_filename)
                os.remove(csv_path)
                csv_count += 1
                csv_filename = f'{csv_count}.csv'
                csv_path = os.path.join(temp_dir, csv_filename)
                csv_file = open(csv_path, 'w', newline='')
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Timestamp', 'Sender', 'Receiver', 'Message', 'Attachments'])
        
        # Write the last CSV file to the ZIP file
        if messages_count % 100 != 0:
            csv_file.close()
            zipf.write(csv_path, arcname=csv_filename)
            os.remove(csv_path)

    # Upload the ZIP file to S3
    s3_url = s3_client.upload_to_s3(zip_name, zip_path)
    print(f"{len(messages)} messages exported to {s3_url}")

    # Clean up temporary directory and zip file
    try:
        os.remove(zip_path)
        shutil.rmtree(temp_dir)
    except Exception as exc:
        print("Error while removing temporary files")

if __name__ == "__main__":
    main()
