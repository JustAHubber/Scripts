import socket
import datetime
import concurrent.futures
import os
import asyncio
from tqdm import tqdm
from termcolor import colored

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_log.txt")  # Log file in the same directory as the script

port_descriptions = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    465: "SMTPS",
    587: "SMTP (Submission)",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
}

def log_scan_start(mode):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n[--- New Scan ---]\nScan Mode: {mode}\nTimestamp: {timestamp}"

    with open(log_file, "a") as file:
        file.write(log_entry + "\n")

    tqdm.write(colored(log_entry, "green"))

def log_scan_result(ip, port, protocol):
    log_entry = f"IP: {ip}, Port {port} ({protocol})"

    with open(log_file, "a") as file:
        file.write(log_entry + "\n")

    tqdm.write(colored(log_entry, "green"))

async def scan_port(ip, port, mode, progress_bar):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Set the timeout value for the port connection attempt

        await asyncio.get_event_loop().sock_connect(sock, (ip, port))
        sock.close()
        protocol = get_protocol(port)
        log_scan_result(ip, port, protocol)
        progress_bar.update(1)
        return port, True

    except (socket.error, socket.timeout, ConnectionRefusedError):
        progress_bar.update(1)
        return port, False

def get_protocol(port):
    if port in port_descriptions:
        return port_descriptions[port]
    else:
        return "Unknown"

async def specific_mode(ip):
    mode = "Specific Scan"
    log_scan_start(mode)

    tasks = []
    print(f"\nSpecific Scanning: IP {ip}\n")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        progress_bar = tqdm(total=65535, desc=colored("Specific Scanning", "cyan"), unit="port", ncols=80, bar_format="{desc}: {percentage:.1f}%|{bar}| {n_fmt}/{total_fmt} {elapsed}<{remaining}, {rate_fmt}{postfix}")

        for port in range(1, 65536):
            tasks.append(scan_port(ip, port, mode, progress_bar))

        await asyncio.gather(*tasks)

    progress_bar.close()

def main():
    mode = input("Please select a mode (1 - Specific): ")

    if mode == "1":
        ip = input("Enter the IP to scan: ")
        asyncio.run(specific_mode(ip))
    else:
        print(colored("Invalid mode selection. Please try again.", "red"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan stopped by user.")

input()