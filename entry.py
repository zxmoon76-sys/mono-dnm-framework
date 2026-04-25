import csv
import re
import os
import hashlib
from datetime import datetime

# --- Configuration & Storage ---
GENERAL_FILE = "general_records.csv"
BILLING_FILE = "accounting_records.csv"
PASS_FILE = ".secret_pass.txt"

# --- Utility Functions ---
def clear_screen():
    os.system('clear')

def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def format_currency(amount):
    """টাকার অংককে কমা ফরম্যাটে সাজানো (যেমন: 1,234,567.00)"""
    return "{:,.2f}".format(amount)

def banner():
    CYAN = "\033[1;36m"
    GREEN = "\033[1;32m"
    WHITE = "\033[1;37m"
    RESET = "\033[0m"
    print(rf"""
{CYAN}██████╗  █████╗ ████████╗ █████╗ 
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
██║  ██║███████║   ██║   ███████║
██║  ██║██╔══██║   ██║   ██╔══██║
██████╔╝██║  ██║   ██║   ██║  ██║
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
{GREEN}       MASTER DATA ENTRY TOOL v3.0 (PRO)
{WHITE}        Developed by: MAMUN
{RESET}""")

# --- Security ---
def check_password():
    clear_screen()
    banner()
    if not os.path.exists(PASS_FILE):
        print("\033[1;33m[!] Welcome, Mamun! Setup your first security password.\033[0m")
        new_pass = input("Set Password: ").strip()
        with open(PASS_FILE, "w") as f: f.write(get_hash(new_pass))
        print("\033[1;32m[+] Password set successfully!\033[0m")
    
    with open(PASS_FILE, "r") as f: saved_hash = f.read()
    print("\033[1;34m--- Security Check (User: Mamun) ---\033[0m")
    attempt = input("Enter Password: ").strip()
    return get_hash(attempt) == saved_hash

# --- Validation ---
def validate_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 10

# --- Modules ---
def general_entry():
    while True:
        clear_screen()
        banner()
        print("\033[1;35m[ 1. General Data Entry ]\033[0m")
        name = input("Full Name: ").strip()
        email = input("Email: ").strip()
        if not validate_email(email):
            print("Error: Invalid Email!"); input("Retry..."); continue
        phone = input("Phone: ").strip()
        if not validate_phone(phone):
            print("Error: Invalid Phone!"); input("Retry..."); continue
        address = input("Address: ").strip()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if input("\nSave this entry? (y/n): ").lower() == 'y':
            exists = os.path.isfile(GENERAL_FILE)
            with open(GENERAL_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not exists:
                    writer.writerow(["Time", "Name", "Email", "Phone", "Address"])
                writer.writerow([timestamp, name, email, phone, address])
            print("\033[1;32m[+] Successfully Saved!\033[0m")
        if input("\nAdd another? (y/n): ").lower() != 'y': break

def billing_entry():
    while True:
        clear_screen()
        banner()
        print("\033[1;35m[ 2. Professional Billing Mode ]\033[0m")
        item = input("Item Name: ").strip()
        try:
            price = float(input("Unit Price: "))
            qty = int(input("Quantity: "))
            disc_pct = float(input("Discount (%): "))
        except ValueError:
            print("Error: Enter valid numbers!"); input("Retry..."); continue

        gross = price * qty
        disc_amt = gross * (disc_pct / 100)
        net = gross - disc_amt

        print(f"\n\033[1;33m--- Invoice Summary ---")
        print(f"Item        : {item}")
        print(f"Gross Total : {format_currency(gross)}")
        print(f"Discount    : -{format_currency(disc_amt)} ({disc_pct}%)")
        print(f"Net Payable : {format_currency(net)}")
        print(f"-----------------------\033[0m")
        
        if input("\nConfirm and Save? (y/n): ").lower() == 'y':
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exists = os.path.isfile(BILLING_FILE)
            with open(BILLING_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not exists:
                    writer.writerow(["Time", "Item", "Price", "Qty", "Gross", "Net"])
                writer.writerow([timestamp, item, price, qty, format_currency(gross), format_currency(net)])
            print("\033[1;32m[+] Billing Saved Successfully!\033[0m")
        if input("\nNext item? (y/n): ").lower() != 'y': break

def view_data():
    clear_screen()
    banner()
    print("1. View General Info | 2. View Billing Records")
    ch = input("Select Option: ")
    target = GENERAL_FILE if ch == '1' else BILLING_FILE
    if os.path.exists(target):
        with open(target, 'r') as f:
            print("\n" + "="*50 + "\n" + f.read() + "="*50)
    else: print("No records found.")
    input("\nPress Enter to return...")

def search_data():
    clear_screen()
    banner()
    print("1. Search People | 2. Search Billing")
    ch = input("Where to search? ")
    query = input("Enter keyword (Name/Item): ").lower()
    target = GENERAL_FILE if ch == '1' else BILLING_FILE
    
    if os.path.exists(target):
        print(f"\n--- Results for '{query}' ---")
        with open(target, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if query in str(row).lower():
                    print(" | ".join(row))
    else: print("File not found.")
    input("\nPress Enter to return...")

# --- Main Program ---
def main():
    if not check_password(): 
        print("\033[1;31m[!] Wrong Password. Access Denied!\033[0m")
        return

    while True:
        clear_screen()
        banner()
        print(f"\033[1;37mWelcome Mamun! What's your task today?\033[0m")
        print("-" * 40)
        print("1. Add New General Data")
        print("2. Add New Billing/Accounts")
        print("3. View Saved Records")
        print("4. Search Specific Data")
        print("5. Reset Security Password")
        print("6. Exit Tool")
        
        choice = input("\nSelect (1-6): ")
        
        if choice == '1': general_entry()
        elif choice == '2': billing_entry()
        elif choice == '3': view_data()
        elif choice == '4': search_data()
        elif choice == '5':
            if input("Are you sure? This will delete current pass (y/n): ") == 'y':
                os.remove(PASS_FILE)
                print("Password deleted. Restarting..."); break
        elif choice == '6':
            print("Goodbye Mamun!"); break
        else:
            print("Invalid Choice!"); input("Enter to retry...")

if __name__ == "__main__":
    main()
