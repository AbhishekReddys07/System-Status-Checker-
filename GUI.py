import tkinter as tk
import subprocess
import platform
import os

def fireReader(system_name):
    file_path = "please Enter requrements.txt path here"
    try:
        with open(file_path, 'r') as f:
            for line in f:
                list_items = line.split(',')
                if len(list_items) > 1 and list_items[0].strip().lower() == system_name.lower():
                    ip_address = list_items[1].strip().replace("ip", "").replace(":", "").strip()
                    return ip_address
            print("System not found")
            result_label.config(text="Could not find system", fg="purple")
    except IOError as e:
        print(f"An error occurred: {e}")
        return None

def check_device_status(ip_address):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        response = subprocess.check_output(['ping', param, '1', ip_address], timeout=5)
        return True  # Device is reachable (on)
    except subprocess.CalledProcessError:
        return False  # Device is not reachable (off)
    except Exception as e:
        # Assume device is off if an error occurs
        print(f"Error occurred while checking device status: {e}")
        return False 

def send_signal(mac_address):
    print(f"Sending signal to MAC address: {mac_address}")

def sendRestartSignal(ip_address):
    file_path = "please Enter requrements.txt path here"
    try:
        with open(file_path, 'r') as f:
            for line in f:
                list_items = line.split(',')
                if len(list_items) > 2 and list_items[1].strip().replace("ip", "").replace(":", "").strip() == ip_address:
                    mac_address = list_items[2].strip().replace("mac", "").replace(":", "").strip()
                    print("Cleaned MAC Address:", mac_address)
                    send_signal(mac_address)
                    username = username_entry.get()
                    password = password_entry.get()
                    restart_remote_machine(ip_address, username, password)
                    result_label.config(text=f"Signal sent to MAC: {mac_address}", fg="green")
                    return mac_address
            print("IP address not found")
            result_label.config(text="IP address not found", fg="purple")
    except IOError as e:
        print(f"An error occurred: {e}")
        return None

def get_ip_from_mac(mac_address):
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    
    for line in lines:
        if mac_address in line:
            parts = line.split()
            ip_address = parts[0]
            return ip_address
    return None

def restart_remote_machine(ip_address, username, password):
    command = f"shutdown /r /m \\\\{ip_address} /t 0 /f"
    subprocess.run(['net', 'use', f'\\\\{ip_address}', '/user:' + username, password], capture_output=True)
    subprocess.run(command, shell=True)

def button_clicked():
    enter_value = system_name_entry.get()
    ip_address = fireReader(enter_value)
    if ip_address:
        if check_device_status(ip_address):
            result_label.config(text="Device is online", fg="green")
        else:
            result_label.config(text="Device is offline", fg="red")
            username_label.pack(padx=20, pady=10)
            username_entry.pack()
            password_label.pack(padx=20, pady=10)
            password_entry.pack()
            send_label.config(text="Restart Device", command=lambda: sendRestartSignal(ip_address))
            send_label.pack(padx=10, pady=10)

root = tk.Tk()
root.geometry("400x400")
root.title("Device Manager")

label = tk.Label(root, text="Enter system name", font=('Arial', 10))
label.pack(padx=20, pady=10)

system_name_entry = tk.Entry(root)
system_name_entry.pack()

username_label = tk.Label(root, text="Enter your username", font=('Arial', 10))
username_entry = tk.Entry(root)

password_label = tk.Label(root, text="Enter your password", font=('Arial', 10))
password_entry = tk.Entry(root, show="*")

button = tk.Button(root, 
                   text="Check device status", 
                   command=button_clicked,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 8),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=20,
                   wraplength=100)
button.pack(padx=10, pady=20)

result_label = tk.Label(root, text="", font=('Arial', 10))
result_label.pack(padx=20, pady=20)

send_label = tk.Button(root, text="", font=('Arial', 10), command=lambda: None)
send_label.pack_forget()
root.mainloop()
