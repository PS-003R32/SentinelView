# SentinelView: End-to-End IoT Cyber Threat Detection & Response System
**Sentinel** is a "Digital Nervous System" for network security. It bridges the gap between physical threat detection and enterprise response. By connecting a custom hardware edge device (Raspberry Pi Pico) to a cloud ecosystem, Sentinel turns a physical threat signature into an immediate Slack alert, a Salesforce incident ticket, and a live Tableau visualization in under 2 seconds.

---
## Repository Structure

```text
├── firmware/
│   ├── main.py          # logic for Raspberry Pi Pico (Edge sensor)
│   └── ssd1306.py       # OLED Display Driver,you can install inside Thony(this is just for reference
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
**Critical** for Tableau: Go to Project Settings > Database > Connection Parameters.
Host: Copy the "Pooler" URL (e.g., aws-1-ap-southeast-1.pooler.supabase.com).
Port: You MUST use port 6543 (Transaction Pooler). The default 5432 will not work with Tableau live connections.
Password: Use the database password.

### Make.com (Automation)
Create a new Scenario in [Make.com](https://www.make.com/en/login).
Trigger: Add a Webhooks > Custom Webhook. Copy the URL (e.g., https://hook.eu1.make.com/...).
- Action 1: Slack > Create a Message. Map threat and risk to the message text.
- Action 2: Salesforce > Create a Record (Object: Case). Map fields to create an incident ticket.

**[Important: Turn the "Scheduling" toggle to ON to ensure it runs automatically.]**

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
