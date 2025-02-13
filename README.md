## Wake-on-LAN Automation Tool with GUI
A user-friendly GUI-based Wake-on-LAN (WoL) automation tool that enables remote system wake-up and restart with real-time status updates.

**Features**
Intuitive GUI for easy device selection and control.
Supports file-based and database-based device information retrieval.
Displays real-time status updates (online/offline).
Password protection for remote restarts.
Uses Wake-on-LAN (WoL) magic packets to power on remote devices.
Technologies Used
Python
Tkinter (GUI)
SQLite3 (Database interaction)
subprocess (System commands)
socket (Network communication)
Installation & Setup
1. **Install Dependencies**
Ensure you have Python installed, then install required dependencies:
pip install tk sqlite3
2. **Configure Database (Optional)**
If using a database, modify GUI.py to connect to the correct SQLite database.
Update file paths and database configurations as needed.
3.**Run the Application**
python GUI.py
Usage Instructions
Enter the system name in the input field.
Click "Check device status" to verify if the device is online or offline.
If offline, enter username & password, then click "Restart Device" to send a WoL signal.
Code Structure
GUI.py → Main Tkinter GUI with system checks and restart functionality.
Database Integration → Fetches system details if a local database is available.
WoL Magic Packet → Constructs and sends magic packets to wake devices.
**Disclaimer**
This project is for educational and demonstration purposes only. Use with proper authorization before remotely powering on any device.

