import os
import sys
import time
import socket
import shutil
import termios
import tty
import select

# --- ระบบจัดการภาษา (Language System) ---
current_lang = "en"

translations = {
    "en": {
        "welcome": "🚀 KORNENGEL UTILITY TOOL v4.0 (SYSTEM MONITOR) 🚀",
        "type_help": "Type 'help' to see all available commands.\n",
        "help_title": "\n=== 🛠️ AVAILABLE COMMANDS ===",
        "help_help": "  help         : Show all available commands",
        "help_files": "  files        : Enter File Manager",
        "help_sysinfo": "  sysinfo      : Open Live System Monitor",
        "help_ip": "  ip           : Show current IP Address",
        "help_battery": "  battery      : Check battery percentage",
        "help_clear": "  clear        : Clear screen",
        "help_lang": "  /thai        : Switch to Thai language\n  /english     : Switch to English language",
        "help_exit": "  exit         : Exit program\n",
        "unknown": "❌ Unknown command '{cmd}'. (Type 'help' for options)",
        "exiting": "\nExiting program... Goodbye!",
        "error": "❌ An error occurred: {e}",
        "lang_changed": "✅ Language switched to English.",
        
        # File Manager
        "fm_title": "\n==================================================\n 📁 FILE MANAGER | Path: {path}\n==================================================",
        "fm_cmds": "Available commands: ls, move, exit",
        "fm_prompt": "FileManager> ",
        "fm_exit": "Exiting File Manager...",
        "fm_ls": "\nFiles in {path}:\n",
        "fm_empty": " (Directory is empty)",
        "fm_not_found": " ❌ Directory not found.",
        "fm_src_prompt": "Enter filename to move (e.g., song.mp3): ",
        "fm_cancel_src": "❌ Cancelled: No filename provided.",
        "fm_file_not_found": "❌ File '{filename}' not found in this directory.",
        "fm_dest_prompt": "Enter destination folder (e.g., /storage/emulated/0/Music): ",
        "fm_cancel_dest": "❌ Cancelled: No destination provided.",
        "fm_create_dir": "📁 Created new directory: {folder}",
        "fm_create_fail": "❌ Could not create directory {folder}",
        "fm_move_success": "✅ Successfully moved: {filename} -> {folder}",
        "fm_move_fail": "❌ Move failed: {e}",
        "fm_unknown": "❌ Unknown command '{cmd}' in File Manager. (Type 'ls', 'move', or 'exit')",
        
        # System Monitor
        "mon_title": "📊 LIVE SYSTEM MONITOR 📊",
        "mon_time": "Time          :",
        "mon_ip": "IP Address    :",
        "mon_uptime": "System Uptime :",
        "mon_ram": "RAM Usage     :",
        "mon_status": "Status        : MONITORING...",
        "mon_exit": "Press 'e' to EXIT Monitor."
    },
    "th": {
        "welcome": "🚀 KORNENGEL UTILITY TOOL v4.0 (ระบบตรวจสอบสถานะ) 🚀",
        "type_help": "พิมพ์ 'help' เพื่อดูรายการคำสั่งทั้งหมด\n",
        "help_title": "\n=== 🛠️ คำสั่งที่ใช้งานได้ ===",
        "help_help": "  help         : แสดงรายการคำสั่งทั้งหมด",
        "help_files": "  files        : เข้าสู่ระบบจัดการไฟล์",
        "help_sysinfo": "  sysinfo      : เปิดหน้าจอตรวจสอบสถานะแบบเรียลไทม์",
        "help_ip": "  ip           : แสดง IP Address ปัจจุบัน",
        "help_battery": "  battery      : เช็กเปอร์เซ็นต์แบตเตอรี่",
        "help_clear": "  clear        : ล้างหน้าจอ",
        "help_lang": "  /thai        : เปลี่ยนเป็นภาษาไทย\n  /english     : เปลี่ยนเป็นภาษาอังกฤษ",
        "help_exit": "  exit         : ออกจากโปรแกรม\n",
        "unknown": "❌ ไม่รู้จักคำสั่ง '{cmd}' (พิมพ์ 'help' เพื่อดูคำสั่ง)",
        "exiting": "\nปิดโปรแกรม... ลาก่อนครับ!",
        "error": "❌ เกิดข้อผิดพลาด: {e}",
        "lang_changed": "✅ เปลี่ยนภาษาเป็นภาษาไทยเรียบร้อยแล้ว",
        
        # File Manager
        "fm_title": "\n==================================================\n 📁 ระบบจัดการไฟล์ | ตำแหน่ง: {path}\n==================================================",
        "fm_cmds": "คำสั่งที่ใช้ได้: ls, move, exit",
        "fm_prompt": "FileManager> ",
        "fm_exit": "ออกจากระบบจัดการไฟล์...",
        "fm_ls": "\nรายชื่อไฟล์ใน {path}:\n",
        "fm_empty": " (โฟลเดอร์ว่างเปล่า)",
        "fm_not_found": " ❌ ไม่พบโฟลเดอร์นี้",
        "fm_src_prompt": "ระบุชื่อไฟล์ที่ต้องการย้าย (เช่น song.mp3): ",
        "fm_cancel_src": "❌ ยกเลิก: ไม่ได้ระบุชื่อไฟล์",
        "fm_file_not_found": "❌ ไม่พบไฟล์ '{filename}' ในโฟลเดอร์นี้",
        "fm_dest_prompt": "ระบุโฟลเดอร์ปลายทาง (เช่น /storage/emulated/0/Music): ",
        "fm_cancel_dest": "❌ ยกเลิก: ไม่ได้ระบุปลายทาง",
        "fm_create_dir": "📁 สร้างโฟลเดอร์ใหม่: {folder}",
        "fm_create_fail": "❌ ไม่สามารถสร้างโฟลเดอร์ {folder} ได้",
        "fm_move_success": "✅ ย้ายไฟล์สำเร็จ: {filename} -> {folder}",
        "fm_move_fail": "❌ ย้ายไม่สำเร็จ: {e}",
        "fm_unknown": "❌ ไม่รู้จักคำสั่ง '{cmd}' ใน File Manager (พิมพ์ ls, move หรือ exit)",
        
        # System Monitor
        "mon_title": "📊 หน้าจอตรวจสอบสถานะระบบ 📊",
        "mon_time": "เวลาปัจจุบัน     :",
        "mon_ip": "IP Address       :",
        "mon_uptime": "เปิดเครื่องมาแล้ว:",
        "mon_ram": "การใช้แรม       :",
        "mon_status": "สถานะ            : กำลังตรวจสอบ...",
        "mon_exit": "กดปุ่ม 'e' เพื่อออกจากหน้าจอนี้"
    }
}

def t(key, **kwargs):
    text = translations[current_lang].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

# --- ฟังก์ชันดึงข้อมูลระบบ ---
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
        total, free = 0, 0
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

def get_battery():
    try:
        with open('/sys/class/power_supply/battery/capacity', 'r') as f:
            return f"{f.read().strip()}%"
    except Exception:
        return "N/A"

# --- 📊 ระบบ Live System Monitor (แบบกด e เพื่อออก) ---
def run_system_monitor():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        while True:
            clear_screen()
            current_time = time.strftime("%H:%M:%S")
            
            print("==================================================")
            print(f"       {t('mon_title')}       ")
            print("==================================================")
            print(f" {t('mon_time')} {current_time}")
            print(f" {t('mon_ip')} {get_ip_address()}")
            print(f" {t('mon_uptime')} {get_uptime()}")
            print(f" {t('mon_ram')} {get_ram_info()}")
            print("==================================================")
            print(f" {t('mon_status')}")
            print(f"\n [!] {t('mon_exit')}")
            
            # หน่วงเวลา 1 วินาที และรอรับการกดปุ่ม
            rlist, _, _ = select.select([sys.stdin], [], [], 1.0)
            
            if rlist:
                char = sys.stdin.read(1)
                if char.lower() == 'e':
                    break # ออกจากลูปเมื่อกด e
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        clear_screen()

# --- File Manager ---
def run_file_manager():
    current_dir = "/storage/emulated/0/Download"
    
    while True:
        print(t("fm_title", path=current_dir))
        print(t("fm_cmds"))
        
        cmd_input = input(t("fm_prompt")).strip().split()
        if not cmd_input:
            continue
            
        cmd = cmd_input[0].lower()

        if cmd == "exit":
            print(t("fm_exit"))
            break

        elif cmd in ["ls", "dir"]:
            print(t("fm_ls", path=current_dir))
            if os.path.exists(current_dir):
                files = os.listdir(current_dir)
                if not files:
                    print(t("fm_empty"))
                for f in files:
                    full_path = os.path.join(current_dir, f)
                    if os.path.isfile(full_path):
                        size_kb = os.path.getsize(full_path) / 1024
                        print(f" [FILE] {f:<30} ({size_kb:.1f} KB)")
                    else:
                        print(f" [DIR ] {f:<30}")
            else:
                print(t("fm_not_found"))

        elif cmd == "move":
            filename = input(t("fm_src_prompt")).strip()
            if not filename:
                print(t("fm_cancel_src"))
                continue
                
            source_path = os.path.join(current_dir, filename)
            
            if not os.path.exists(source_path):
                print(t("fm_file_not_found", filename=filename))
                continue

            dest_folder = input(t("fm_dest_prompt")).strip()
            if not dest_folder:
                print(t("fm_cancel_dest"))
                continue
                
            if not os.path.exists(dest_folder):
                try:
                    os.makedirs(dest_folder)
                    print(t("fm_create_dir", folder=dest_folder))
                except Exception:
                    print(t("fm_create_fail", folder=dest_folder))
                    continue
            
            dest_path = os.path.join(dest_folder, filename)
            
            try:
                shutil.move(source_path, dest_path)
                print(t("fm_move_success", filename=filename, folder=dest_folder))
            except Exception as e:
                print(t("fm_move_fail", e=e))
                
        else:
            print(t("fm_unknown", cmd=cmd))

# --- Main Program ---
def show_help():
    print(t("help_title"))
    print(t("help_help"))
    print(t("help_files"))
    print(t("help_sysinfo"))
    print(t("help_ip"))
    print(t("help_battery"))
    print(t("help_clear"))
    print(t("help_lang"))
    print(t("help_exit"))

def main():
    global current_lang
    clear_screen()
    print("==================================================")
    print(t("welcome"))
    print("==================================================")
    print(t("type_help"))

    while True:
        try:
            cmd = input("KornengelTool> ").strip()

            # --- ระบบสลับภาษา ---
            if cmd == "/thai":
                current_lang = "th"
                clear_screen()
                print(t("lang_changed"))
                continue
            elif cmd == "/english":
                current_lang = "en"
                clear_screen()
                print(t("lang_changed"))
                continue

            cmd_lower = cmd.lower()

            if cmd_lower == "help":
                show_help()
            elif cmd_lower == "files" or cmd_lower == "file":
                run_file_manager()
            elif cmd_lower == "sysinfo":
                run_system_monitor() # เรียกใช้ฟังก์ชัน Monitor แบบเต็มจอ
                print(t("lang_changed").replace("Language switched to English.", "").replace("เปลี่ยนภาษาเป็นภาษาไทยเรียบร้อยแล้ว", "").replace("✅ ", "")) # ล้างข้อความตกค้าง
                # เคลียร์หน้าจอหลังออกจาก Monitor
                clear_screen() 
            elif cmd_lower == "ip":
                print(f"\n[🌐] IP Address : {get_ip_address()}")
            elif cmd_lower == "battery":
                print(f"\n[🔋] Battery    : {get_battery()}")
            elif cmd_lower == "clear":
                clear_screen()
            elif cmd_lower == "exit":
                print(t("exiting"))
                break
            elif cmd_lower == "":
                continue
            else:
                print(t("unknown", cmd=cmd))

        except KeyboardInterrupt:
            print(t("exiting"))
            break
        except Exception as e:
            print(t("error", e=e))

if __name__ == "__main__":
    main()

