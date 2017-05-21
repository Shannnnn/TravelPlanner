from threading import Thread
from app import app, mail
from flask_mail import Message
from flask_login import current_user

#this will determine how many trips can be displayed each page of the template
<<<<<<< HEAD
POSTS_PER_PAGE = 12 
maxNum = 1
maxPage = 3

#max numbers of trips to be displayed for Most Popular Trips
max_for_most = 15 

#max numbers of trips to be displayed for Newest Trips
max_for_new = 15 

#formula needed to know the max page to be displayed given records of trips
num_of_page = max_for_new/POSTS_PER_PAGE 

#determines what to put on the header of all templates
def determine(id_): 
=======
POSTS_PER_PAGE = 12
maxNum = 1
maxPage = 3

#max numbers of trips to be displayed for Most Popular Trips
max_for_most = 15

#max numbers of trips to be displayed for Newest Trips
max_for_new = 15

#formula needed to know the max page to be displayed given records of trips
num_of_page = max_for_new/POSTS_PER_PAGE

#determines what to put on the header of all templates
def determine(id_):
>>>>>>> Changes in Friends
    if(id_==1):
        return "/admin"
    return "/home"

#this fucntion will return the proper labels and directories for the two big buttons on the headers of landing_blueprint
def verify():
    #first checks if user is authenticated in other words if user is logged in
   	if current_user.isAuthenticated():
      #returns the proper labels for logged in users
   		return [current_user.username, "Log Out", determine(current_user.role_id), "/logout"]
    #return the default values if user is anonymously visiting the templates
   	return ["Log In", "Sign Up", "/login", "/register"]

#this will send the email on a different host while still running in our main host
<<<<<<< HEAD
def send_async_email(app, msg): 
=======
def send_async_email(app, msg):
>>>>>>> Changes in Friends
    #this will append the process to the existing process
    with app.app_context():
        mail.send(msg)

 #the mail sending process
def send_email(subject, sender, recipients, text_body):
    #instance of the Message Class
<<<<<<< HEAD
    msg = Message(subject, sender=sender, recipients=recipients) 
    #the message body that will be viewed by the recipient/s
    msg.body = text_body 
=======
    msg = Message(subject, sender=sender, recipients=recipients)
    #the message body that will be viewed by the recipient/s
    msg.body = text_body
>>>>>>> Changes in Friends
    #Thread shall be implemented in order for the server not to terminate our main host
    thr = Thread(target=send_async_email, args=[app, msg])
    #Thread running
    thr.start()



