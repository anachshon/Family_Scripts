import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class MyMail:

    def __init__( self ):

        self.sender_email = "akjsutr@gmail.com"
        self.password = "Send@2019"

    def send_mail( self, receiver_email, file_name ):

        message = MIMEMultipart("alternative")
        message["Subject"] = "stl object"
        message["From"] = self.sender_email
        message["To"] = receiver_email

        file = open( file_name, 'r' )
        text = file.read()
        file.close()

        part = MIMEApplication( text, file_name )
        part['Content-Disposition'] = 'attachment; filename=' + file_name

        message.attach( part )

        s = smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.login( self.sender_email, self.password )
        s.sendmail( self.sender_email, receiver_email, message.as_string() )
