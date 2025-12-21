import serial
import time
import json
import psutil
import psycopg2
from datetime import datetime

SERIAL_PORT='/dev/serial0'
BAUD_RATE=9600
DEVICE_ID='RPI-ZERO-SEC-01'

