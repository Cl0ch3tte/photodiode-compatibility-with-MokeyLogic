# photodiode-compatibility-with-MokeyLogic

Open-hardware photodiode circuit that generates sub-millisecond event markers
synchronized with on-screen visual stimuli on a 144Hz display, designed to
complement eye-tracking data collected with MonkeyLogic.

# Overview
The detector converts a light signal into an electrical signal using a
photodiode and a transimpedance amplifier (TIA), then compares it to an
adjustable threshold to produce a clean logic signal. An Arduino timestamps
this signal in microseconds and streams it over USB serial; a Python script
logs it to CSV, which can then be merged with keyboard-generated event
markers for full experimental synchronization.

# Hardware

- **Photodiode:** SFH206K
- **Amplifier:** LM358 (single dual op-amp: one stage as TIA, one as
  threshold comparator with hysteresis)
- **Supply:** single 5V rail
- **Output:** BNC (analog) + digital logic line to the Arduino

Full schematic, component justification, and bill of materials are in
[`docs/Dossier_de_conception.pdf`](docs/Dossier_de_conception.pdf).

## Firmware

The Arduino reads the comparator's digital output, timestamps it with
`micros()`, and writes `timestamp,state` lines over USB serial at 115200
baud.

## Software

`acquisition_pcclock.py` logs the Arduino stream to a timestamped CSV.
`merge_file_auto.py` aligns and merges the Arduino CSV with a keyboard
marker CSV (useful when acquisition runs across two separate PCs), using a
shared SYNC marker as the time reference.


## Getting started

1. Build the circuit following the schematic
2. Flash 'test_arduino.ino' to the Arduino.
3. Run `acquisition_pcclock.py` to start logging.
4. Use `merge_file_auto.py` if combining with keyboard event markers.

Chloé Lapaquellerie — BUT GEII, IUT Lyon 1
Internship at INSERM SBRI Lyon, Dehay team (Cerebral Cortex and Connectome)
