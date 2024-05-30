
# Chat Message Generator

This Python script generates random chat messages between random users and stores them in a PostgreSQL database.

## Prerequisites

Before running the script, ensure you have the following installed:

-   Python 3.x

## Setup


1.  **Virtual Environment Setup**:

-   Create a virtual environment using the following command:
    
    ```bash
    python -m venv env
    ```
    
2.  **Install Dependencies**:

-   Install required packages using the provided `requirements.txt` file:
    
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Environment Variables**:

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

### Retrieving Messages from a Chatroom

1.  Open a terminal or command prompt.
2.  Navigate to the directory containing the `retrieve_chat.py` file.
3.  Run the script with the following command:
    
    ```bash
    python retrieve_chat.py CHATROOM_ID 
    ```
    Replace `CHATROOM_ID` with the ID of the chatroom whose messages you want to retrieve.

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


## Example Output

After running the retrieval script, a ZIP file containing text files (each with up to 100 messages) will be created and uploaded to the specified S3 bucket. The script will print the URL of the uploaded ZIP file.