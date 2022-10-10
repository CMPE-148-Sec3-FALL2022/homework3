from socket import *
import ssl
import base64
import socket

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"
ssl_context = ssl.create_default_context()
client_socket = socket.create_connection((mailserver, 465))
client_socket = ssl_context.wrap_socket(client_socket, server_hostname=mailserver)
print(client_socket.recv(1024).decode())

# Send HELO command and print server response.
heloCommand = "HELO Ryan\r\n"
client_socket.send(heloCommand.encode())
print(client_socket.recv(1024).decode())

# Authenticate with GMAIL
# read login data from secret file (excluded in .gitignore)
(email, app_password) = open("gmail_login_info").read().split()
b64_email = base64.b64encode(email.encode())
b64_app_password = base64.b64encode(app_password.encode())
client_socket.send("AUTH LOGIN ".encode() + b64_email + "\r\n".encode())
print(client_socket.recv(1024).decode())
client_socket.send(b64_app_password + "\r\n".encode())
print(client_socket.recv(1024).decode())

# Send MAIL FROM command and print server response.
client_socket.send(("MAIL FROM: <" + email + "> \r\n").encode())
print(client_socket.recv(1024).decode())

# Send RCPT TO command and print server response.
client_socket.send(("RCPT TO: <" + email + "> \r\n").encode())
print(client_socket.recv(1024).decode())

# Send DATA command and print server response.
client_socket.send("DATA\r\n".encode())
print(client_socket.recv(1024).decode())

# Send message data.
client_socket.send(msg.encode())

# Message ends with a single period.
client_socket.send(endmsg.encode())
print(client_socket.recv(1024).decode())

# Send QUIT command and get server response.
client_socket.send("QUIT\r\n".encode())
print(client_socket.recv(1024).decode())
client_socket.close()
