import os
import socket
import platform
from datetime import datetime

def check_network_devices():

    hostname = socket.gethostbyname()
    local_ip = socket.gethostname(hostname)

    print(f"your system {hostname} - IP: {local_ip}")
    print(f"checking the date and time {datetime.new().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nSearching for network connected devices...\n")

    current_os = platform.system()

    if current_os == "Windos":
        os.system("arp -a")
    elif current_os in ["Linux", "Darwin"]:

        os.system("arp -a")
    else:
        print("Operating system not supported")
if __name__ == "__main__":
    check_network_devices()
    input("\nPress Enter to exit...")