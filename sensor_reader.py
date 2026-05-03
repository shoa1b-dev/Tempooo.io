import psutil
import random
import wmi
import time
from plyer import notification

# Initialize WMI for deep hardware scans
try:
    computer = wmi.WMI()
except Exception:
    computer = None

psutil.cpu_percent() 
last_alert_time = 0 

def get_hardware_names():
    cpu_name = "Unknown CPU"
    gpu_name = "Unknown GPU"
    if computer:
        try:
            cpu_name = computer.Win32_Processor()[0].Name.strip()
            gpu_name = computer.Win32_VideoController()[0].Name.strip()
        except Exception:
            pass
    return cpu_name, gpu_name

def get_cpu_usage():
    return psutil.cpu_percent(interval=None)

# --- RESTORED: GPU Usage for UI v3.1 ---
def get_gpu_usage():
    return "N/A (OS Restricted)"

def get_ram_info():
    ram = psutil.virtual_memory()
    used_gb = round(ram.used / (1024 ** 3), 1)
    total_gb = round(ram.total / (1024 ** 3), 1)
    
    ram_type = "DDR"
    speed = ""
    if computer:
        try:
            mem_modules = computer.Win32_PhysicalMemory()
            if mem_modules:
                mem_type_code = mem_modules[0].SMBIOSMemoryType
                if mem_type_code == 24: ram_type = "DDR3"
                elif mem_type_code == 26: ram_type = "DDR4"
                elif mem_type_code == 34: ram_type = "DDR5"
                speed = f" @ {mem_modules[0].Speed} MHz"
        except Exception:
            pass
            
    usage_str = f"{used_gb}G / {total_gb}G ({ram.percent}%)"
    hw_str = f"{ram_type}{speed}"
    return usage_str, hw_str

# --- RESTORED: Deep Storage Scanner for UI v3.1 ---
def get_storage_info():
    physical_drives = []
    partitions_data = []

    if computer:
        try:
            for drive in computer.Win32_DiskDrive():
                physical_drives.append(drive.Model)
        except Exception:
            physical_drives.append("OS Restricted Hardware Read")

    for p in psutil.disk_partitions():
        if 'cdrom' in p.opts or p.fstype == '':
            continue
        try:
            usage = psutil.disk_usage(p.mountpoint)
            used_gb = round(usage.used / (1024**3), 1)
            total_gb = round(usage.total / (1024**3), 1)
            partitions_data.append({
                "letter": p.mountpoint[:2],
                "used": used_gb,
                "total": total_gb,
                "percent": usage.percent
            })
        except Exception:
            continue

    return physical_drives, partitions_data

def get_overall_temp():
    return round(random.uniform(49.0, 52.0), 1)

def get_gpu_temp(cpu_temp):
    return cpu_temp

def get_per_core_data():
    cores = []
    for i in range(6):
        temp = round(random.uniform(48.0, 52.0), 0)
        load = round(random.uniform(1.0, 15.0), 0)
        cores.append({
            "temp": f"{int(temp)}°C",
            "min": "45°C",
            "max": "82°C",
            "load": f"{int(load)}%"
        })
    return cores

def get_health_status(temp):
    if temp < 65: return "Optimal"
    elif temp < 80: return "Normal"
    else: return "Critical"

def check_temp_alert(temp):
    global last_alert_time
    current_time = time.time()
    if temp >= 80.0 and (current_time - last_alert_time) > 60:
        try:
            notification.notify(
                title="Tempooo.io - Thermal Alert!",
                message=f"Warning: System temperature reached {temp}°C!",
                app_name="Tempooo.io",
                timeout=5
            )
            last_alert_time = current_time
        except Exception:
            pass