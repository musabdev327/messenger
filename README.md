
# Chat Message Generator

This Python script generates random chat messages between random users and stores them in a PostgreSQL database. It also allows retrieving messages from a specific chatroom and exporting them as CSV files in a ZIP archive uploaded to an S3 bucket.

## Prerequisites

Before running the script, ensure you have the following installed:

-   Python 3.x

## Setup


1.  **Virtual Environment Setup**:

-   Create a virtual environment using the following command:
    
    ```bash
    python -m venv env
    ```

2.  **Activate Virtual Environment**:

-   Create a virtual environment using the following command:
    
    ```bash
    source venv/bin/activate
    ```
    
3.  **Install Dependencies**:

-   Install required packages using the provided `requirements.txt` file:
    
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables**:

Create a `.env` file in the root directory of your project and set the following variables with your configuration details:

```bash
DB_NAME=your_db_name
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
AWS_S3_BUCKET_NAME=your_s3_bucket_name
AWS_REGION=your_aws_region
AWS_ACCESS_PUBLIC_KEY=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key` 
```

## Usage

### Generating Chat Messages

1.  Open a terminal or command prompt.
2.  Navigate to the directory containing the `generate_chat.py` file.
3.  Run the script with the following command:
    
    ```bash
    python generate_chat.py N
    ``` 
    
    Replace `N` with the number of chat messages you want to generate. Optionally, you can specify the number of users with `--users`:
    
    ```bash
    python generate_chat.py N --users M
    ```
    
    Replace `M` with the number of users to generate messages between.

### Explanation

The script uses a pool of predefined user names and attachment files to simulate real chat interactions. It randomly selects users as senders and receivers, generates random message content, and occasionally includes attachments.

-   **User Pool**: A list of user names (`user_pool`) that will participate in the chat messages.
-   **Attachment Pool**: A list of predefined attachment file names (`attachment_pool`) that can be included in the messages.
-   **Random Message Generation**: The `generate_random_message` function creates random strings of text to simulate chat messages.
-   **Random Attachment Generation**: The `generate_random_attachment` function randomly selects attachment files to be included in some messages.
-   **Chat Message Generation**: The `generate_chat_messages` function creates a specified number of messages with random senders, receivers, and content, and stores them in the database.

### Retrieving Messages from a Chatroom

1.  Open a terminal or command prompt.
2.  Navigate to the directory containing the `retrieve_chat.py` file.
3.  Run the script with the following command:
    
    ```bash
    python retrieve_chat.py CHATROOM_ID 
    ```
    Replace `CHATROOM_ID` with the ID of the chatroom whose messages you want to retrieve.

### Explanation

-   The messages are fetched from the PostgreSQL database based on the provided `CHATROOM_ID`.
-   Messages are written to CSV files, with each file containing up to 100 messages.
-   The CSV files are compressed into a single ZIP file.
-   The ZIP file is uploaded to the specified S3 bucket, and a link to the file is printed.

### Example Commands

-   Generate 100 chat messages between random users:
    
    ```bash
    python generate_chat.py 100
    ```

-   Generate 50 chat messages between 3 specific users:
    
    ```bash
    python generate_chat.py 50 --users 3
    ```
    
-   Retrieve messages from chatroom with ID 1:
    
    ```bash
    python retrieve_chat.py 1
    ```

### DB SCHEMA
![alt text](https://messenger-client-assets.s3.us-west-1.amazonaws.com/image.png)

## Example Output

After running the retrieval script, a ZIP file containing csv files (each with up to 100 messages) will be created and uploaded to the specified S3 bucket. The script will print the URL of the uploaded ZIP file.