import subprocess
import time
import os

def get_gpu_stats():
    # Consulta uso de GPU (%) e memória (MiB)
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode == 0:
        gpu_util, mem_used, mem_total = result.stdout.strip().split(", ")
        return int(gpu_util), int(mem_used), int(mem_total)
    else:
        return None, None, None

def progress_bar(value, total=100, length=30, show_percentage=True, unit=""):
    filled = int(length * value / total)
    bar = "█" * filled + "░" * (length - filled)
    
    if show_percentage:
        percentage = (value / total) * 100
        return f"[{bar}] {percentage:.1f}%"
    else:
        return f"[{bar}] {value}{unit} / {total}{unit}"

if __name__ == "__main__":
    try:
        while True:
            gpu_util, mem_used, mem_total = get_gpu_stats()
            os.system("clear")  # use "cls" se for Windows
            print("📊 Monitoring GPU Usage (Ctrl+C to stop)\n")
            if gpu_util is not None:
                print(f"GPU Usage:    {progress_bar(gpu_util)}")
                print(f"Memory Usage: {progress_bar(mem_used, mem_total, show_percentage=False, unit=' MiB')}")
            else:
                print("Error while reading nvidia-smi")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✅ Monitoring finished.")
