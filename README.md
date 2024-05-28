
# Chat Message Generator

This Python script generates random chat messages between random users and stores them in a PostgreSQL database.

## Prerequisites

Before running the script, ensure you have the following installed:

-   Python 3.x

## Setup


1.  **Virtual Environment Setup**:

-   Create a virtual environment using the following command:
    
    bash
    
    Copy code
    
    `python -m venv env`
    
2.  **Install Dependencies**:

-   Install required packages using the provided `requirements.txt` file:
    
    bash
    
    Copy code
    
    `pip install -r requirements.txt`

3.  **Database Configuration**:
    
    -   Open the `main.py` file.
        
    -   Modify the `db_config` dictionary with your PostgreSQL database connection details:
        
        python
        
        Copy code
        
        `db_config = {
            'dbname': 'your_db_name',
            'user': 'your_db_user',
            'password': 'your_db_password',
            'host': 'your_db_host',
            'port': 'your_db_port'
        }` 
        
    -   Create a `.env` file based on the provided `.env.example` file and set the database configurations accordingly.
        

## Usage

1.  Open a terminal or command prompt.
    
2.  Navigate to the directory containing the `main.py` file.
    
3.  Run the script with the following command:
    
    bash
    
    Copy code
    
    `python main.py N` 
    
    Replace `N` with the number of chat messages you want to generate.
    
4.  The script will generate random chat messages between random users and store them in the PostgreSQL database.