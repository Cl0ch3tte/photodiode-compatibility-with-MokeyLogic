import csv
import time
import keyboard
from datetime import datetime

duree = 7200

name_file = "keyPressed_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

KEYS = {
    's': 'SYNC',
    '1': 'HORIZONTAL',
    '2': 'VERTICAL',
    '3': 'OTHER',
}

key_on = None
sync_ready = True

with open(name_file, 'w', newline='') as file:
    crea = csv.writer(file, delimiter=';')
    crea.writerow(["timestamp_pc", "key_pressed"])

    print("S = sync | 1 = horizontal | 2 = vertical | 3 = other | Esc= stop")

    debut = time.time()

    try:
        while time.time() - debut < duree:
            event = keyboard.read_event()
            if event.name == 'esc':
                break

            label = KEYS.get(event.name)
            if not label:
                continue

            if label == 'SYNC':
                if event.event_type == keyboard.KEY_DOWN and sync_ready:
                    ts = int(time.time() * 1_000_000)
                    crea.writerow([ts, label])
                    print(f"[{label}] @ {ts}µs")
                    sync_ready = False
                elif event.event_type == keyboard.KEY_UP:
                    sync_ready = True
            else:
                if event.event_type == keyboard.KEY_DOWN:
                    ts = int(time.time() * 1_000_000)
                    crea.writerow([ts, label])
                    print(f"[{label}] @ {ts}µs")

    except KeyboardInterrupt:
        print("Acquisition stopped by user.")

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        print(f"Acquisition finished. Data saved to {name_file}.")