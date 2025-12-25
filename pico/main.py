from machine import Pin, SoftI2C
import time
import json
import ssd1306

i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=100000)

print("Initializing OLED...")
try:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
    print("OLED Success!")
except Exception as e:
    print(f"Error: {e}")
    oled = None


rows = [Pin(x, Pin.OUT) for x in [6, 7, 8, 9]]
cols = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in [5, 4, 3, 2]]

keys = [
    ['1', '2', '3', 'Syn Scan'], 
    ['4', '5', '6', 'SSH Brute'], 
    ['7', '8', '9', 'Malware'], 
    ['*', '0', '#', 'Clear']
]

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
        oled.text("SENTINEL VIEW", 0, 0)
        oled.text("Threat:", 0, 20)
        oled.text(status[:16], 0, 30)
        oled.text(f"Risk: {risk}", 0, 50)
        oled.show()




print("Pico Active on USB...")
update_display("Waiting...", 0)

while True:
    key = scan_keypad()
    if key:
        risk = 0
        if key == 'Syn Scan': risk = 35
        elif key == 'SSH Brute': risk = 65
        elif key == 'Malware': risk = 95
        
        update_display(key, risk)
        
        payload = {"threat": key, "risk": risk}
        print(json.dumps(payload))
