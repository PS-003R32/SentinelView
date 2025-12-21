import serial
import time
import json
import psutil
import psycopg2
from datetime import datetime

SERIAL_PORT='/dev/serial0'
BAUD_RATE=9600
DEVICE_ID='RPI-ZERO-SEC-01'

DB_URI = "postgresql://postgres:190503@db.qhzlenfzebrrahmnngty.supabase.co:5432/postgres"

def get_db_connection():
  try:
    conn = psycopg2.connect(DB_URI)
    return conn
  except Exception as e:
    print(f"DB Connection Error: {e}")
    return None
def calculate_risk(threat, cpu):
    base_score = 0
    if threat == "Syn Scan": base_score = 30
    elif threat == "SSH Brute Force": base_score = 60
    elif threat == "Malware Beacon": base_score = 90

    cpu_factor = 10 if cpu > 80 else 0
    return min(100, base_score + cpu_factor)
  