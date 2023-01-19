# Orian Eluz

import socket
from datetime import datetime
import random
import glob
import os
import shutil
import subprocess
import sys
import PIL.Image
import sqlite3
import re
import smtplib
import ssl
from email.message import EmailMessage




con = sqlite3.connect('userdata.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    name text, 
                    email text, 
                    contact number, 
                    gender text, 
                    country text,
                    password text
                )
            ''')
con.commit()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
seperate = "#<>#"


def checkString(str):
    for i in str:
        # if string has number
        if i.isdigit():
            return False
    return True


def check_contact(str):
    for i in str:
        # if string has number
        if not i.isdigit():
            return False
    return True

def confirm_response(email):
    # Define email sender and receiver
    email_sender = 'orianprojectmail@gmail.com'
    email_password = 'puqhlabmchrrokpv'
    email_receiver = email
    global ran
    ran=random.randint(100000,999999)
    # Set the subject and body of the email
    subject = 'verification email'
    body = """your verification code is: """ +str(ran)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def verification(code):
    if code == str(ran):
        try:
            con = sqlite3.connect('userdata.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record VALUES (:name, :email, :contact, :gender, :country, :password)", {
                'name': record[1],
                'email': record[2],
                'contact': record[3],
                'gender': record[4],
                'country': record[5],
                'password': record[6]

            })
            con.commit()
            return "registration completed"
        except Exception as ep:
            return "error"
    else:
        return "incorrect"

def insert_record(arr):
    check_counter = 0
    warn = ""
    if arr[1] == "":
        print(arr[1])
        warn = "Name can't be empty"
    elif not checkString(arr[1]):
        warn = "Name can't be numbers"
    else:
        check_counter += 1
        if arr[2] == "":
            warn = "Email can't be empty"
        elif not re.fullmatch(regex, arr[2]):
            warn = "enter valid email address"
        else:
            check_counter += 1
            if arr[3] == "":
                warn = "Contact can't be empty"
            elif len(arr[3]) < 10:
                warn = "Contact Number too short"
            elif len(arr[3]) > 10:
                warn = "Contact Number too long"
            elif not check_contact(arr[3]):
                warn = "Contact Number contains letters"
            else:
                check_counter += 1
                if arr[4] == "":
                    warn = "Select Gender"
                else:
                    check_counter += 1
                    if arr[5] == "":
                        warn = "Select Country"
                    else:
                        check_counter += 1
                        if arr[6] == "":
                            warn = "Password can't be empty"
                        else:
                            check_counter += 1
                            if arr[7] == "":
                                warn = "Re-enter password can't be empty"
                            else:
                                check_counter += 1
                                if arr[6]!= arr[7]:
                                    warn = "Passwords didn't match!"
                                else:
                                    check_counter += 1

    if check_counter == 8:
        print("yass")
        confirm_response(arr[2])
        return "verify"

    else:
        return warn


def login_response(arr):
    uemail = arr[1]
    upwd = arr[2]
    cur.execute("""SELECT email
                             ,password
                      FROM userdata.db
                      WHERE email=?
                          AND password=?""",
                (uemail,upwd ))
    print(uemail)

    # Fetch one result from the query because it
    # doesn't matter how many records are returned.
    # If it returns just one result, then you know
    # that a record already exists in the table.
    # If no results are pulled from the query, then
    # fetchone will return None.
    result = cur.fetchone()

    if result:
        return 'Logged in Successfully!'
    else:
        return 'invalid username or password'



def connect_to_client():
    """connecting to the client"""
    a_server_socket = socket.socket()
    a_server_socket.bind(("127.0.0.1", 42069))  # binding to client
    a_server_socket.listen()  # connecting to client
    print("Server is up and running")

    (a_client_socket, client_address) = a_server_socket.accept()  # server's client
    print("Client connect")
    return a_server_socket, a_client_socket


def reply_length(the_reply):
    """returns the reply length"""
    length = str(len(the_reply))  # the reply's length
    length = str(length.zfill(4))  # filling the length with 0s
    return length


def main():
    server_socket, client_socket = connect_to_client()
    data_length = client_socket.recv(4).decode()  # receiving the message's length from client
    print("message's length " + data_length)
    message = client_socket.recv(int(data_length)).decode()  # receiving the message from client
    print("the client sent: " + message)
    message_arr = message.split(r'#<>#')
    command = message_arr[0]  # the command from the client
    while True:
        if command=="registration":
            global record
            record=message_arr
            msg=insert_record(message_arr)
            print(insert_record(message_arr))
            client_socket.send(reply_length(msg).encode())
            client_socket.send(msg.encode())  # sending the last message (exit)
        elif command=="login":
            msg = login_response(message_arr)
            client_socket.send(reply_length(msg).encode())
            client_socket.send(msg.encode())  # sending the last message (exit)
        elif command == "confirmation":
            msg = verification(message_arr[1])
            client_socket.send(reply_length(msg).encode())
            client_socket.send(msg.encode())  # sending the last message (exit)
        data_length = client_socket.recv(4).decode()  # receiving the message's length from client
        print("message's length " + data_length)
        message = client_socket.recv(int(data_length)).decode()  # receiving the message from client
        print("the client sent: " + message)
        message_arr = message.split(r'#<>#')
        command = message_arr[0]  # the command from the client





if __name__ == "__main__":
    main()