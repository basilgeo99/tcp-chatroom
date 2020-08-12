import threading
import socket
from cryptography.fernet import Fernet

port = 34443
localhost = '127.0.0.1'
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

while True:
    try:
        host = input("Enter host address: ")
        if host == 'local':
            host = localhost
        server.bind((host,port))
        print('\nServer connection success')
        break
    except Exception as e:
        print("\nError occurred ")
        print(e)
        break
server.listen()


clients = []
nicknames = []

key = Fernet.generate_key()
f = Fernet(key)

def encrpyter(message):
    return f.encrypt(message.encode('ascii'))

def decrypter(message):
    return f.decrypt(message).decode('ascii')

def broadcast(message):
    for client in clients:
        client.send(message)

def toOthers(message,client):
    for c in clients:
        if c == client:
            pass
        else:
            c.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            toOthers(message,client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chatroom'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        try:
            client,address = server.accept()
            print(f'\nConnected with {str(address)}')
            
            client.send("NICK".encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            client.send("\n--- type CLOSE_CONN to close the connection ---\n".encode('ascii'))

            print(f'\nNickname of the client is {nickname}')
            broadcast(f'{nickname} joined the chatroom'.encode('ascii'))
            client.send('Connected to the server'.encode('ascii'))

            thread = threading.Thread(target = handle, args=(client,))
            thread.start()
        except KeyboardInterrupt:
            print('\nShutting down server ...')
            broadcast('CLOSE_CONN'.encode('ascii'))
            for t in threading.enumerate:
                t.join()
            server.close()
            break

print('\nServer is listening ...')
receive()

