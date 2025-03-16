import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',9999))
text = input("Enter your text: ")
client.send(text.encode())
print("updated text: "+client.recv(1024).decode())