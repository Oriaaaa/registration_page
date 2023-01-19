# Orian Eluz


import socket
from PIL import ImageFile
import os
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
import re
import hashlib

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 42069))  # connection to server

ImageFile.LOAD_TRUNCATED_IMAGES = True




def reply_length(the_reply):
    """returns the reply length"""
    length = str(len(the_reply))  # the reply's length
    length = str(length.zfill(4))  # filling the length with 0s
    return length


def sending_message_and_answer(msg, a_list):
    """sending a message and then receiving the answer from server"""
    message_arr = msg.split(r' \"')
    print(message_arr[0].upper())
    while message_arr[0].upper() != "EXIT":
        print(message_arr[0].upper())

        if message_arr[0].upper() in a_list:
            the_length = reply_length(msg)
            my_socket.send(the_length.encode())
            my_socket.send(msg.encode())  # sending the message to the server
            data_length = my_socket.recv(4).decode()  # receiving the reply's length from server
            print("reply's length " + data_length)
            answer = my_socket.recv(int(data_length)).decode()  # receiving the reply from server
            print("the server sent: " + answer)
            msg = input(
                "enter one of the commands: DIR, DELETE, COPY,EXECUTE,SCREENSHOT, EXIT")  # another message
            message_arr = msg.split(r' \"')
        else:
            print("please send a valid command")
            msg = input("enter one of the commands: DIR, DELETE, COPY,EXECUTE,SCREENSHOT, EXIT")
            message_arr = msg.split(r' \"')
    return msg

LARGEFONT = ("Verdana", 35)

f = ('Times', 14)
def reply_length(the_reply):
    """returns the reply length"""
    length = str(len(the_reply))  # the reply's length
    length = str(length.zfill(4))  # filling the length with 0s
    return length


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        def login_response():
            seperator="#<>#"
            uname = email_tf.get()
            upwd = pwd_tf.get()
            check_counter = "login"+seperator
            counter=0
            if uname == "":
                warn = "email can't be empty"
                messagebox.showerror('Login Status', warn)
            else:
                check_counter+=uname+seperator
                counter += 1
                if upwd == "":
                    warn = "Password can't be empty"
                    messagebox.showerror('Login Status', warn)
                else:
                    check_counter += upwd + seperator
                    counter += 1
            if counter == 2:
                my_socket.send(reply_length(check_counter).encode())
                my_socket.send(check_counter.encode())
                data_length = my_socket.recv(4).decode()  # receiving the reply's length from server
                print("reply's length " + data_length)
                answer = my_socket.recv(int(data_length)).decode()  # receiving the reply from server
                print("the server sent: " + answer)
                messagebox.showinfo('Login Status', answer)

            else:
                messagebox.showerror('Login Status', 'invalid username or password')
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = Label(self, text="Startpage")

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)
        # widgets
        left_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )

        Label(
            left_frame,
            text="Enter Email",
            bg='#CCCCCC',
            font=f).grid(row=0, column=0, sticky=W, pady=10)

        Label(
            left_frame,
            text="Enter Password",
            bg='#CCCCCC',
            font=f
        ).grid(row=1, column=0, pady=10)

        email_tf = Entry(
            left_frame,
            font=f
        )
        pwd_tf = Entry(
            left_frame,
            font=f,
            show='*'
        )
        login_btn = Button(
            left_frame,
            width=15,
            text='Login',
            font=f,
            relief=SOLID,
            cursor='hand2',
            command=login_response
        )
        bottom_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )
        email_tf.grid(row=0, column=1, pady=10, padx=20)
        pwd_tf.grid(row=1, column=1, pady=10, padx=20)
        login_btn.grid(row=2, column=1, pady=10, padx=20)
        left_frame.place(x=50, y=50)

        button1 = Button(bottom_frame, text="Page 1",
                         command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)


        bottom_frame.place(x=50, y=300)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        x = controller.winfo_screenwidth()

        y = controller.winfo_screenheight()

        controller.geometry("%dx%d" % (x, y))

        tk.Frame.__init__(self, parent)
        label = Label(self, text="Page 1", )
        label.grid(row=0, column=4, padx=10, pady=10)

        f = ('Times', 14)



        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        seperate="#<>#"

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

        def insert_record():
            check_counter = ""
            counter = 0
            warn = "info sent"
            if register_name.get() == "":
                warn = "Name can't be empty"
            elif not checkString(register_name.get()):
                warn = "Name can't be numbers"
            else:
                check_counter +=seperate+ register_name.get()
                counter += 1
                if register_email.get() == "":
                    warn = "Email can't be empty"
                elif not re.fullmatch(regex, register_email.get()):
                    warn = "enter valid email address"
                else:
                    check_counter +=seperate+ register_email.get()
                    counter += 1
                    if register_mobile.get() == "":
                        warn = "Contact can't be empty"
                    elif len(register_mobile.get()) < 10:
                        warn = "Contact Number too short"
                    elif len(register_mobile.get()) > 10:
                        warn = "Contact Number too long"
                    elif not check_contact(register_mobile.get()):
                        warn = "Contact Number contains letters"
                    else:
                        check_counter += seperate+register_mobile.get()
                        counter += 1
                        if var.get() == "":
                            warn = "Select Gender"
                        else:
                            check_counter += seperate+var.get()
                            counter += 1
                            if variable.get() == "":
                                warn = "Select Country"
                            else:
                                check_counter += seperate+variable.get()
                                counter += 1
                                if register_pwd.get() == "":
                                    warn = "Password can't be empty"
                                else:
                                    check_counter += seperate+ str(hashlib(register_pwd.get()))
                                    counter += 1
                                    if pwd_again.get() == "":
                                        warn = "Re-enter password can't be empty"
                                    else:
                                        check_counter += seperate+ str(hashlib(pwd_again.get()))
                                        counter += 1
                                        if register_pwd.get() != pwd_again.get():
                                            warn = "Passwords didn't match!"
                                        else:
                                            counter += 1

            if counter == 8:
                msg ="registration"+check_counter
                print(msg)
                my_socket.send(reply_length(msg).encode())
                print(reply_length(msg))
                my_socket.send(msg.encode())  # sending the last message (exit)
                data_length = my_socket.recv(4).decode()  # receiving the reply's length from server
                print("reply's length " + data_length)
                answer = my_socket.recv(int(data_length)).decode() # receiving the reply from server
                print("the server sent: " + answer)
                if answer=="verify":
                    messagebox.showinfo('confirmation', 'success')
                    controller.show_frame(Page2)
                else:
                    messagebox.showinfo("ERROR", "error")
            else:
                messagebox.showinfo("ERROR",warn)



        var = StringVar()
        var.set('male')

        countries = []
        variable = StringVar()
        world = open('countries.txt', 'r')
        for country in world:
            country = country.rstrip('\n')
            countries.append(country)
        variable.set(countries[22])

        right_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )

        Label(
            right_frame,
            text="Enter Name",
            bg='#CCCCCC',
            font=f
        ).grid(row=0, column=0, sticky=W, pady=10)

        Label(
            right_frame,
            text="Enter Email",
            bg='#CCCCCC',
            font=f
        ).grid(row=1, column=0, sticky=W, pady=10)

        Label(
            right_frame,
            text="Contact Number",
            bg='#CCCCCC',
            font=f
        ).grid(row=2, column=0, sticky=W, pady=10)

        Label(
            right_frame,
            text="Select Gender",
            bg='#CCCCCC',
            font=f
        ).grid(row=3, column=0, sticky=W, pady=10)

        Label(
            right_frame,
            text="Select Country",
            bg='#CCCCCC',
            font=f
        ).grid(row=4, column=0, sticky=W, pady=10)

        Label(
            right_frame,
            text="Enter Password",
            bg='#CCCCCC',
            font=f
        ).grid(row=5, column=0, sticky=W, pady=10)

        Label(
            right_frame,
            text="Re-Enter Password",
            bg='#CCCCCC',
            font=f
        ).grid(row=6, column=0, sticky=W, pady=10)

        gender_frame = LabelFrame(
            right_frame,
            bg='#CCCCCC',
            padx=10,
            pady=10,
        )

        register_name = Entry(
            right_frame,
            font=f
        )

        register_email = Entry(
            right_frame,
            font=f
        )

        register_mobile = Entry(
            right_frame,
            font=f
        )

        register_country = OptionMenu(
            right_frame,
            variable,
            *countries)

        register_country.config(
            width=15,
            font=('Times', 12)
        )
        register_pwd = Entry(
            right_frame,
            font=f,
            show='*'
        )
        pwd_again = Entry(
            right_frame,
            font=f,
            show='*'
        )

        male_rb = Radiobutton(
            gender_frame,
            text='Male',
            bg='#CCCCCC',
            variable=var,
            value='male',
            font=('Times', 10),

        )

        female_rb = Radiobutton(
            gender_frame,
            text='Female',
            bg='#CCCCCC',
            variable=var,
            value='female',
            font=('Times', 10),

        )

        others_rb = Radiobutton(
            gender_frame,
            text='Others',
            bg='#CCCCCC',
            variable=var,
            value='others',
            font=('Times', 10)

        )

        register_btn = Button(
            right_frame,
            width=15,
            text='Register',
            font=f,
            relief=SOLID,
            cursor='hand2',
            command=insert_record
        )
        bottom_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )

        # widgets placement

        register_name.grid(row=0, column=1, pady=10, padx=20)
        register_email.grid(row=1, column=1, pady=10, padx=20)
        register_mobile.grid(row=2, column=1, pady=10, padx=20)
        register_country.grid(row=4, column=1, pady=10, padx=20)
        register_pwd.grid(row=5, column=1, pady=10, padx=20)
        pwd_again.grid(row=6, column=1, pady=10, padx=20)
        register_btn.grid(row=7, column=1, pady=10, padx=20)
        right_frame.place(x=500, y=50)

        gender_frame.grid(row=3, column=1, pady=10, padx=20)
        male_rb.pack(expand=True, side=LEFT)
        female_rb.pack(expand=True, side=LEFT)
        others_rb.pack(expand=True, side=LEFT)

        # infinite loop

        # button to show frame 2 with text
        # layout2
        button1 = Button(bottom_frame, text="login",
                         command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.grid(row=8, column=1, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2

        bottom_frame.place(x=50, y=300)


# third window frame page2
class Page2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = Label(self, text="Page 2")
        label.grid(row=0, column=4, padx=10, pady=10)
        def confirmation():
            msg = "confirmation"+"#<>#"+confirmation_tf.get()
            print(msg)
            my_socket.send(reply_length(msg).encode())
            print(reply_length(msg))
            my_socket.send(msg.encode())  # sending the last message (exit)
            data_length = my_socket.recv(4).decode()  # receiving the reply's length from server
            print("reply's length " + data_length)
            answer = my_socket.recv(int(data_length)).decode()  # receiving the reply from server
            print("the server sent: " + answer)
            if answer == "registration completed":
                messagebox.showinfo('confirmation', 'Record Saved')
                controller.show_frame(StartPage)
            else:
                messagebox.showinfo("ERROR", "error")
        left_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )

        Label(
            left_frame,
            text="",
            bg='#CCCCCC',
            font=f).grid(row=0, column=0, sticky=W, pady=10)

        Label(
            left_frame,
            text="Enter code",
            bg='#CCCCCC',
            font=f
        ).grid(row=1, column=0, pady=10)

        confirmation_tf = Entry(
            left_frame,
            font=f
        )

        confirm_btn = Button(
            left_frame,
            width=15,
            text='send',
            font=f,
            relief=SOLID,
            cursor='hand2',
            command=confirmation
        )
        bottom_frame = Frame(
            self,
            bd=2,
            bg='#CCCCCC',
            relief=SOLID,
            padx=10,
            pady=10
        )
        confirmation_tf.grid(row=0, column=1, pady=10, padx=20)
        confirm_btn.grid(row=1, column=1, pady=10, padx=20)
        left_frame.place(x=500, y=50)

        # button to show frame 2 with text
        # layout2
        button1 = Button(bottom_frame, text="register",
                         command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = Button(bottom_frame, text="login",
                         command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)
        bottom_frame.place(x=50,y=200)




app = tkinterApp()
app.mainloop()




