import os
import time
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_ram_info():
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        total, free = 0, 0
        for line in lines:
            if 'MemTotal' in line: total = int(line.split()[1])
            elif 'MemFree' in line: free = int(line.split()[1])
        used = total - free
        percent = int((used / total) * 100) if total > 0 else 0
        return f"{used // 1024}MB / {total // 1024}MB ({percent}%)"
    except Exception:
        return "N/A"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    except Exception:
        return "N/A"

def get_battery():
    try:
        with open('/sys/class/power_supply/battery/capacity', 'r') as f:
            return f"{f.read().strip()}%"
    except Exception:
        return "N/A"

def show_neofetch():
    os.system('clear')
    
    print("\n")
    # โลโก้แบบย่อ (พอดีจอ J7)
    print("    _  __                 _           ")
    print("   | |/ /___  _ __ _ __  | |__   ___  ")
    print("   | ' // _ \\| '__| '_ \\ | '_ \\ / _ \\ ")
    print("   | . \\ (_) | |  | | | || | | |  __/ ")
    print("   |_|\\_\\___/|_|  |_| |_||_| |_|\\___| ")
    print("        KORNENGEL OS SIMULATOR       ")
    print("-------------------------------------")
    
    time.sleep(0.5) # หน่วงเวลาให้เห็นโลโก้
    
    print(f" OS       : Termux Android")
    print(f" Kernel   : Linux 3.x")
    print(f" Uptime   : {get_uptime()}")
    print(f" IP Addr  : {get_ip_address()}")
    print(f" Memory   : {get_ram_info()}")
    print(f" Battery  : {get_battery()}")
    print("-------------------------------------")
    print(" (C) 2026 Kornengel Group\n")
    
    # ใช้ input() แทนเพื่อไม่ให้ปิดตัวเองทันที
    input(" [Press Enter to exit...]")
    os.system('clear')

if __name__ == "__main__":
    try:
        show_neofetch()
    except KeyboardInterrupt:
        os.system('clear')
        print("\nExited Neofetch.\n")
