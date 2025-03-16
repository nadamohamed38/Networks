import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("0.0.0.0",9999))
server.listen(5)

while True:
    client,addr = server.accept()
    massege = client.recv(1024).decode()
    print(massege)
    if massege[0] == "C":
        substring = massege[1:]  
        substring = "".join(sorted(substring))  
        
    elif massege[0] == "A":
        substring = massege[1:]
        substring = "".join(sorted(substring , reverse=True))
        
    elif massege[0] == "D":
        substring = massege[1:]
        substring = substring.upper()
    else:
        substring = massege
    print(substring)
    client.send(substring.encode())
         
    