import os
import sys
import termios
import tty
import time
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
        print("           SYSTEM: STORAGE PERMISSION")
        print("==================================================")
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
    print("               BROWSER (bs) - Windows 3.0")
    print("==================================================")
    print("Checking internet connection...")
    time.sleep(1.5)
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("[OK] Internet Connected.\n")
    except OSError:
        print("[ERROR] No Internet Connection!")
        time.sleep(2.5)
        return False 
    while True:
        url = input("Enter URL (or type 'exit' to close): ").strip()
        if url.lower() == 'exit':
            print("Closing Browser...")
            time.sleep(1.5)
            return False
        if url.lower() == 'turnoff' or url.lower() == 'shutdown win':
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
    print("               CALCULATOR (Windows 3.0)")
    print("==================================================")
    print("  Type 'exit' to return to Program Manager.\n")
    while True:
        try:
            expr = input("Calculator> ").strip()
            if expr.lower() == 'exit': return False 
            if expr.lower() == 'turnoff' or expr.lower() == 'shutdown win': return True 
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
    print("           MICROSOFT WORD (Windows 3.0)")
    print("==================================================")
    print("  Type '/exve' to save and exit.\n")
    doc_content = ""
    while True:
        try:
            line = input("Write> ")
            if line.strip().lower() == "shutdown win" or line.strip().lower() == "turnoff": return True 
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
    print("           FILE EXPLORER (Windows 3.0)")
    print("==================================================")
    print("  Type 'help' for commands.\n")
    target_dir = "/storage/emulated/0/Download"
    while True:
        try:
            cmd = input("Fileep> ").strip().lower()
            if cmd == 'exit': return False
            elif cmd == 'turnoff' or cmd == 'shutdown win': return True
            elif cmd == 'dir' or cmd == 'ls':
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
                    print(f"\nExtracting {filename} using unzip...")
                    out_dir = os.path.dirname(filepath)
                    os.system(f'unzip -o "{filepath}" -d "{out_dir}"')
                    input("\nPress Enter to continue...")
                else: print(f"[ERROR] File not found: {filepath}")
            elif cmd.startswith('zip '):
                parts = cmd.split()
                if len(parts) == 3:
                    source = parts[1]
                    dest_zip = parts[2]
                    source_path = source.replace("home/", "/storage/emulated/0/", 1) if source.startswith("home/") else f"/storage/emulated/0/Download/{source}"
                    zip_path = dest_zip.replace("home/", "/storage/emulated/0/", 1) if dest_zip.startswith("home/") else f"/storage/emulated/0/Download/{dest_zip}"
                    if os.path.exists(source_path):
                        print(f"\nCompressing {source} into {dest_zip}...")
                        os.system(f'zip -r "{zip_path}" "{source_path}"')
                        input("\nPress Enter to continue...")
                    else: print(f"[ERROR] Source not found: {source_path}")
                else: print("[ERROR] Usage: zip <source> <dest.zip>")
            elif cmd == 'mc':
                print("\nLaunching mc...")
                time.sleep(1); os.system('mc'); clear_screen()
            elif cmd == 'help':
                print("\n  dir / ls - List files\n  ex [file] - Extract using unzip\n  zip [src] [dst] - Compress to .zip\n  mc - File Manager\n  exit - Return\n")
            elif cmd == "": continue
            else: print("Unknown command.")
        except KeyboardInterrupt: return False

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
    print("   - Browser (Type 'bs' to open)")
    print("==================================================")
    print("[!] Type 'shutdown win' and press Enter to exit Windows.\n")
    while True:
        cmd = get_win_input("Program Manager> ")
        if cmd.lower() == "shutdown win" or cmd.lower() == "turnoff": return 
        elif cmd.lower() == "cal":
            if run_calculator(): return 
            else: clear_screen(); print("=== WINDOWS 3.0 ===\n  [Returned from Calculator]\n")
        elif cmd.lower() == "msword":
            if run_msword(): return 
            else: clear_screen(); print("=== WINDOWS 3.0 ===\n  [Returned from Word]\n")
        elif cmd.lower() == "fileep":
            if run_fileep(): return
            else: clear_screen(); print("=== WINDOWS 3.0 ===\n  [Returned from File Explorer]\n")
        elif cmd.lower() == "bs":
            if run_browser(): return
            else: clear_screen(); print("=== WINDOWS 3.0 ===\n  [Returned from Browser]\n")
        elif cmd.strip() == "": continue
        else: print(f"Bad command or file name: {cmd}")

def show_apple_mac_os():
    clear_screen()
    print(" macOS Ventura (Simulator)")
    print("--------------------------------------------------")
    print("  +--------------------------------------------+")
    print("  | Virtual Machine: MS-DOS 6.22 / Win 3.0     |")
    print("  |--------------------------------------------|")
    print("  |      [ WINDOWS 3.0 PROFESSIONAL ]          |")
    print("  +--------------------------------------------+")
    print("\n[!] Press any key to exit macOS and return to DOS.\n")

def show_settings_app_screen():
    clear_screen()
    print("==================================================")
    print("           WINDOWS 3.0 - SYSTEM SETTINGS")
    print("==================================================")
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
            print("  dir        - List files\n  win        - Start Windows 3.0\n  apple mac  - Run macOS VM\n  settings   - System Settings\n  restart    - Restart\n  shutdown   - Shutdown\n  cls        - Clear screen")
        elif command == "dir":
            print(" Volume in drive C is MS-DOS_6\n Directory of C:\\\n\nDOS          <DIR>     10-25-26  10:00a\nWINDOWS      <DIR>     10-25-26  10:05a\nCOMMAND  COM     54876 10-20-26  10:00a\nAUTOEXEC BAT       128 10-20-26  10:00a\n")
        elif command == "win":
            show_windows_3_professional()
            print("Shutting down Windows 3.0...")
            show_loading_bar("Returning to MS-DOS", 3); time.sleep(0.5); clear_screen(); print("Returning to C:\\...\n")
        elif command in ["apple mac", "apple max", "app termux"]:
            show_apple_mac_os()
            get_single_key()
            show_loading_bar("Closing Virtual Machine", 2); clear_screen(); print("Returning to C:\\...\n")
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
                        clear_screen(); show_loading_bar("reinstalling.. ms-dos", 10)
                        while True:
                            if input("\nPlease type 'yes' to restart: ").strip().lower() == "yes": break
                        show_loading_bar("Restarting MS-DOS", 3); clear_screen(); settings_active = False 
                elif sub_cmd == "upytr":
                    print("\nUpdate system? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        print("\nPress enter 4 times.\n")
                        for i in range(4): input(f"({i+1}/4)...")
                        clear_screen(); show_loading_bar("updating msdos", 10)
                        while True:
                            if input("\nType 'yes' to restart: ").strip().lower() == "yes": break
                        show_loading_bar("Restarting MS-DOS", 3); clear_screen(); settings_active = False 
                elif sub_cmd == "shutoff":
                    print("\nForce shutdown? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        show_loading_bar("Force shutting down device", 10); clear_screen(); exit_program = True; settings_active = False
                elif sub_cmd == "f-restart":
                    print("\nForce restart? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        show_loading_bar("Force restarting device", 10); clear_screen(); settings_active = False 
                elif sub_cmd == "e-start":
                    print("\nEMERGENCY restart? (y/n): ", end="", flush=True)
                    ans = get_single_key().lower(); print(ans)
                    if ans == 'y':
                        show_loading_bar("EMERGENCY RESTARTING SYSTEM", 10); clear_screen(); settings_active = False 
        elif command == "shutdown":
            print("\nShutdown? (y/n): ", end="", flush=True)
            ans = get_single_key().lower(); print(ans)
            if ans == 'y':
                clear_screen(); print("\033[33m\n==================================================\n           SHUTTING DOWN MS-DOS...\n==================================================\n\033[0m")
                time.sleep(1.5); show_loading_bar("Shutting down system", 3); print("It is now safe to turn off your computer."); time.sleep(2); clear_screen(); exit_program = True
        elif command == "restart":
            print("\nRestart? (y/n): ", end="", flush=True)
            ans = get_single_key().lower(); print(ans)
            if ans == 'y':
                show_loading_bar("Restarting MS-DOS", 3); time.sleep(0.5); clear_screen(); print("Returning to C:\\...\n")
        elif command == "cls": clear_screen()
        elif command == "": continue
        else: print(f"Bad command or file name: {command}\n")
    except KeyboardInterrupt:
        print("\n\nUse 'shutdown' to quit properly.\n")
