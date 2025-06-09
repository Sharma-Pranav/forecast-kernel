import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
MAX_BYTES = 500 * 1024 * 1024  # 500 MB
LOG_PATH = "data/logs/storage_check.log"

def get_total_size(directory):
    total = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
    return total

def main():
    monitored_dirs = ["data", "data/outputs"]
    total = sum(get_total_size(d) for d in monitored_dirs if os.path.exists(d))

    with open(LOG_PATH, "w") as f:
        f.write(f"Total storage used: {total / (1024 * 1024):.2f} MB\n")
        if total > MAX_BYTES:
            f.write("Storage exceeds 500MB limit.\n")
            raise RuntimeError("Exceeded 500MB limit.")
        else:
            f.write("Storage within safe bounds.\n")

if __name__ == "__main__":
    main()