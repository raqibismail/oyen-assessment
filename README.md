# Oyen Assessment

## Steps to Run the Code

Before running the code, make sure you have the following prerequisites installed:

    pip install -r requirements.txt

Follow these steps to run the code:

1. Start the backend server using `uvicorn`:
   
   uvicorn main:app --reload

2. In a new terminal or command prompt, start the frontend server using http-server:
    
    npx http-server

3. Enter the username and password on the login page:

    Username: test, Password: password
    Username: admin, Password: admin
    Username: raqib, Password: password

4. If the login is successful, you can check the Inspect Element feature in your browser.

    1. Open the Application tab.
    2. Under Local Storage, you will find the accessToken saved there.

5. The SQLite database (database.db) contains a table called "login history" with the following columns:

    username: Stores the username of the login.
    datetime: Stores the date and time of the login.
    accessToken: Stores the access token associated with the login.
