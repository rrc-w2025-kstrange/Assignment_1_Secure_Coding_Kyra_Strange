import os
import pymysql
import smtplib
from email.message import EmailMessage
from urllib.request import urlopen

# The database credentials were moved to environment 
# variables so they are not hard coded in the source code,
# reducing the risk of authentication failures (OWASP A07).
db_config = {
    'host': os.environ.get("DB_HOST"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD")
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input
    
# I removed os.system and used Python’s email library instead, which prevents command injection attacks (OWASP A03).
def send_email(to, subject, body):
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("localhost") as server:
        server.send_message(msg)
    
# I changed the API URL to use HTTPS instead of HTTP so the data is encrypted while being sent (OWASP A02).
def get_data():
    url = 'https://secure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data
    
# I removed the f-string from the SQL query and used placeholders to avoid SQL injection (OWASP A03).
def save_to_db(data):
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    
    cursor.execute(query, (data, "Another Value"))
    
    connection.commit()
    cursor.close()
    connection.close()

# I added a simple check to make sure the user input is valid before using it,
# instead of blindly trusting it (OWASP A04).
if __name__ == '__main__':
    user_input = get_user_input()

    if user_input and len(user_input) < 500:
        data = get_data()
        save_to_db(data)
        send_email('admin@example.com', 'User Input', user_input)
    else:
        print("Invalid input provided.")
