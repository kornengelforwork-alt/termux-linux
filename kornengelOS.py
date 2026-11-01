import os
import sys
import termios
import tty
import time
import subprocess
import socket
import urllib.request

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

def check_storage_permission():
    global storage_checked
    if not storage_checked:
        clear_screen()
        print("==================================================")
        print("           kornengelOS: STORAGE PERMISSION")
        print("==================================================")
        print("\nRequesting access to /storage/emulated/0/")
        print("Please press 'Allow' if a popup appears.\n")
        os.system('termux-setup-storage')
        time.sleep(3)
        storage_checked = True
        clear_screen()

def get_os_input(prompt):
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

def run_browser():
    check_storage_permission()
    clear_screen()
    print("==================================================")
    print("           BROWSER (bs) - kornengelOS")
    print("==================================================")
    print("Checking internet connection...")
    time.sleep(1.5)
    
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("[OK] Internet Connected.\n")
    except OSError:
        print("[ERROR] No Internet Connection!")
        print("Browser will now close.")
        time.sleep(2.5)
        return False 
    
    while True:
        url = input("Enter URL (or type 'exit' to close): ").strip()
        
        if url.lower() == 'exit':
            print("Closing Browser...")
            time.sleep(1.5)
            return False
        if url.lower() == 'turnoff':
            return True
        if not url:
            continue

        print(f"\nLink: {url}")
        choice = input("Do you want to download? (Press Enter to download, 'n' to cancel): ").strip().lower()

        if choice == 'n':
            print("Download cancelled.\n")
        else:
            print("\nStarting download...")
            filename = url.split("/")[-1]
            if not filename or "." not in filename or "?" in filename:
                filename = "downloaded_file.zip"
            
            download_path = f"/storage/emulated/0/Download/{filename}"
            
            try:
                print(f"Saving to: {download_path}")
                urllib.request.urlretrieve(url, download_path)
                size_kb = os.path.getsize(download_path) / 1024
                print(f"\n[SUCCESS] Downloaded successfully! ({size_kb:.2f} KB)")
            except Exception as e:
                print(f"\n[ERROR] Could not download: {e}")
                print("Creating a simulated file instead...")
                try:
                    with open(download_path, "w") as f:
                        f.write("Simulated download content.")
                    show_loading_bar("Downloading file", 2)
                    print(f"[SUCCESS] Simulated file saved to: {download_path}")
                except PermissionError:
                    print("[CRITICAL ERROR] Permission Denied!")
            print("")

def run_calculator():
    clear_screen()
    print("==================================================")
    print("               CALCULATOR (kornengelOS)")
    print("==================================================")
    print("  Type 'exit' to return to Desktop.\n")
    while True:
        try:
            expr = input("Calculator> ").strip()
            if expr.lower() == 'exit': return False 
            if expr.lower() == 'turnoff': return True 
            if not expr: continue
            allowed_chars = set("0123456789+-*/(). ")
            if not set(expr).issubset(allowed_chars):
                print("Error: Invalid characters.")
                continue
            result = eval(expr)
            print(f"= {result}")
        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")
        except Exception:
            print("Error: Invalid expression.")

def run_msword():
    check_storage_permission()
    clear_screen()
    print("==================================================")
    print("           MICROSOFT WORD (kornengelOS)")
    print("==================================================")
    print("  Type '/exve' to save and exit.\n")
    doc_content = ""
    while True:
        try:
            line = input("Write> ")
            if line.strip().lower() == "turnoff": return True 
            if "/exve" in line:
                text_to_add = line.split("/exve")[0]
                if text_to_add.strip(): doc_content += text_to_add + "\n"
                print("\n--- Saving Document ---")
                filename = input("Step 1: File name: ").strip() or "document"
                print("Step 2: Extension (1: txt, 2: docx): ", end="")
                ext = "docx" if input().strip() == "2" else "txt" 
                print("Step 3: Folder (Type 'home/' for /storage/emulated/0/):")
                folder_path = input("Enter folder: ").strip()
                if folder_path.startswith("home/"): folder_path = folder_path.replace("home/", "", 1)
                elif folder_path == "home": folder_path = ""
                
                base_dir = "/storage/emulated/0"
                full_dir = os.path.join(base_dir, folder_path)
                file_path = os.path.join(full_dir, f"{filename}.{ext}")
                try:
                    if not os.path.exists(full_dir): os.makedirs(full_dir, exist_ok=True)
                    with open(file_path, "w", encoding="utf-8") as f: f.write(doc_content)
                    print(f"\n[SUCCESS] File saved at: {file_path}")
                    time.sleep(2); input("Press Enter to return...")
                    return False 
                except Exception as e:
                    print(f"\n[ERROR] Could not save file: {e}")
                    time.sleep(2); input("Press Enter to return...")
                    return False
            elif line.strip() == "": doc_content += "\n"
            else: doc_content += line + "\n"
        except KeyboardInterrupt: return False

def run_fileep():
    check_storage_permission()
    clear_screen()
    print("==================================================")
    print("           FILE EXPLORER (kornengelOS)")
    print("==================================================")
    print("  Type 'help' for commands.\n")
    while True:
        try:
            cmd = input("Fileep> ").strip().lower()
            if cmd == 'exit': return False
            elif cmd == 'turnoff': return True
            elif cmd == 'dir' or cmd == 'ls':
                target_dir = "/storage/emulated/0/Download"
                print(f"\nDirectory of {target_dir}:\n")
                if os.path.exists(target_dir):
                    for f in os.listdir(target_dir):
                        if os.path.isfile(os.path.join(target_dir, f)):
                            print(f" {os.path.getsize(os.path.join(target_dir, f)):>10}  {f}")
                else: print(" Directory not found.")
            elif cmd.startswith('ex '):
                filename = cmd.replace('ex ', '').strip()
                filepath = filename.replace("home/", "/storage/emulated/0/", 1) if filename.startswith("home/") else f"/storage/emulated/0/Download/{filename}"
                if os.path.exists(filepath):
                    print(f"\nExtracting {filename}...")
                    os.system(f'7z x "{filepath}" -o"{os.path.dirname(filepath)}" -p""')
                    input("\nPress Enter to continue...")
                else: print(f"[ERROR] File not found: {filepath}")
            elif cmd == 'mc':
                print("\nLaunching mc...")
                time.sleep(1); os.system('mc'); clear_screen()
            elif cmd == 'help':
                print("\n  dir / ls - List files\n  ex [file] - Extract\n  mc - File Manager\n  exit - Return\n")
            elif cmd == "": continue
            else: print("Unknown command.")
        except KeyboardInterrupt: return False

def show_os_desktop():
    clear_screen()
    print("==================================================")
    print("           kornengelOS (Desktop)")
    print("==================================================")
    print("  Activities   Terminal   Files   Settings")
    print("--------------------------------------------------")
    print("  Installed Applications:")
    print("   - Calculator (Type 'cal' to open)")
    print("   - Microsoft Word (Type 'msword' to open)")
    print("   - File Explorer (Type 'fileep' to open)")
    print("   - Web Browser (Type 'bs' to open)")
    print("==================================================")
    print("[!] Type 'turnoff' and press Enter to close GUI.\n")
    
    while True:
        cmd = get_os_input("osko> ")
        if cmd.lower() == "turnoff": return 
        elif cmd.lower() == "cal":
            if run_calculator(): return 
            else: clear_screen(); print("=== kornengelOS (Desktop) ===\n  [Returned from Calculator]\n")
        elif cmd.lower() == "msword":
            if run_msword(): return 
            else: clear_screen(); print("=== kornengelOS (Desktop) ===\n  [Returned from Microsoft Word]\n")
        elif cmd.lower() == "fileep":
            if run_fileep(): return
            else: clear_screen(); print("=== kornengelOS (Desktop) ===\n  [Returned from File Explorer]\n")
        elif cmd.lower() == "bs":
            if run_browser(): return
            else: clear_screen(); print("=== kornengelOS (Desktop) ===\n  [Returned from Browser]\n")
        elif cmd.strip() == "": continue
        else: print(f"osko: {cmd}: command not found")

def show_settings_app_screen():
    clear_screen()
    print("==================================================")
    print("           kornengelOS - SYSTEM SETTINGS")
    print("==================================================")
    print("   1. reset       : Factory Reset")
    print("   2. upytr       : Update System")
    print("   3. f-restart   : Force Restart")
    print("   4. shutoff     : Force Shutdown")
    print("   5. e-start     : Emergency Restart")
    print("   6. exit set    : Close Settings App")
    print("==================================================\n")

# --- BOOT SEQUENCE ---
clear_screen()
print("Booting kornengelOS...")
time.sleep(1.5)
print("[  OK  ] Started kornengel Core.")
time.sleep(0.5)
print("[  OK  ] Reached target Desktop Environment.")
time.sleep(1)
print("\nWelcome to kornengelOS!")
print("Type 'help' to see available commands.\n")

exit_program = False
while not exit_program:
    try:
        command = input("osko> ").strip().lower()
        if command == "help":
            print("  ls / dir   - List files\n  gui        - Start kornengelOS Desktop\n  settings   - System Settings\n  reboot     - Restart\n  poweroff   - Shutdown\n  clear      - Clear screen")
        elif command == "ls" or command == "dir":
            print("bin   dev  home  lib    media  opt   root  sbin  sys  usr\nboot  etc  initrd.img  lost+found  mnt  proc  run   srv  tmp  var\n")
        elif command == "gui" or command == "startx" or command == "kornengel":
            show_os_desktop()
            print("Closing kornengelOS GUI...")
            show_loading_bar("Stopping X Server", 2)
            time.sleep(0.5); clear_screen(); print("Returning to TTY1...\n")
        elif command == "settings":
            settings_active = True
            while settings_active:
                show_settings_app_screen()
                sub_cmd = input("Settings> ").strip().lower()
                if sub_cmd == "exit set": settings_active = False
                elif sub_cmd == "reset":
                    print("\nAre you sure? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        print("\nType enter 5 times to continue.\n")
                        for i in range(5): input(f"({i+1}/5)...")
                        clear_screen(); show_loading_bar("reinstalling.. kornengelOS", 10)
                        while True:
                            if input("\nPlease type 'yes' to restart: ").strip().lower() == "yes": break
                        show_loading_bar("Rebooting kornengelOS", 3); clear_screen(); settings_active = False 
                elif sub_cmd == "upytr":
                    print("\nUpdate system? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        print("\nPress enter 4 times.\n")
                        for i in range(4): input(f"({i+1}/4)...")
                        clear_screen(); show_loading_bar("updating kornengelOS", 10)
                        while True:
                            if input("\nType 'yes' to restart: ").strip().lower() == "yes": break
                        show_loading_bar("Rebooting kornengelOS", 3); clear_screen(); settings_active = False 
                elif sub_cmd == "shutoff":
                    print("\nForce shutdown? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        show_loading_bar("Force poweroff", 10); clear_screen(); exit_program = True; settings_active = False
                elif sub_cmd == "f-restart":
                    print("\nForce reboot? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        show_loading_bar("Forcing reboot", 10); clear_screen(); settings_active = False 
                elif sub_cmd == "e-start":
                    print("\nEMERGENCY restart? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        show_loading_bar("KERNEL PANIC - RESTARTING", 10); clear_screen(); settings_active = False 
        elif command == "poweroff" or command == "shutdown":
            print("\nPoweroff? (y/n): ", end="", flush=True)
            ans = get_single_key().lower(); print(ans)
            if ans == 'y':
                clear_screen(); show_loading_bar("Powering off", 3); print("System halted."); time.sleep(2); clear_screen(); exit_program = True
        elif command == "reboot" or command == "restart":
            print("\nReboot? (y/n): ", end="", flush=True)
            ans = get_single_key().lower(); print(ans)
            if ans == 'y':
                show_loading_bar("Rebooting system", 3); time.sleep(0.5); clear_screen()
        elif command == "clear" or command == "cls": clear_screen()
        elif command == "": continue
        else: print(f"osko: {command}: command not found\n")
    except KeyboardInterrupt:
        print("\n\nUse 'poweroff' to quit properly.\n")

