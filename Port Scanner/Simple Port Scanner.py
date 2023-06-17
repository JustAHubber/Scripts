# import library for networking 
import socket

# address and port of the target 
target = 'localhost'
port = 80

# create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set a timeout
s.settimeout(5)

# function to scan ports on the target 
def port_scanner(port):
    if s.connect_ex((target, port)):
        print(f'The port {port} is closed')
    else:
        print(f'The port {port} is open')

if __name__ == "__main__":
# scan the first 1024 ports 
    for port in range(0, 1025):
        port_scanner(port)

input()