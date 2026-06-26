import csv
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

try:
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("Choisis le fichier Arduino...")
    arduino_file = filedialog.askopenfilename(
        parent=root,
        title="Choisis le fichier Arduino (get_*.csv)",
        initialdir=script_dir,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not arduino_file:
        print("Aucun fichier Arduino sélectionné, arrêt.")
        exit()

    print("Choisis le fichier Keys...")
    keys_file = filedialog.askopenfilename(
        parent=root,
        title="Choisis le fichier Keys (keyPressed_*.csv)",
        initialdir=script_dir,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not keys_file:
        print("Aucun fichier Keys sélectionné, arrêt.")
        exit()

    print(f"Arduino file name : {os.path.basename(arduino_file)}")
    print(f"Keys file name : {os.path.basename(keys_file)}")

    # essaye de récupérer la date depuis le nom du fichier Arduino (ex: get_2026-06-17_14-22-02.csv)
    arduino_basename = os.path.basename(arduino_file)
    try:
        date_part = arduino_basename.split('_', 1)[1].replace('.csv', '')  # 2026-06-17_14-22-02
    except IndexError:
        date_part = "session"
    default_name = f"merge_{date_part}"

    # demande le nom du fichier de sortie via une popup texte
    root.attributes('-topmost', True)
    root.focus_force()
    merge_name = simpledialog.askstring(
        "Nom du fichier merge",
        "Nom du fichier de sortie (sans .csv) :",
        initialvalue=default_name,
        parent=root
    )
    if not merge_name:
        merge_name = default_name
    if not merge_name.lower().endswith('.csv'):
        merge_name += '.csv'

    arduino_rows = []
    keys_rows = []

    with open(arduino_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            arduino_rows.append({
                'timestamp_pc': int(row['timestamp_pc']),
                'timestamp_arduino': row['timestamp_arduino'],
                'etat': row['etat'],
            })
    print(f"-> {len(arduino_rows)} lignes Arduino lues.")

    with open(keys_file, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            keys_rows.append({
                'timestamp_pc': int(row['timestamp_pc']),
                'key_pressed': row['key_pressed'],
            })
    print(f"-> {len(keys_rows)} lignes Keys lues.")

    # find SYNC
    sync_reference = None
    for row in keys_rows:
        if row['key_pressed'] == 'SYNC':
            sync_reference = row['timestamp_pc']
            break

    if sync_reference is None:
        print("Error: no SYNC found.")
        exit()
    print(f"-> SYNC trouvé à timestamp_pc = {sync_reference}")

    # offset everything to SYNC
    for row in arduino_rows:
        row['timestamp_pc'] = row['timestamp_pc'] - sync_reference
    for row in keys_rows:
        row['timestamp_pc'] = row['timestamp_pc'] - sync_reference

    # remove arduino rows before SYNC
    arduino_rows = [row for row in arduino_rows if row['timestamp_pc'] >= 0]
    print(f"-> {len(arduino_rows)} lignes Arduino après SYNC.")

    # propagate last known key to each arduino row
    current_key = ''
    key_index = 0

    result = []
    for row in arduino_rows:
        while key_index < len(keys_rows) and keys_rows[key_index]['timestamp_pc'] <= row['timestamp_pc']:
            if keys_rows[key_index]['key_pressed'] != 'SYNC':
                current_key = keys_rows[key_index]['key_pressed']
            key_index += 1
        result.append({
            'timestamp_pc': row['timestamp_pc'],
            'timestamp_arduino': row['timestamp_arduino'],
            'etat': row['etat'],
            'key_pressed': current_key,
        })

    merge_path = os.path.join(script_dir, merge_name)
    with open(merge_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, delimiter=';', fieldnames=['timestamp_pc', 'timestamp_arduino', 'etat', 'key_pressed'])
        writer.writeheader()
        writer.writerows(result)

    print(f"\nMerge file created — {len(result)} rows. ({merge_path})")

except Exception as e:
    import traceback
    print("\n--- ERREUR ---")
    traceback.print_exc()

input("\nAppuie sur Entrée pour fermer...")
