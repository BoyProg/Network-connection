import os
import socket
import platform
import subprocess
import time
from datetime import datetime
from pyfiglet import Figlet
from colorama import Fore, Style, init
import csv
import matplotlib.pyplot as plt
import speedtest

# Initialize colorama
init()

class NetworkToolsPro:
    """
    Network Tools Pro - Comprehensive network analysis and monitoring tool
    Features:
    1. System and network information
    2. Network device scanning
    3. Advanced ping
    4. Full-featured port scanner
    5. Internet speed test
    6. Results saving
    7. Network visualization
    """

    def __init__(self):
        self.hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(self.hostname)
        self.current_os = platform.system()
        self.scan_results = []
        self.ping_results = []
        self.port_scan_results = []
        self.speed_test_results = {}

    def display_header(self):
        """Display application header with styling"""
        custom_fig = Figlet(font="slant")
        banner = custom_fig.renderText("NET TOOLS PRO")
        print(Fore.CYAN + banner + Style.RESET_ALL)
        print(Fore.WHITE + f"System: {self.hostname} | IP: {self.local_ip} | OS: {self.current_os}")
        print(Fore.WHITE + f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + Style.RESET_ALL)


        print(Fore.WHITE + "\nDeveloped by NimaRezaei (Github BoyProg)")

    def scan_network_devices(self, save_to_file=False):
        """Scan network devices with save option"""
        print(Fore.BLUE + "\n[+] Scanning network devices..." + Style.RESET_ALL)
        
        try:
            if self.current_os == "Windows":
                result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            else:
                result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            
            devices = []
            for line in result.stdout.split('\n'):
                if "dynamic" in line.lower() or "ether" in line.lower():
                    parts = line.split()
                    ip = parts[0]
                    mac = parts[1] if len(parts) > 1 else "Unknown"
                    devices.append({"IP": ip, "MAC": mac, "Status": "Online"})
            
            self.scan_results = devices
            
            # Display results
            print(Fore.GREEN + "\nNetwork Devices:" + Style.RESET_ALL)
            print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
            for device in devices:
                print(f"IP: {device['IP']} | MAC: {device['MAC']}")
            print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
            
            if save_to_file:
                self._save_to_csv("network_devices.csv", devices)
                print(Fore.GREEN + "[+] Results saved to network_devices.csv" + Style.RESET_ALL)
                
        except Exception as e:
            print(Fore.RED + f"[!] Error scanning network: {e}" + Style.RESET_ALL)

    def advanced_ping(self, target, count=4, interval=1, timeout=2):
        """Advanced ping with configurable parameters"""
        print(Fore.BLUE + f"\n[+] Pinging {target}..."
               + Style.RESET_ALL)
        
        param = '-n' if self.current_os.lower() == 'windows' else '-c'
        command = ['ping', param, str(count), '-w', str(timeout*1000), target]
        
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
            print(result.stdout)
            
            # Analyze results
            if "unreachable" in result.stdout.lower():
                status = "Offline"
            else:
                # Extract response times
                lines = result.stdout.split('\n')
                times = []
                for line in lines:
                    if "time=" in line.lower():
                        time_str = line.split('time=')[1].split()[0]
                        times.append(float(time_str))
                
                if times:
                    avg_time = sum(times)/len(times)
                    status = f"Online (Avg: {avg_time:.2f}ms)"
                else:
                    status = "Online"
            
            self.ping_results.append({
                "Target": target,
                "Status": status,
                "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            return status
            
        except Exception as e:
            print(Fore.RED + f"[!] Ping error: {e}" + Style.RESET_ALL)
            return "Error"

    def port_scanner(self, target, start_port=1, end_port=100, timeout=0.5):
        """Advanced port scanner with progress display"""
        print(Fore.BLUE + f"\n[+] Scanning ports {start_port}-{end_port} on {target}..." + Style.RESET_ALL)
        
        open_ports = []
        start_time = time.time()
        
        for port in range(start_port, end_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(timeout)
                    result = s.connect_ex((target, port))
                    if result == 0:
                        service = socket.getservbyport(port, 'tcp') if port <= 49151 else "Unknown"
                        print(Fore.GREEN + f"[+] Port {port} ({service}): OPEN" + Style.RESET_ALL)
                        open_ports.append({
                            "Port": port,
                            "Service": service,
                            "Status": "Open"
                        })
                    else:
                        print(Fore.RED + f"[-] Port {port}: CLOSED" + Style.RESET_ALL)
            except socket.error:
                print(Fore.YELLOW + f"[!] Error scanning port {port}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"[!] General error: {e}" + Style.RESET_ALL)
        
        scan_time = time.time() - start_time
        self.port_scan_results.append({
            "Target": target,
            "Open Ports": open_ports,
            "Scan Time": f"{scan_time:.2f} seconds"
        })
        
        print(Fore.GREEN + f"\n[+] Scan completed in {scan_time:.2f} seconds" + Style.RESET_ALL)
        return open_ports

    def speed_test(self):
        """Internet speed test with detailed results"""
        print(Fore.BLUE + "\n[+] Running speed test..." + Style.RESET_ALL)
        
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            
            print(Fore.YELLOW + "[+] Testing download speed..." + Style.RESET_ALL)
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            
            print(Fore.YELLOW + "[+] Testing upload speed..." + Style.RESET_ALL)
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            
            ping = st.results.ping
            
            self.speed_test_results = {
                "Download": f"{download_speed:.2f} Mbps",
                "Upload": f"{upload_speed:.2f} Mbps",
                "Ping": f"{ping:.2f} ms",
                "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(Fore.GREEN + "\nSpeed Test Results:" + Style.RESET_ALL)
            print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
            print(f"Download: {download_speed:.2f} Mbps")
            print(f"Upload: {upload_speed:.2f} Mbps")
            print(f"Ping: {ping:.2f} ms")
            print(Fore.YELLOW + "-"*50 + Style.RESET_ALL)
            
            return self.speed_test_results
            
        except Exception as e:
            print(Fore.RED + f"[!] Speed test error: {e}" + Style.RESET_ALL)
            return None

    def visualize_network(self):
        """Visualize network devices"""
        if not self.scan_results:
            print(Fore.RED + "[!] No scan results available. Please scan network first." + Style.RESET_ALL)
            return
        
        ips = [device['IP'] for device in self.scan_results]
        statuses = [1 if device['Status'] == 'Online' else 0 for device in self.scan_results]
        
        plt.figure(figsize=(10, 6))
        plt.bar(ips, statuses, color=['green' if s == 1 else 'red' for s in statuses])
        plt.title("Network Devices Status")
        plt.xlabel("IP Address")
        plt.ylabel("Status (1=Online, 0=Offline)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        print(Fore.BLUE + "[+] Showing network visualization..." + Style.RESET_ALL)
        plt.show()

    def save_results_to_file(self, filename="network_report.txt"):
        """Save all results to a file"""
        try:
            with open(filename, 'w') as f:
                f.write("=== Network Tools Pro Report ===\n")
                f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("=== Network Devices ===\n")
                for device in self.scan_results:
                    f.write(f"IP: {device['IP']} | MAC: {device['MAC']} | Status: {device['Status']}\n")
                
                f.write("\n=== Ping Results ===\n")
                for ping in self.ping_results:
                    f.write(f"Target: {ping['Target']} | Status: {ping['Status']} | Time: {ping['Time']}\n")
                
                f.write("\n=== Port Scan Results ===\n")
                for scan in self.port_scan_results:
                    f.write(f"Target: {scan['Target']} | Scan Time: {scan['Scan Time']}\n")
                    for port in scan['Open Ports']:
                        f.write(f"  Port {port['Port']} ({port['Service']}): {port['Status']}\n")
                
                f.write("\n=== Speed Test Results ===\n")
                if self.speed_test_results:
                    f.write(f"Download: {self.speed_test_results['Download']}\n")
                    f.write(f"Upload: {self.speed_test_results['Upload']}\n")
                    f.write(f"Ping: {self.speed_test_results['Ping']}\n")
                    f.write(f"Test Time: {self.speed_test_results['Time']}\n")
            
            print(Fore.GREEN + f"[+] All results saved to {filename}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[!] Error saving results: {e}" + Style.RESET_ALL)

    def _save_to_csv(self, filename, data):
        """Save data to CSV format"""
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = data[0].keys() if data else []
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            print(Fore.RED + f"[!] CSV save error: {e}" + Style.RESET_ALL)

    def show_menu(self):
        """Display main interactive menu"""
        while True:
            print("\n" + Fore.LIGHTCYAN_EX + "| Main Menu |\n" + Style.RESET_ALL)
            print(Fore.GREEN + "1. Scan Network Devices")
            print("2. Advanced Ping")
            print("3. Port Scanner")
            print("4. Internet Speed Test")
            print("5. Visualize Network")
            print("6. Save All Results")
            print("0. Exit" + Style.RESET_ALL)
            
            choice = input("\nSelect an option (0-6): ")
            
            if choice == "1":
                save = input("Save results to file? (y/n): ").lower() == 'y'
                self.scan_network_devices(save)
            elif choice == "2":
                target = input("Enter target IP or hostname: ")
                count = int(input("Number of pings (default 4): ") or 4)
                self.advanced_ping(target, count)
            elif choice == "3":
                target = input("Enter target IP: ")
                start = int(input("Start port (default 1): ") or 1)
                end = int(input("End port (default 100): ") or 100)
                self.port_scanner(target, start, end)
            elif choice == "4":
                self.speed_test()
            elif choice == "5":
                self.visualize_network()
            elif choice == "6":
                filename = input("Enter filename (default network_report.txt): ") or "network_report.txt"
                self.save_results_to_file(filename)
            elif choice == "0":
                print(Fore.GREEN + "\n[+] Exiting Network Tools Pro. Goodbye!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "[!] Invalid choice!" + Style.RESET_ALL)
            
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        tool = NetworkToolsPro()
        tool.display_header()
        tool.show_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Program interrupted by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[!] Critical error: {e}" + Style.RESET_ALL)