import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com', 25)

server.ehlo()

#server.login('mail@mail.com', 'password') #!!!!Never do that save your password in encrypted file and pull it from there.

with open('password.txt', 'r') as f: #Do that instead for security
    password = f.read()

server.login('mailtesting@gmail.com', password)

msg = MIMEMultipart()
msg['From'] = 'Sender'
msg['To'] = 'testmail@example.com'
msg['Subject'] = 'Just A Test'

with open('message.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message, 'plain'))

filename = 'image.jpg'
attachment = open(filename, 'rb')

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename= {filename}')
msg.attach(p)

text = msg.as_string()
server.sendmail('mailtesting@gmail.com', 'testmail@example.com', text)
