import os
import subprocess
import math
import re
import sys

# --- ตั้งค่าเริ่มต้น ---
SIMULATION_MODE = True 

# ฟังก์ชันล้างหน้าจอแบบใหม่ (เร็วกว่า os.system('clear') และไม่ค้าง)
def clear_screen():
    print("\033[2J\033[H", end="", flush=True)

def get_installed_apps():
    try:
        output = subprocess.check_output(['dpkg-query', '-Wf', '${Package}\n']).decode('utf-8')
        apps = [app for app in output.split('\n') if app]
        apps.sort()
        return apps
    except Exception:
        return []

def main():
    global SIMULATION_MODE
    system_blacklist = ['bash', 'termux-tools', 'coreutils', 'apt', 'dpkg', 'libc++', 'openssl']

    current_page = 1
    items_per_page = 20

    while True:
        clear_screen()
        print("==================================================")
        print("       🛠️ TERMUX APP MANAGER (v1.3) 🛠️          ")
        
        if SIMULATION_MODE:
            print("       MODE: [ 🛡️ SIMULATION (SAFE) ]              ")
        else:
            print("       MODE: [ ⚠️ REAL MODE (DANGEROUS) ]          ")
        print("==================================================")
        
        apps = get_installed_apps()
        total_apps = len(apps)
        total_pages = math.ceil(total_apps / items_per_page)
        
        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_apps)
        
        for i in range(start_idx, end_idx):
            app = apps[i]
            display_num = i + 1
            if app in system_blacklist:
                print(f" [{display_num:03d}] ❌ {app} (SYSTEM)")
            else:
                print(f" [{display_num:03d}] 📦 {app}")
        
        print("==================================================")
        print(f" Page {current_page}/{total_pages} (Total: {total_apps} apps)")
        print(" 📥 /apt <name1> <name2> | 📥 /dpkg <path1> <path2>")
        print(" 🗑️ [Num1] [Num2] ...      | 🔍 /find <name>")
        print(" ⚙️ [s] Toggle Mode | [q] Quit")
        
        if current_page < total_pages: print(" ⏩ [n] Next Page")
        if current_page > 1: print(" ⏪ [p] Previous Page")
        print("==================================================")
        
        sys.stdout.flush() # บังคับให้แสดงผลเมนูก่อนรับค่า
        choice = input(" AppManager> ").strip()
        
        # --- ออกจากโปรแกรม ---
        if choice.lower() == 'q':
            print("\nExiting App Manager. Goodbye! 👋")
            break
            
        # --- สลับโหมด ---
        elif choice.lower() == 's':
            SIMULATION_MODE = not SIMULATION_MODE
            print(f"\n🔄 Mode changed to: {'SIMULATION' if SIMULATION_MODE else 'REAL'}")
            subprocess.run(['sleep', '1.5'])
            
        # --- แบ่งหน้า ---
        elif choice.lower() == 'n':
            if current_page < total_pages: current_page += 1
        elif choice.lower() == 'p':
            if current_page > 1: current_page -= 1
                
        # --- ค้นหา ---
        elif choice.startswith('/find '):
            keyword = choice[6:].strip().lower()
            found_apps = [app for app in apps if keyword in app.lower()]
            if not found_apps:
                print(f"\n❌ No apps found matching '{keyword}'.")
                subprocess.run(['sleep', '2'])
            else:
                print(f"\n🔍 Found {len(found_apps)} apps:")
                for app in found_apps:
                    real_index = apps.index(app) + 1
                    print(f" [{real_index:03d}] {app}")
                print("\n\n\n")
                input("Press Enter to continue...")

        # --- ติดตั้งหลายแอปผ่าน apt ---
        elif choice.startswith('/apt '):
            args = choice[5:].strip().split()
            if not args: continue
                
            packages = []
            for arg in args:
                if arg.isdigit() and 1 <= int(arg) <= total_apps:
                    packages.append(apps[int(arg)-1])
                else:
                    packages.append(arg)
                    
            print(f"\n⏳ Preparing to install: {', '.join(packages)}")
            
            if SIMULATION_MODE:
                print(f"🛡️ SIMULATING: apt install {' '.join(packages)} -s\n")
                subprocess.run(['apt', 'install'] + packages + ['-s'])
            else:
                print(f"🔥 REAL INSTALL: apt install {' '.join(packages)}\n")
                subprocess.run(['apt', 'install'] + packages + ['-y'])
                
            print("\n\n\n")
            input("Press Enter to return to menu...")

        # --- ติดตั้งหลายไฟล์ผ่าน dpkg ---
        elif choice.startswith('/dpkg '):
            paths = choice[6:].strip().split()
            if not paths: continue
                
            processed_paths = []
            for path in paths:
                if path.startswith('home/'):
                    path = path.replace('home/', '/storage/emulated/0/', 1)
                processed_paths.append(path)
                
            print(f"\n⏳ Preparing to install files: {', '.join(processed_paths)}")
            
            if SIMULATION_MODE:
                print(f"🛡️ SIMULATION: Would run dpkg -i {' '.join(processed_paths)}")
            else:
                print(f"🔥 REAL INSTALL: dpkg -i {' '.join(processed_paths)}\n")
                subprocess.run(['dpkg', '-i'] + processed_paths)
                
            print("\n\n\n")
            input("Press Enter to return to menu...")

        # --- ถอนการติดตั้งหลายแอป ---
        elif re.search(r'\d', choice):
            tokens = re.split(r'[,\s]+', choice)
            targets = []
            
            for token in tokens:
                if token.isdigit():
                    index = int(token) - 1
                    if 0 <= index < total_apps:
                        targets.append(apps[index])
            
            if not targets:
                print("❌ No valid app numbers found.")
                subprocess.run(['sleep', '1.5'])
                continue
                
            blocked = [app for app in targets if app in system_blacklist]
            if blocked:
                print(f"\n🚨 DANGER! Cannot remove system apps: {', '.join(blocked)}")
                subprocess.run(['sleep', '2'])
                continue

            print(f"\n⚠️ You are about to UNINSTALL: {', '.join(targets)}")
            confirm = input("Are you sure? (y/n): ").strip().lower()
            
            if confirm == 'y':
                if SIMULATION_MODE:
                    print(f"\n🛡️ SIMULATING purge of: {', '.join(targets)}\n")
                    subprocess.run(['apt', 'purge'] + targets + ['-s'])
                else:
                    print(f"\n🔥 REAL PURGING: {', '.join(targets)}\n")
                    subprocess.run(['apt', 'purge'] + targets + ['-y'])
                
                print("\n\n\n")
                input("Press Enter to return to menu...")
        else:
            print("❌ Invalid command.")
            subprocess.run(['sleep', '1.5'])

if __name__ == "__main__":
    main()
