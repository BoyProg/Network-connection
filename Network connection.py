import os
import socket
import platform
from datetime import datetime
from pyfiglet import Figlet
from colorama import Fore, Style

class bcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_banner():
    custom_fig = Figlet(font="slant")

    banner = custom_fig.renderText("Net connection")
    colored_banner = Fore.CYAN + banner + Style.RESET_ALL
    return colored_banner
if __name__ == "__main__":
    print(create_banner())

def check_network_devices():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print("\x1b[3;32;40m"+"\nNetwork connection"+"\x1b[0m")
    print("\x1b[3;32;40m"+"Developed by NimaRezaei - Git BoyProg\n"+"\x1b[0m")
    print("\x1b[3;33;40m"+f"Your system {hostname} - IP: {local_ip}")
    print("\x1b[3;33;40m"+f"Checking the date and time {datetime.now().strftime('%Y-%m-%d %H:%M:%S\n')}")
    print("\x1b[3;30;42m"+"Searching for network connected devices..."+"\x1b[0m")
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
