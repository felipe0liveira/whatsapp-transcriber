import subprocess
import time
import os
import psutil

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

def get_cpu_stats():
    # Obtém uso de CPU (%) e memória RAM
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    return cpu_percent, memory.used // (1024**2), memory.total // (1024**2)  # Convertendo para MiB

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
            gpu_util, gpu_mem_used, gpu_mem_total = get_gpu_stats()
            cpu_util, ram_used, ram_total = get_cpu_stats()
            
            os.system("clear")  # use "cls" se for Windows
            print("📊 System Monitoring (Ctrl+C to stop)\n")
            
            # CPU Stats
            print("🖥️  CPU:")
            print(f"   Usage:       {progress_bar(cpu_util)}")
            print(f"   RAM Usage:   {progress_bar(ram_used, ram_total, show_percentage=False, unit=' MiB')}")
            
            print()
            
            # GPU Stats
            print("🎮 GPU:")
            if gpu_util is not None:
                print(f"   Usage:       {progress_bar(gpu_util)}")
                print(f"   VRAM Usage:  {progress_bar(gpu_mem_used, gpu_mem_total, show_percentage=False, unit=' MiB')}")
            else:
                print("   No NVIDIA GPU detected or nvidia-smi not available")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✅ Monitoring finished.")
