import os
import sys
import time
import socket
import termios
import tty
import select

def clear_screen():
    os.system('clear')

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
        total = 0
        free = 0
        for line in lines:
            if 'MemTotal' in line: total = int(line.split()[1])
            elif 'MemFree' in line: free = int(line.split()[1])
        used = total - free
        percent = int((used / total) * 100) if total > 0 else 0
        return f"{used // 1024} MB / {total // 1024} MB ({percent}%)"
    except Exception:
        return "N/A"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            return f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"
    except Exception:
        return "N/A"

def main():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    
    is_paused = False

    try:
        while True:
            if not is_paused:
                clear_screen()
                current_time = time.strftime("%H:%M:%S")
                print("==================================================")
                print("       HACKER DASHBOARD (KORNENGEL EDITION)       ")
                print("==================================================")
                print(f" [*] Time          : {current_time}")
                print(f" [*] IP Address    : {get_ip_address()}")
                print(f" [*] System Uptime : {get_uptime()}")
                print(f" [*] RAM Usage     : {get_ram_info()}")
                print("==================================================")
                print(" [>] Status: MONITORING...")
                print("\n [!] Press 'p' to PAUSE (to copy IP).")
                print(" [!] Press 'e' to EXIT.")
            else:
                # ถ้าอยู่ในโหมดหยุดชั่วคราว จะไม่ Clear หน้าจอ
                pass 
            
            rlist, _, _ = select.select([sys.stdin], [], [], 1.0)
            
            if rlist:
                char = sys.stdin.read(1).lower()
                if char == 'e':
                    break
                elif char == 'p' and not is_paused:
                    is_paused = True
                    print("\n\n [PAUSED] You can now long-press to copy the IP.")
                    print(" Press 'r' to RESUME or 'e' to EXIT.")
                elif char == 'r' and is_paused:
                    is_paused = False

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        clear_screen()
        print("Dashboard closed. Returning to Termux...")

if __name__ == "__main__":
    main()
