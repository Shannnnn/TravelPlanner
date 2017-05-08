from threading import Thread
from app import app, mail
from flask_mail import Message
from flask_login import current_user

POSTS_PER_PAGE = 4
maxNum = 1
maxPage = 3
max_for_most = 8
max_for_new = 8

def determine(id_):
    detail=""
    if(id_==1):
        detail="/admin"
    elif(id_==3):
        detail="/home"
    return detail

def verify():
	label =[]
   	if current_user.isAuthenticated():
   		label = [current_user.username, "Log Out", determine(current_user.role_id), "/logout"]
   	else:
   		label = ["Log In", "Sign Up", "/login", "/register"]
   	return label

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

