#!/usr/bin/env python3
"""
Tool Name: mono_d_n_m.py
Description: Integrated Device Management & Network Monitoring Framework
Author: Mamun (Natespo)
For Educational Purposes Only
"""

import os
import sys
import time
import socket
import platform
import subprocess
import hashlib
import json
import secrets
import threading
from datetime import datetime, timedelta
from collections import defaultdict

# রঙ সেটআপ
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

# --- ১. অথেন্টিকেশন সিস্টেম ---
class DeviceAuth:
    def __init__(self):
        self.sessions = {}
        self.secret_key = secrets.token_hex(32)
    
    def generate_device_id(self, info):
        device_string = f"{info.get('Hostname', '')}{platform.node()}"
        return hashlib.sha256(device_string.encode()).hexdigest()[:16]

    def create_session(self, device_id):
        token = secrets.token_hex(16)
        self.sessions[token] = {
            'device_id': device_id,
            'expires': datetime.now() + timedelta(hours=1)
        }
        return token

# --- ২. ডিভাইস ম্যানেজমেন্ট ---
class DeviceManager:
    def __init__(self):
        self.os_type = platform.system()
    
    def get_info(self):
        return {
            'Hostname': platform.node(),
            'OS': platform.system(),
            'Release': platform.release(),
            'Processor': platform.processor(),
            'Python': platform.python_version()
        }

    def check_security(self):
        status = {'Firewall': False, 'Root/Admin': False, 'Encryption': False}
        if self.os_type == 'Linux':
            status['Root/Admin'] = os.geteuid() == 0
            try:
                res = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
                status['Firewall'] = 'active' in res.stdout
            except: pass
        return status

# --- ৩. নেটওয়ার্ক মনিটরিং ---
class NetworkMonitor:
    def __init__(self):
        self.interface = "eth0" # Termux বা Linux এর জন্য প্রয়োজন হলে পরিবর্তন করো
    
    def get_stats(self):
        try:
            with open('/proc/net/dev', 'r') as f:
                for line in f:
                    if self.interface in line:
                        parts = line.split()
                        return {'RX': int(parts[1]), 'TX': int(parts[9])}
        except: return {'RX': 0, 'TX': 0}

    def scan_network(self):
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "127.0.0.1"
            
        prefix = ".".join(local_ip.split('.')[:-1]) + "."
        print(f"\n{Colors.CYAN}[*] Scanning Network: {prefix}0/24{Colors.END}")
        active_hosts = []
        
        # দ্রুত রেজাল্টের জন্য প্রথম ৩০টি আইপি চেক করছে
        for i in range(1, 31):
            ip = prefix + str(i)
            response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
            if response == 0:
                active_hosts.append(ip)
        return active_hosts

# --- ব্যানার এবং ইন্টারফেস ---
def show_banner():
    os.system('clear' if os.name == 'nt' else 'clear')
    print(f"""{Colors.CYAN}{Colors.BOLD}
    
    ███╗   ███╗ ██████╗ ███╗   ██╗ ██████╗ 
    ████╗ ████║██╔═══██╗████╗  ██║██╔═══██╗
    ██╔████╔██║██║   ██║██╔██╗ ██║██║   ██║
    ██║╚██╔╝██║██║   ██║██║╚██╗██║██║   ██║
    ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║╚██████╔╝
    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
    
    {Colors.WHITE}>> Device & Network Manager Framework <<
    {Colors.YELLOW}Version: 1.0 | Dev: Mamun (Natespo)
    {Colors.CYAN}---------------------------------------{Colors.END}""")

def main():
    auth = DeviceAuth()
    dm = DeviceManager()
    nm = NetworkMonitor()
    
    device_id = auth.generate_device_id(dm.get_info())
    session_token = auth.create_session(device_id)

    while True:
        show_banner()
        print(f"{Colors.MAGENTA}{Colors.BOLD}[ SESSION INFO ]{Colors.END}")
        print(f"Device ID : {device_id}")
        print(f"Token     : {session_token[:12]}...")
        print("-" * 39)
        
        print(f"\n{Colors.WHITE}1.{Colors.END} Device Info & Security Status")
        print(f"{Colors.WHITE}2.{Colors.END} Live Network Traffic (RX/TX)")
        print(f"{Colors.WHITE}3.{Colors.END} Local Network IP Scanner")
        print(f"{Colors.WHITE}4.{Colors.END} Educational Broadcast Info")
        print(f"{Colors.WHITE}5.{Colors.END} Exit MoNo Tool")
        
        choice = input(f"\n{Colors.GREEN}mono > {Colors.END}").strip()
        
        if choice == '1':
            info = dm.get_info()
            sec = dm.check_security()
            print(f"\n{Colors.CYAN}[+] Hardware & OS Info:{Colors.END}")
            for k, v in info.items(): print(f"    {k:<12}: {v}")
            
            print(f"\n{Colors.CYAN}[+] Security Metrics:{Colors.END}")
            for k, v in sec.items():
                status = f"{Colors.GREEN}SECURE" if v else f"{Colors.RED}OFF/LOW"
                print(f"    {k:<12}: {status}{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '2':
            print(f"\n{Colors.YELLOW}[*] Monitoring {nm.interface}... Press Ctrl+C to stop.{Colors.END}")
            try:
                while True:
                    stats = nm.get_stats()
                    sys.stdout.write(f"\r    {Colors.BOLD}Incoming:{Colors.END} {stats['RX']:,} bytes | {Colors.BOLD}Outgoing:{Colors.END} {stats['TX']:,} bytes")
                    sys.stdout.flush()
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Colors.CYAN}[!] Monitoring Stopped.{Colors.END}")
                time.sleep(1)

        elif choice == '3':
            hosts = nm.scan_network()
            print(f"\n{Colors.GREEN}[+] Discovery Complete! Active Hosts: {len(hosts)}{Colors.END}")
            for h in hosts:
                print(f"    - {h} (Active)")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '4':
            print(f"\n{Colors.BOLD}--- Educational Concepts ---{Colors.END}")
            print("1. Broadcast is sending data to all devices in a subnet.")
            print("2. IPv4 Broadcast address usually ends in .255")
            print("3. Legitimate use: DHCP requests, ARP discovery.")
            print("4. Security: Hijacking broadcasts can lead to MITM attacks.")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")

        elif choice == '5':
            print(f"\n{Colors.RED}[!] Closing MoNo Framework. Salam!{Colors.END}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Process Interrupted.{Colors.END}")
        sys.exit()
