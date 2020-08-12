import socket
import threading

localhost = '127.0.0.1'
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


# host = localhost
# port = 34443
# client.connect((host,port))


while True:
    try:
        host = input("Enter host address: ")
        port = int(input("Enter port: "))
        if host == 'local':
            host = localhost
        client.connect((host,port))
        print('\nConnection success')
        break
    except Exception as e:
        print('\nConnection error - check host and port (port must be 0-65535) ')
        print(e)

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'CLOSE_CONN':
                close_conn()
            elif message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        
        except KeyboardInterrupt:
            close_conn()
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def close_conn():
    print('\nClosing connection')
    client.close()
    receive_thread.join()
    write_thread.join()


def write():
    while True:
        try :
            message = input('> ')
            if message == "close connection":
                close_conn()
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('ascii'))
        except KeyboardInterrupt:
            print('\nClosing connection')
            client.close()
            receive_thread.join()
            write_thread.join()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()