import serial
import csv
import time
from datetime import datetime

port = "COM3"
baud = 115200
duree = 7200

name_file = "get_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv" #add full path in front of get_ to save it in chosen place

arduino = serial.Serial(port, baud, timeout=0.01)
time.sleep(2)

with open(name_file, 'w', newline='') as file:
    crea = csv.writer(file, delimiter=';')
    crea.writerow(["timestamp_arduino", "etat", "timestamp_pc"])

    debut = time.time()

    try:
        while time.time() - debut < duree:
            line = arduino.readline().decode('utf-8', errors='ignore').strip()
            if "," in line:
                parties = line.split(",")
                if len(parties) >= 2:
                    timestamp = parties[0]
                    etat = parties[1]
                    ts_pc = int(time.time() * 1_000_000)
                    crea.writerow([timestamp, etat, ts_pc])
                    print(f"Timestamp: {timestamp}µs, Etat: {etat}")

    except KeyboardInterrupt:
        print("Acquisition stopped by user.")

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        arduino.close()
        print(f"Acquisition finished. Data saved to {name_file}.")