import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_ROM_DIR = ROOT / "gb-test-roms-master" / "cpu_instrs" / "individual"
RESULTS_DIR = ROOT / "results"
WAVE_DIR = RESULTS_DIR / "waveforms"
LOG_DIR = RESULTS_DIR / "logs"


def clean_output_dirs() -> None:
    shutil.rmtree(ROOT / "sim_build", ignore_errors=True)
    shutil.rmtree(WAVE_DIR, ignore_errors=True)
    shutil.rmtree(LOG_DIR, ignore_errors=True)
    WAVE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_name(name: str) -> str:
    cleaned = name.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "")
    return cleaned.replace("/", "_")


def collect_roms(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(target.glob("*.gb"))
    raise FileNotFoundError(f"ROM path not found: {target}")


def run_single_rom(rom_path: Path, timeout_seconds: int, waves: bool) -> bool:
    rom_name = sanitize_name(rom_path.stem)
    wave_path = WAVE_DIR / f"{rom_name}.ghw"
    log_path = LOG_DIR / f"{rom_name}.log"

    print(f"-> Simulating {rom_path.name}...", end=" ", flush=True)

    env = os.environ.copy()
    env.setdefault("TRACE_OPCODES", "0")
    env["PYTHONUNBUFFERED"] = "1"
    env["TEST_ROM"] = str(rom_path.resolve())
    env["WAVE_FILE"] = str(wave_path.resolve())
    env["WAVES"] = "1" if waves else "0"
    env.setdefault("MODULE", "blargg_test")

    try:
        with log_path.open("w") as log_file:
            result = subprocess.run(
                ["make", "sim"],
                cwd=ROOT,
                env=env,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                timeout=timeout_seconds,
            )
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return False

    if result.returncode == 0:
        print("OK")
        return True

    print("ERROR")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Blargg Game Boy CPU ROMs through cocotb.")
    parser.add_argument(
        "target",
        nargs="?",
        default=str(DEFAULT_ROM_DIR),
        help="Path to a single .gb ROM or a directory containing .gb files",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=2000,
        help="Per-ROM timeout in seconds",
    )
    parser.add_argument(
        "--waves",
        action = "store_true",
        help = "Enable GHDL waveform dumping",
        )
    args = parser.parse_args()

    # target = Path(args.target).resolve()
    target = "/Users/marouanehajri/PycharmProjects/Gboy_emulator/CPU/simulation/gb-test-roms-master/cpu_instrs/individual/11-op a,(hl).gb"
    target = Path(target)
    roms = collect_roms(target)
    if not roms:
        print(f"No ROMs found in {target}")
        return 1

    clean_output_dirs()

    failures = 0
    for rom_path in roms:
        if not run_single_rom(rom_path, args.timeout, args.waves):
            failures += 1

    print(f"\nDone. {len(roms) - failures}/{len(roms)} ROMs passed.")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
