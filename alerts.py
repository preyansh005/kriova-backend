import smtplib
from email.message import EmailMessage
from random import random

class EmailAlerts():
    def email_otp(to):
        _user = ''
        _password = ''

        otp = int(random()*10000000)
        body=f"Your One Time Password is: {otp}"

        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = f"Your One-Time-Password is here"
        msg['to'] = to
        msg['from'] = _user

        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(_user,_password)
        server.send_message(msg)
        server.quit()
        return otp
