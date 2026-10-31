import os
import sys
import termios
import tty
import time
import subprocess

# ตัวแปรสำหรับเช็กว่าได้ขอสิทธิ์ Storage หรือยังในรอบนี้
storage_checked = False

def clear_screen():
    os.system('clear')

def get_single_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = os.read(fd, 1).decode('utf-8', errors='ignore')
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old_settings)
    return ch

# ฟังก์ชันบังคับขอสิทธิ์ Storage
def check_storage_permission():
    global storage_checked
    if not storage_checked:
        clear_screen()
        print("==================================================")
        print("           SYSTEM: STORAGE PERMISSION")
        print("==================================================")
        print("\nRequesting access to /storage/emulated/0/")
        print("Please press 'Allow' if a popup appears.\n")
        os.system('termux-setup-storage')
        time.sleep(3)
        storage_checked = True
        clear_screen()

def get_win_input(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    buffer = ""
    while True:
        char = get_single_key()
        
        if char in ('\r', '\n'):
            print()
            return buffer
            
        elif char in ('\x7f', '\b'):
            if len(buffer) > 0:
                buffer = buffer[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
                
        elif char == '\x03':
            raise KeyboardInterrupt
            
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            buffer += char

def run_calculator():
    clear_screen()
    print("==================================================")
    print("               CALCULATOR (Windows 3.0)")
    print("==================================================")
    print("  Type math (e.g., 1 + 1) and press Enter.")
    print("  Type 'exit' to return to Program Manager.")
    print("--------------------------------------------------\n")
    
    while True:
        try:
            expr = input("Calculator> ").strip()
            
            if expr.lower() == 'exit':
                return False 
                
            if expr.lower() == 'shutdown win':
                return True 
            
            if not expr:
                continue
                
            allowed_chars = set("0123456789+-*/(). ")
            if not set(expr).issubset(allowed_chars):
                print("Error: Invalid characters. Only numbers and + - * / are allowed.")
                continue
                
            result = eval(expr)
            print(f"= {result}")
            
        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")
        except Exception:
            print("Error: Invalid mathematical expression.")

def run_msword():
    check_storage_permission()
    clear_screen()
    print("==================================================")
    print("           MICROSOFT WORD (Windows 3.0)")
    print("==================================================")
    print("  Type your document below.")
    print("  When finished, type a space and '/exve' to save and exit.")
    print("--------------------------------------------------\n")
    
    doc_content = ""
    
    while True:
        try:
            line = input("Write> ")
            
            if line.strip().lower() == "shutdown win":
                return True 
            
            if "/exve" in line:
                text_to_add = line.split("/exve")[0]
                if text_to_add.strip():
                    doc_content += text_to_add + "\n"
                    
                print("\n--- Saving Document ---")
                
                filename = input("Step 1: What file name will you save the file as? (e.g., mydoc): ").strip()
                if not filename:
                    filename = "document" 
                
                print("\nStep 2: What file extension will you save the file as?")
                print("1: txt")
                print("2: docx")
                ext_choice = input("Select (1 or 2): ").strip()
                if ext_choice == "2":
                    ext = "docx"
                else:
                    ext = "txt" 
                
                print("\nStep 3: Where would you like to save the file?")
                print("(Type 'home/' for /storage/emulated/0/)")
                folder_path = input("Enter folder (e.g., home/document): ").strip()
                
                if folder_path.startswith("home/"):
                    folder_path = folder_path.replace("home/", "", 1)
                elif folder_path == "home":
                    folder_path = ""
                
                base_dir = "/storage/emulated/0"
                full_dir = os.path.join(base_dir, folder_path)
                file_path = os.path.join(full_dir, f"{filename}.{ext}")
                
                try:
                    if not os.path.exists(full_dir):
                        os.makedirs(full_dir, exist_ok=True)
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(doc_content)
                    
                    print(f"\n[SUCCESS] File saved at: {file_path}")
                    time.sleep(2)
                    input("Press Enter to return to Program Manager...")
                    return False 
                    
                except PermissionError:
                    print(f"\n[ERROR] Permission denied.")
                    print("If you are on A14, you cannot grant storage permission.")
                    print("Please use J7 to save files, or save in Termux Home.")
                    time.sleep(3)
                    input("Press Enter to return...")
                    return False
                except Exception as e:
                    print(f"\n[ERROR] Could not save file: {e}")
                    time.sleep(2)
                    input("Press Enter to return...")
                    return False
                    
            elif line.strip() == "":
                doc_content += "\n"
            else:
                doc_content += line + "\n"
                
        except KeyboardInterrupt:
            return False

def run_fileep():
    check_storage_permission()
    clear_screen()
    print("==================================================")
    print("           FILE EXPLORER (Windows 3.0)")
    print("==================================================")
    print("  Type 'help' to see available commands.")
    print("  Type 'exit' to return to Program Manager.")
    print("--------------------------------------------------\n")
    
    while True:
        try:
            cmd = input("Fileep> ").strip().lower()
            
            if cmd == 'exit':
                return False
            elif cmd == 'shutdown win':
                return True
            elif cmd == 'dir' or cmd == 'ls':
                target_dir = "/storage/emulated/0/Download"
                print(f"\nDirectory of {target_dir}:\n")
                if os.path.exists(target_dir):
                    files = os.listdir(target_dir)
                    for f in files:
                        if os.path.isfile(os.path.join(target_dir, f)):
                            size = os.path.getsize(os.path.join(target_dir, f))
                            print(f" {size:>10}  {f}")
                    print(f"\n Total: {len(files)} files/folders.")
                else:
                    print(" Directory not found or Permission Denied.")
            
            elif cmd.startswith('ex '):
                filename = cmd.replace('ex ', '').strip()
                
                if filename.startswith("home/"):
                    filepath = filename.replace("home/", "/storage/emulated/0/", 1)
                else:
                    filepath = f"/storage/emulated/0/Download/{filename}"
                
                if os.path.exists(filepath):
                    print(f"\nChecking file integrity and password...")
                    
                    # ระบบตรวจสอบรหัสผ่านเบื้องต้น (ทดสอบด้วยรหัสว่าง)
                    try:
                        # ใช้ subprocess เพื่อทดสอบไฟล์โดยไม่ให้หน้าจอค้าง
                        test_res = subprocess.run(["7z", "t", "-p", "", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
                        out_str = test_res.stdout.decode('utf-8', errors='ignore') + test_res.stderr.decode('utf-8', errors='ignore')
                        
                        # ถ้าตรวจพบว่าติดรหัสผ่าน
                        if "Enter password" in out_str or "Wrong password" in out_str or "Data Error" in out_str or "Cannot open encrypted" in out_str:
                            print("\n[ERROR] This file cannot be extracted without the file's password.")
                            input("\nPress Enter to continue...")
                            continue
                    except Exception:
                        # ถ้าระบบทดสอบมีปัญหา ให้ข้ามไปแตกไฟล์ปกติ
                        pass

                    print(f"\nExtracting {filename} using p7zip...")
                    out_dir = os.path.dirname(filepath)
                    # ใส่ -p"" ไว้เพื่อป้องกันไม่ให้ 7z ค้างรอใส่รหัสผ่าน
                    os.system(f'7z x "{filepath}" -o"{out_dir}" -p""')
                    input("\nPress Enter to continue...")
                else:
                    print(f"[ERROR] File not found: {filepath}")

            elif cmd == 'mc':
                print("\nLaunching Midnight Commander (Press F10 to exit mc)...")
                time.sleep(1)
                os.system('mc') 
                clear_screen()
                print("Returned to File Explorer.")
                
            elif cmd == 'help':
                print("\nAvailable Commands:")
                print("  dir / ls       - List files in Download")
                print("  ex [file]      - Extract .zip/.7z (e.g., ex file.zip or ex home/file.zip)")
                print("  mc             - Open Midnight Commander")
                print("  exit           - Return to Program Manager\n")
            elif cmd == "":
                continue
            else:
                print("Unknown command. Type 'help' for options.")
                
        except KeyboardInterrupt:
            return False

def show_loading_bar(prefix, duration=3):
    clear_screen()
    print("==================================================")
    print(f"   {prefix}...")
    print("==================================================\n")
    steps = 20
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        bar = '#' * i + '-' * (steps - i)
        sys.stdout.write(f'\rProgress: [{bar}] {percent}%')
        sys.stdout.flush()
        time.sleep(duration / steps)
    print("\n\nDone.")

def show_windows_3_professional():
    clear_screen()
    print("==================================================")
    print("           WINDOWS 3.0 PROFESSIONAL")
    print("==================================================")
    print("  Program Manager")
    print("  -----------------")
    print("  [ Main ]   [ Accessories ]   [ Games ]")
    print("  -----------------")
    print("  File Manager       Control Panel")
    print("  Write              Paint")
    print("  MS-DOS Prompt      Print Manager")
    print("--------------------------------------------------")
    print("  Installed Applications:")
    print("   - Calculator (Type 'cal' to open)")
    print("   - Microsoft Word (Type 'msword' to open)")
    print("   - File Explorer (Type 'fileep' to open)")
    print("   - Notepad")
    print("   - Clock")
    print("==================================================")
    print("[!] Type 'shutdown win' and press Enter to exit Windows.\n")
    
    while True:
        cmd = get_win_input("Program Manager> ")
        
        if cmd == "shutdown win":
            return 
            
        elif cmd.lower() == "cal":
            if run_calculator(): 
                return 
            else:
                clear_screen()
                print("==================================================")
                print("           WINDOWS 3.0 PROFESSIONAL")
                print("==================================================")
                print("  [Returned from Calculator]")
                print("[!] Type 'cal', 'msword', 'fileep', or 'shutdown win'.\n")
                
        elif cmd.lower() == "msword":
            if run_msword():
                return 
            else:
                clear_screen()
                print("==================================================")
                print("           WINDOWS 3.0 PROFESSIONAL")
                print("==================================================")
                print("  [Returned from Microsoft Word]")
                print("[!] Type 'cal', 'msword', 'fileep', or 'shutdown win'.\n")

        elif cmd.lower() == "fileep":
            if run_fileep():
                return
            else:
                clear_screen()
                print("==================================================")
                print("           WINDOWS 3.0 PROFESSIONAL")
                print("==================================================")
                print("  [Returned from File Explorer]")
                print("[!] Type 'cal', 'msword', 'fileep', or 'shutdown win'.\n")
                
        elif cmd.strip() == "":
            continue
        else:
            print(f"Bad command or file name: {cmd}")

def show_apple_mac_os():
    clear_screen()
    print(" macOS Ventura (Simulator)")
    print("--------------------------------------------------")
    print(" File  Edit  View  Go  Window  Help")
    print("--------------------------------------------------")
    print("\n\n")
    print("  +--------------------------------------------+")
    print("  | Virtual Machine: MS-DOS 6.22 / Win 3.0     |")
    print("  |--------------------------------------------|")
    print("  |                                            |")
    print("  |      [ WINDOWS 3.0 PROFESSIONAL ]          |")
    print("  |                                            |")
    print("  |      Program Manager                       |")
    print("  |      - Main                                |")
    print("  |      - Accessories                         |")
    print("  |      - Games                               |")
    print("  |                                            |")
    print("  |      (Running inside Apple environment)    |")
    print("  |                                            |")
    print("  +--------------------------------------------+")
    print("\n")
    print("  [Installed Mac Apps]")
    print("   - p7zip (File Archiver)")
    print("   - mc (Midnight Commander - File Manager)")
    print("   - Termux")
    print("\n")
    print("  [Dock]: Finder   Safari   Mail   Termux   Settings")
    print("==================================================")
    print("[!] You are viewing Windows 3.0 inside macOS.")
    print("[!] Press any key to exit macOS and return to DOS.\n")

def show_settings_app_screen():
    clear_screen()
    print("==================================================")
    print("           WINDOWS 3.0 - SYSTEM SETTINGS")
    print("==================================================")
    print("  [ System Configuration ]")
    print("   - Display Adapter: VGA")
    print("   - Keyboard Layout: US")
    print("   - Mouse: Microsoft Serial Mouse")
    print("\n  [ Advanced Commands (Total 6) ]")
    print("   1. reset       : Factory Reset")
    print("   2. upytr       : Update System")
    print("   3. f-restart   : Force Restart")
    print("   4. shutoff     : Force Shutdown")
    print("   5. e-start     : Emergency Restart")
    print("   6. exit set    : Close Settings App")
    print("==================================================\n")

clear_screen()
print("Starting MS-DOS...")
time.sleep(1.5)
print("HIMEM is testing extended memory...done.")
time.sleep(1)
print("\nType 'help' to see available commands.\n")

exit_program = False

while not exit_program:
    try:
        command = input("C:\\> ").strip().lower()

        if command == "help":
            print("=== MAIN COMMANDS ===")
            print("  dir        - List files in current directory")
            print("  win        - Start Windows 3.0 Simulator")
            print("  apple mac  - Run Windows in macOS VM")
            print("  settings   - Open System Settings App")
            print("  restart    - Restart the DOS environment")
            print("  shutdown   - Shutdown the simulator")
            print("  cls        - Clear the screen")

        elif command == "dir":
            print(" Volume in drive C is MS-DOS_6")
            print(" Directory of C:\\\n")
            print("DOS          <DIR>     10-25-26  10:00a")
            print("WINDOWS      <DIR>     10-25-26  10:05a")
            print("COMMAND  COM     54876 10-20-26  10:00a")
            print("AUTOEXEC BAT       128 10-20-26  10:00a")
            print("        2 dir(s)   8,192,000 bytes free\n")

        elif command == "win":
            show_windows_3_professional()
            print("Shutting down Windows 3.0...")
            show_loading_bar("Returning to MS-DOS", 3)
            time.sleep(0.5)
            clear_screen()
            print("Returning to C:\\...\n")
            print("Type 'help' to see available commands.\n")

        elif command in ["apple mac", "apple max", "app termux"]:
            show_apple_mac_os()
            get_single_key()
            show_loading_bar("Closing Virtual Machine", 2)
            clear_screen()
            print("Returning to C:\\...\n")
            print("Type 'help' to see available commands.\n")

        elif command == "settings":
            settings_active = True
            while settings_active:
                show_settings_app_screen()
                sub_cmd = input("Settings> ").strip().lower()
                
                if sub_cmd == "exit set":
                    print("Closing Settings App...\n")
                    settings_active = False

                elif sub_cmd == "reset":
                    print("\nAre you sure you want to do this? This operation is irreversible. (y/n): ", end="", flush=True)
                    ans = get_single_key().lower()
                    print(ans)
                    if ans == 'y':
                        print("\nThe action is as follows:")
                        print("If there is important information, type ytr")
                        print("To exit this page, but if you want to perform a permanent reset, press enter 5 times to continue.\n")
                        for i in range(5):
                            input(f"Press Enter to confirm ({i+1}/5)...")
                        clear_screen()
                        print("reinstalling.. ms-dos and windows\n") 
                        for i in range(101):
                            bar = '#' * (i // 2) + '-' * (50 - (i // 2))
                            sys.stdout.write(f'\rProgress: [{bar}] {i}%')
                            sys.stdout.flush()
                            time.sleep(25.0 / 100) 
                        print("\n\nFactory reset complete. System restored to defaults.")
                        time.sleep(2)
                        while True:
                            confirm_restart = input("\nPlease type 'yes' to restart and return to MS-DOS: ").strip().lower()
                            if confirm_restart == "yes": break
                            print("Invalid input. You must type 'yes'.")
                        show_loading_bar("Restarting MS-DOS", 3)
                        clear_screen()
                        print("returning to C:\\>\n")
                        print("Type 'help' to see available commands.\n")
                        settings_active = False 
                    else:
                        print("Reset cancelled.\n")

                elif sub_cmd == "upytr":
                    print("\nDo you want to update the system? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower()
                    print(ans)
                    if ans == 'y':
                        print("\nAre you sure about the policy for using this device?")
                        print("And will you use this device?")
                        print("If you will use it, you must press enter 4 times.\n")
                        for i in range(4):
                            input(f"Press Enter to confirm ({i+1}/4)...")
                        clear_screen()
                        for i in range(101):
                            bar = '#' * (i // 2) + '-' * (50 - (i // 2))
                            if i < 50:
                                status = "updating msdos      "
                                time.sleep(15.0 / 50) 
                            else:
                                status = "Updating windows    "
                                time.sleep(15.0 / 50) 
                            sys.stdout.write(f'\r{status} [{bar}] {i}%')
                            sys.stdout.flush()
                        print("\n\nSystem update complete!")
                        time.sleep(2)
                        while True:
                            confirm_restart = input("\nPlease type 'yes' to restart and return to MS-DOS: ").strip().lower()
                            if confirm_restart == "yes": break
                            print("Invalid input. You must type 'yes'.")
                        show_loading_bar("Restarting MS-DOS", 3)
                        clear_screen()
                        print("returning to C:\\>\n")
                        print("Type 'help' to see available commands.\n")
                        settings_active = False 
                    else:
                        print("Update cancelled.\n")

                elif sub_cmd == "shutoff":
                    print("\nDo you want to force shut down the device? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower()
                    print(ans)
                    if ans == 'y':
                        show_loading_bar("Force shutting down device", 10)
                        clear_screen() 
                        exit_program = True 
                        settings_active = False
                    else:
                        print("Force shutdown cancelled.\n")

                elif sub_cmd == "f-restart":
                    print("\nDo you want to force restart the device? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower()
                    print(ans)
                    if ans == 'y':
                        show_loading_bar("Force restarting device", 10)
                        clear_screen()
                        print("Starting MS-DOS...")
                        time.sleep(1.5)
                        print("Type 'help' to see available commands.\n")
                        settings_active = False 
                    else:
                        print("Force restart cancelled.\n")

                elif sub_cmd == "e-start":
                    print("\nDo you want to perform an EMERGENCY restart? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower()
                    print(ans)
                    if ans == 'y':
                        show_loading_bar("EMERGENCY RESTARTING SYSTEM", 10)
                        clear_screen()
                        print("Starting MS-DOS...")
                        time.sleep(1.5)
                        print("Type 'help' to see available commands.\n")
                        settings_active = False 
                    else:
                        print("Emergency restart cancelled.\n")

                elif sub_cmd == "":
                    continue
                else:
                    print("Unknown command inside Settings App.")

        elif command == "shutdown":
            print("\nAre you sure you want to shutdown? (y/n): ", end="", flush=True)
            ans = get_single_key().lower()
            print(ans)
            
            if ans == 'y':
                clear_screen()
                print("\033[33m")
                print("==================================================")
                print("           SHUTTING DOWN MS-DOS...")
                print("==================================================")
                print("\033[0m")
                time.sleep(1.5)
                show_loading_bar("Shutting down system", 3)
                print("It is now safe to turn off your computer.")
                time.sleep(2)
                clear_screen()
                exit_program = True
            else:
                print("Shutdown cancelled.\n")

        elif command == "restart":
            print("\nAre you sure you want to restart? (y/n): ", end="", flush=True)
            ans = get_single_key().lower()
            print(ans)
            
            if ans == 'y':
                show_loading_bar("Restarting MS-DOS", 3)
                time.sleep(0.5)
                clear_screen()
                print("Returning to C:\\...\n")
                print("Type 'help' to see available commands.\n")
            else:
                print("Restart cancelled.\n")

        elif command == "cls":
            clear_screen()

        elif command == "":
            continue

        else:
            print(f"Bad command or file name: {command}\n")

    except KeyboardInterrupt:
        print("\n\nUse 'shutdown' to quit properly.\n")

