import tkinter as tk
import subprocess
import platform
import socket
from PIL import Image, ImageTk
import threading

def fireReader(system_name):
    """
    this function opens the file and searches for the Ip address. if needed add BD for fetching IP address 
    """
    file_path = "Enter path "
    try:
        with open(file_path, 'r') as f:
            for line in f:
                list_items = line.split(',')
                if len(list_items) > 1 and list_items[0].strip().lower() == system_name.lower():
                    ip_address = list_items[1].strip().replace("ip", "").replace(":", "").strip()
                    return ip_address
            result_label.config(text="Could not find system", fg="purple")
    except IOError as e:
        print(f"An error occurred: {e}")
        result_label.config(text=f"An error occurred: {e}", fg="red")
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

def create_magic_packet(mac_address: str) -> bytes:
    mac_address = mac_address.replace(":", "").replace("-", "").replace(".", "")
    if len(mac_address) != 12:
        raise ValueError("MAC address should be 12 hex digits")

    mac_bytes = bytes.fromhex(mac_address)
    magic_packet = bytes([0xFF] * 6) + mac_bytes * 16
    result_label.config(text="Created magic packet", fg="green")
    
    return magic_packet

def send_magic_packet(mac_address: str, ip_address: str = '255.255.255.255', port: int = 9):
    magic_packet = create_magic_packet(mac_address)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (ip_address, port))
        print(f"Magic packet sent to {mac_address} via {ip_address}:{port}")
        result_label.config(text=f"Sending magic packet to {mac_address}", fg="green")

def send_signal(mac_address):
    print(mac_address)
    status_message = f"Waiting to send signal to MAC address: {mac_address}"
    result_label.config(text=status_message, fg="green")
    send_magic_packet(mac_address)
    root.configure(bg="green")

def sendRestartSignal(ip_address):
    file_path = "Enter path here"
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
            result_label.config(text="IP address not found", fg="purple")
    except IOError as e:
        print(f"An error occurred: {e}")
        result_label.config(text=f"An error occurred: {e}", fg="red")
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

def reset_gui():
    result_label.config(text="")
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_frame.pack_forget()
    send_label.pack_forget()
    root.configure(bg="white")

def button_clicked():
    reset_gui()
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
            password_frame.pack()
            send_label.config(text="Restart Device", command=lambda: sendRestartSignal(ip_address))
            send_label.pack(padx=10, pady=10)

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        eye_button.config(text='👁️')
    else:
        password_entry.config(show='*')
        eye_button.config(text='👁')

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

password_frame = tk.Frame(root)
password_entry = tk.Entry(password_frame, show="*", font=('Arial', 10))
password_entry.pack(side=tk.LEFT)

eye_button = tk.Button(password_frame, text='👁️', command=toggle_password, font=('Arial', 10))
eye_button.pack(side=tk.LEFT)

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

if __name__=="__main__":root.mainloop()
