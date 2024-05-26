import tkinter as tk
import subprocess
import platform

def fireReader(system_name):
    file_path = "Please enter Requrements.txt path here"
    try:
        with open(file_path, 'r') as f:
            found_system = False
            for line in f:
                list_items = line.split(',')
                if list_items[0].strip() == system_name:
                    found_system = True
                    ip_address = list_items[1].strip()
                    cleaned_ip = ip_address.replace("ip", "").replace(":", "").strip()
                    print(cleaned_ip)
                    return cleaned_ip
            if not found_system:
                print("System not found")
                result_label.config(text="Could not find system", fg="purple")
    except IOError as e:
        print(f"An error occurred: {e}")
        return None
    
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

def button_clicked():
    enter_value = myentry.get()
    ip_address = fireReader(enter_value)
    if ip_address:
        if check_device_status(ip_address):
            result_label.config(text="Device is online", fg="green")
        else:
            result_label.config(text="Device is offline", fg="red")

root = tk.Tk()
root.geometry("300x300")
root.title("Sender")

label = tk.Label(root, text="Enter system name", font=('Arial', 10))
label.pack(padx=20, pady=20)

myentry = tk.Entry(root)
myentry.pack()

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
                   width=15,
                   wraplength=100)
button.pack(padx=10, pady=10)

result_label = tk.Label(root, text="", font=('Arial', 10))
result_label.pack(padx=20, pady=20)

root.mainloop()
