# import library for networking 
import socket
import threading

# address and port of the target 
target = input("Enter the target IP address to scan: ")
port = 80

# function to scan ports on the target 
def port_scanner(port):
    try:
        
        # create a socket object 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set a timeout
        s.settimeout(5)

        con = s.connect((target, port))
        print(f'The port {port} is open.')
        con.close()
    except:
        pass
# scan the first 1024 ports 
for port in range(0, 1025):
    thread = threading.Thread(target=port_scanner, args=(port,))
    thread.start()

input()