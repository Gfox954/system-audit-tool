import platform
import psutil
import datetime
import subprocess
import json

def get_system_info():
    return {
        "timestamp": str(datetime.datetime.now()),
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def get_resource_usage():
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent
    }

def get_top_processes(limit=5):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        processes.append(proc.info)
    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    return processes[:limit]

def get_defender_status():
    try:
        result = subprocess.check_output(
            ["powershell", "Get-MpComputerStatus | ConvertTo-Json"],
            stderr=subprocess.STDOUT
        )
        return json.loads(result)
    except Exception:
        return "Windows Defender not available or not running PowerShell."

def main():
    report = {
        "system_info": get_system_info(),
        "resource_usage": get_resource_usage(),
        "top_processes": get_top_processes(),
        "defender_status": get_defender_status()
    }

    with open("system_audit_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("System audit complete. Report saved to system_audit_report.json")

if __name__ == "__main__":
    main()
