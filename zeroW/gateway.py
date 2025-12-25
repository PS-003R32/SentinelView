import serial
import time
import json
import psutil
import psycopg2
from datetime import datetime
import sys
import serial.tools.list_ports
import requests

WEBHOOK_URL = "https://hook.eu1.make.com/" #you insert yoursd

DB_HOST = "aws-x-xx-xxxxxxxx-1.xxxxx.supabase.com"#you insert yoursd
DB_PORT = "xxxx"#you insert yoursd, usualy 6543
DB_NAME = "xxxxxxx"#you insert yoursd
DB_USER = "postgres.xxxxxxxxxxxx"#you insert yoursd
DB_PASS = "passwd"#you insert yoursd 

DEVICE_ID = "SENTINEL-ZERO-01"

print(f"Sentinel Gateway Starting...")

def find_pico():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "ACM" in p.device or "USB" in p.device: return p.device
    return None

port = find_pico()
if not port:
    print("Error: No Pico found. Check USB cable.")
    sys.exit(1)

print(f"Connecting to Pico at {port}...")

try:
    ser = serial.Serial(port, 115200, timeout=1)
    ser.flush()
except Exception as e:
    print(f"Access Denied: {e}")
    sys.exit(1)

print("System Active. Waiting for attacks...")