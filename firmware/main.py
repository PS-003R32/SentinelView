from machine import Pin, SoftI2C
import time
import json
import ssd1306

i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=100000)
try:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
except:
    oled = None

rows = [Pin(x, Pin.OUT) for x in [6, 7, 8, 9]]
cols = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in [5, 4, 3, 2]]

keys = [
    ['1', '2', '3', 'Syn Scan'], 
    ['4', '5', '6', 'SSH Brute'], 
    ['7', '8', '9', 'Malware'], 
    ['*', '0', '#', 'Clear']
]

ATTACK_MAP = {
    '1': ('Port Scan', 25),
    '2': ('SQL Injection', 85),
    '3': ('XSS Attack', 45),
    '4': ('MITM Attack', 75),
    '5': ('DDoS Attempt', 90),
    '6': ('Brute Force', 60),
    '7': ('Rootkit', 95),
    '8': ('Ransomware', 99),
    '9': ('Botnet Traffic', 55),
    '0': ('Ping Sweep', 10),
    'Syn Scan': ('Syn Flood', 40),
    'SSH Brute': ('SSH Crack', 70),
    'Malware': ('Trojan', 95)
}

def scan_keypad():
    for r_idx, r in enumerate(rows):
        r.value(1)
        for c_idx, c in enumerate(cols):
            if c.value():
                r.value(0)
                time.sleep(0.2) 
                return keys[r_idx][c_idx]
        r.value(0)
    return None

def update_display(status, risk):
    if oled:
        oled.fill(0)
        oled.text("SENTINEL ACTIVE", 0, 0)
        oled.text(f"Threat: {status}", 0, 20)
        oled.text(f"Risk: {risk}", 0, 40)
        oled.show()

print("System Ready...")
update_display("WAITING...", 0)

while True:
    key = scan_keypad()
    if key:
        if key in ATTACK_MAP:
            threat_name, risk_score = ATTACK_MAP[key]
        else:
            threat_name, risk_score = ("Unknown", 0)

        update_display(threat_name, risk_score)
        
        payload = {"threat": threat_name, "risk": risk_score}
        print(json.dumps(payload))