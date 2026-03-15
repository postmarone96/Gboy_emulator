import csv
import os
import subprocess
import shutil

if os.path.exists("sim_build"):
    shutil.rmtree("sim_build")

if os.path.exists("results/logs"):
    shutil.rmtree("results/logs")

if os.path.exists("results/waveforms"):
    shutil.rmtree("results/waveforms")

os.makedirs("results/waveforms", exist_ok=True)
os.makedirs("results/logs", exist_ok=True)


def run_single_opcode_sim(opcode_hex, label):
    # Dateiname für die Waveform säubern
    clean_label = label.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "").replace("/", "_")
    clean_label = clean_label[:-3]
    wave_path = os.path.abspath(f"results/waveforms/{opcode_hex}_{clean_label}.ghw")
    log_path = os.path.abspath(f"results/logs/{opcode_hex}.log")

    print(f"-> Simuliere Opcode {opcode_hex} ({label[:-3]})...", end=" ", flush=True)

    # Environment variables for Makefile and test_cpu.py
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["TEST_OPCODE"] = opcode_hex
    env["WAVE_FILE"] = wave_path

    # run Makefile
    try:
        with open(log_path, "w") as f:
            result = subprocess.run(
                ["make", "sim"],
                env=env,
                stdout=f,
                stderr=f,
                timeout=30  # Falls die Simulation in einem Loop hängen bleibt
            )

        if result.returncode == 0:
            print("OK")
        else:
            print("ERROR (Check logs/)")
    except subprocess.TimeoutExpired:
        print("TIMEOUT")


# 2. read csv and start simulation
def start_suite(csv_file):
    processed_opcodes = set()

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            op = row['Opcode']
            if op not in processed_opcodes:
                run_single_opcode_sim(op, row['Label'])
                processed_opcodes.add(op)


if __name__ == "__main__":
    print("=== SM83 Opcode Simulation Runner ===")
    start_suite('../../microcode/microcode.csv')
    print("\nDone! Alle Waves under 'results/waveforms/'")
