# SentinelView: End-to-End IoT Cyber Threat Detection & Response System
**Sentinel** is a "Digital Nervous System" for network security. It bridges the gap between physical threat detection and enterprise response. By connecting a custom hardware edge device (Raspberry Pi Pico) to a cloud ecosystem, Sentinel turns a physical threat signature into an immediate Slack alert, a Salesforce incident ticket, and a live Tableau visualization in under 2 seconds.

---
## Repository Structure

```text
├── firmware/
│   ├── main.py          # logic for Raspberry Pi Pico (Edge sensor)
│   └── ssd1306.py       # you can install inside Thony
├── gateway/
│   └── gateway.py       # Python Service for Raspberry Pi Zero W (Bridge)
├── tableau/
│   └── Sentinel_Dashboard.twbx  # my pre-built Tableau Workbook
└── README.md
```
---
# System Architecture
This system operates in four distinct layers:
Edge Layer (Sensor): A Raspberry Pi Pico detects specific attack signatures via a keypad interface and displays status on an OLED screen.
Gateway Layer (Processor): A Raspberry Pi Zero W auto-detects the sensor over USB, parses the JSON threat data, and routes it to the cloud.

Cloud Layer (Storage & Logic):
- Supabase (PostgreSQL): Stores persistent audit logs of every attack.
- Make.com: Orchestrates instant alerts to Slack and Salesforce.

Action Layer (Visualization): Tableau Desktop connects via SSL to the database to render real-time threat velocity and risk scores.

---
# Hardware Prerequisites
```text
Component                                      Function
Raspberry Pi Pico,            The Edge Sensor simulating attacks.
Raspberry Pi Zero W,          The Gateway connecting hardware to the internet.
SSD1306 OLED (0.96""),        Visual feedback for the attacker/user.
4x4 Membrane Keypad,          Interface to trigger specific threat vectors.
Micro-USB Data Cable,         For connecting Pico to Pi Zero (Data transfer + Power).
```

---
# Phase 1: Cloud Infrastructure Setup
### Supabase (Database)
Sentinel uses a PostgreSQL database to store historical attack data for Tableau.
Create a free project at [Supabase](https://supabase.com/).
Go to the SQL Editor and run the following command to create the telemetry table:
```sql
CREATE TABLE telemetry (
    id SERIAL PRIMARY KEY,
    device_id TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    cpu_usage FLOAT,
    ram_usage FLOAT,
    threat_detected TEXT,
    risk_score INT
);
```
**Supabase database table:** <br>
<p align="center">
<img width="1866" height="1104" alt="image" src="https://github.com/user-attachments/assets/8ee50a86-28ba-4b3a-b1d0-17a0ea0108ee" />
</p>

**Critical** for Tableau: Go to Project Settings > Database > Connection Parameters.
Host: Copy the "Pooler" URL (e.g., aws-1-ap-southeast-1.pooler.supabase.com).
Port: You MUST use port 6543 (Transaction Pooler). The default 5432 will not work with Tableau live connections.
Password: Use the database password.

### Make.com (Automation)
Create a new Scenario in [Make.com](https://www.make.com/en/login).
Trigger: Add a Webhooks > Custom Webhook. Copy the URL (e.g., https://hook.eu1.make.com/...).
- Action 1: Slack > Create a Message. Map threat and risk to the message text.
- Action 2: Salesforce > Create a Record (Object: Case). Map fields to create an incident ticket.<br>
**[Important: Turn the "Scheduling" toggle to ON to ensure it runs automatically.]**<br>

**It should look something like this:** <br>
<p align="center">
<img width="1918" height="1097" alt="make" src="https://github.com/user-attachments/assets/3ef3c59e-bc98-476f-9202-67fc80e2ce4d" />
</p>

---
# Phase 2: Hardware Configuration (The Edge)
### Wiring Diagram (Pico)
- OLED Display: SDA -> GP0, SCL -> GP1, VCC -> 3.3V, GND -> GND.
- Keypad Rows (R1-R4): GP6, GP7, GP8, GP9.
- Keypad Cols (C1-C4): GP5, GP4, GP3, GP2.<br>

**Hardware setup:**
<p align="center">
<img src="https://github.com/user-attachments/assets/5a1fd2fa-1661-4aa6-b945-e38127879f04" alt="image" width="600" />
</p>

**Flashing the Firmware:** <br>
Connect the Raspberry Pi Pico to your computer holding the bootsel button.
Open Thonny IDE configure the interpreter and install the `ssd1306` driver from the manage packages tab.
Upload the contents of the firmware/ folder (main.py and ssd1306.py) to the Pico.
Run the script to verify the OLED screen turns on and displays the SentinelView dashboard.

---
# Phase 3: Gateway Configuration (The Bridge)
The Raspberry Pi Zero W runs a Python service to bridge the USB serial data to the Cloud API.

#### 1. System Prep
Run these commands on the Pi Zero terminal to install drivers and unlock the USB port:<br>

`sudo apt update`<br>
`sudo apt install python3-serial python3-requests python3-psycopg2 -y`<br>
**[Fix: Disable ModemManager which often blocks the Pico USB port:]**
```bash
sudo systemctl stop ModemManager
sudo systemctl disable ModemManager
sudo usermod -a -G dialout $USER
```
#### 2. Service Setup
Download the gateway/gateway.py file to your Pi Zero.
**[Edit the configuration at the top of the file:]**
```text
WEBHOOK_URL = "Paste_Your_Make_Webhook_URL_Here"
DB_USER = "postgres.your_project_user"
DB_PASS = "Your_Supabase_Database_Password"
Start the gateway:
sudo python3 gateway.py
```

---
# Phase 4: Data Visualization (The Action)
- Open Tableau Desktop.
- Connect to Data: Select PostgreSQL. You might have to install drivers which can be downloaded from the Tableau website.
- Enter Details:
```text
Server: Use the Supabase Pooler URL (from Phase 1).
Port: 6543 (Do not use 5432).
Database: postgres
SSL: Check "Require SSL".
```
- Build Dashboard:
```text
Drag created_at to Columns (Right-click -> Exact Date).
Drag risk_score to Rows.
Drag threat_detected to Color.
Go Live: Click the Refresh datasource button from the toolbar to see new attacks instantly.
```

---
### Video demonstration
You can check out the video demonstration of this project on YouTube [here](https://youtu.be/8qDUs-2xxes)

---
# Troubleshooting
These are the issues I faced, however if you encounter any other issues you can post in the repository discussions.<br>

Q: The Pi Zero says `"Access Denied"` to `/dev/ttyACM0` type of error message or you can't run the script.
A: This is usually caused by ModemManager hijacking the port. Run `sudo apt purge modemmanager` and `reboot`. Then check if the pico is listed using `ls /dev/tty*`.

Q: Tableau shows "Error Code: BC42EF73" or "Connection Refused".
A: You are likely using Port 5432. Change the port to 6543 in the connection settings. Also, ensure your WiFi network allows outbound traffic on non-standard ports (try a mobile hotspot if on Campus WiFi).

Q: Slack alerts work, but Tableau doesn't update.
A: Check your Python script output. If it says DB Logged, the data is there. In Tableau, you must hit the Refresh Data Source button (F5) manually to fetch the latest rows.

---
## LICENSE
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
