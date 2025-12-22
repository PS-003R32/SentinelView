import serial
import time
import json
import psutil
import psycopg2
from datetime import datetime

SERIAL_PORT='/dev/serial0'
BAUD_RATE=9600
DEVICE_ID='RPI-ZERO-SEC-01'

DB_URI = "postgresql://postgres:@db."

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
def main():
   print("Starting Gateway...")
   ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
   current_threat = "None"

   while True:
      try:
        if ser.in_waiting > 0:
          line=ser.readline().decode('utf-8').strip()
          try:
            data = json.loads(line)
            current_threat = data.get("threat", "None")
            print(f"Update recieved: {current_threat}")
          except json.JSONDecodeError:
            pass
        cpu=psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        risk = calculate_risk(current_threat, cpu)

        conn = get_db_connection()
        if conn:
          cur= conn.cursor()
          cur.execute("""
                      INSERT INTU telemetry (device_id, cpu_usage, ram_usage, threat_detected, risk_score) VALUES (%s,%s,%s,%s,%s)""", (DEVICE_ID, cpu,ram, current_threat, risk))
          conn.commit()
          cur.close()
          conn.close()
          print(f"Logged: {current_threat} | Risk: {risk}")
        time.sleep(2)
      except Exception as e:
        print(f"Loop Error: {e}")
        time.sleep(1)
if __name__=='__main__':
  main()
         