import os
import socket
import platform
from datetime import datetime

def check_network_devices():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(f"Network connection v1.5.0")
    print(f"Developed by NimaRezaei (NRezz)\n")
    print(f"Your system {hostname} - IP: {local_ip}")
    print(f"Checking the date and time {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nSearching for network connected devices...\n")

    current_os = platform.system()

    if current_os == "Windows":
        os.system("arp -a")
    elif current_os in ["Linux", "Darwin"]:
        os.system("arp -a")
    else:
        print("Operating system not supported")

if __name__ == "__main__":
    check_network_devices()
    input("\nPress Enter to exit...")
