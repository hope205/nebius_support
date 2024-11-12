# nebius_support

Nebius AI assistant is a customer support chatbot that helps to answers questions about Nebius AI studio. It was built using open source models from Nebius AI studio.

## Prerequisites

-   [Python](https://www.python.org/downloads/) (version 3.7 or above recommended)
-   [Git](https://git-scm.com/)

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

First, clone the repository using the following command:


`git clone https://github.com/hope205/nebius_support.git` 

Navigate into the project directory:

`cd nebius_support` 

### 2. Create a Virtual Environment

It’s recommended to use a virtual environment to manage dependencies. Run the following commands to create and activate a virtual environment:

-   **On Windows:**

    `python -m venv venv
    venv\Scripts\activate` 
    
-   **On macOS and Linux:**
    
    `python3 -m venv venv
    source venv/bin/activate` 
    

### 3. Install Required Packages

With the virtual environment activated, install the required packages by running:

`pip install -r requirements.txt` 

### 4. Run the Application

Now, launch the Streamlit application by executing:


`streamlit run app.py` 

### 5. Deactivate the Virtual Environment

After you’re done working on the application, you can deactivate the virtual environment with:

`deactivate`

