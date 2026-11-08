import os
import subprocess
import math

# --- ตั้งค่าเริ่มต้น ---
SIMULATION_MODE = True 

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

    # ตัวแปรสำหรับการแบ่งหน้า
    current_page = 1
    items_per_page = 20

    while True:
        os.system('clear')
        print("==================================================")
        print("       🛠️ TERMUX APP MANAGER (v1.1) 🛠️          ")
        
        if SIMULATION_MODE:
            print("       MODE: [ 🛡️ SIMULATION (SAFE) ]              ")
        else:
            print("       MODE: [ ⚠️ REAL MODE (DANGEROUS) ]          ")
        print("==================================================")
        
        apps = get_installed_apps()
        total_apps = len(apps)
        total_pages = math.ceil(total_apps / items_per_page)
        
        # คำนวณช่วงแอปที่จะแสดงในหน้านี้
        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_apps)
        
        # แสดงรายชื่อแอป
        for i in range(start_idx, end_idx):
            app = apps[i]
            display_num = i + 1
            if app in system_blacklist:
                print(f" [{display_num:03d}] ❌ {app} (SYSTEM)")
            else:
                print(f" [{display_num:03d}] 📦 {app}")
        
        print("==================================================")
        print(f" Page {current_page}/{total_pages} (Total: {total_apps} apps)")
        print(" 📥 /apt <name>  | 📥 /dpkg <path> | 🗑️ [Num] Remove")
        print(" 🔍 /find <name> | ⚙️ [s] Toggle Mode | [q] Quit")
        
        if current_page < total_pages:
            print(" ⏩ [n] Next Page")
        if current_page > 1:
            print(" ⏪ [p] Previous Page")
        print("==================================================")
        
        choice = input(" AppManager> ").strip()
        
        # --- คำสั่งพื้นฐาน ---
        if choice.lower() == 'q':
            print("\nExiting App Manager. Goodbye! 👋")
            break
            
        elif choice.lower() == 's':
            SIMULATION_MODE = not SIMULATION_MODE
            print(f"\n🔄 Mode changed to: {'SIMULATION' if SIMULATION_MODE else 'REAL'}")
            subprocess.run(['sleep', '1.5'])
            
        elif choice.lower() == 'n':
            if current_page < total_pages:
                current_page += 1
        elif choice.lower() == 'p':
            if current_page > 1:
                current_page -= 1
                
        # --- ฟีเจอร์ค้นหา ---
        elif choice.startswith('/find '):
            keyword = choice[6:].strip().lower()
            found_apps = [app for app in apps if keyword in app.lower()]
            
            if not found_apps:
                print(f"\n❌ No apps found matching '{keyword}'.")
                subprocess.run(['sleep', '2'])
            else:
                print(f"\n🔍 Found {len(found_apps)} apps matching '{keyword}':")
                for app in found_apps:
                    # หาลำดับที่แท้จริงของแอปในลิสต์ทั้งหมด
                    real_index = apps.index(app) + 1
                    print(f" [{real_index:03d}] {app}")
                input("\nPress Enter to continue...")

        # --- ฟีเจอร์ติดตั้งผ่าน apt ---
        elif choice.startswith('/apt '):
            arg = choice[5:].strip()
            if not arg:
                print("❌ Please specify a package name or number.")
                subprocess.run(['sleep', '1.5'])
                continue
                
            if arg.isdigit() and 1 <= int(arg) <= total_apps:
                package_name = apps[int(arg)-1]
            else:
                package_name = arg
                
            print(f"\n⏳ Preparing to install: {package_name}")
            
            if SIMULATION_MODE:
                print("🛡️ SIMULATING: apt install", package_name)
                subprocess.run(['apt', 'install', package_name, '-s'])
            else:
                print("🔥 REAL INSTALL: apt install", package_name)
                subprocess.run(['apt', 'install', package_name, '-y'])
                
            input("\nPress Enter to continue...")

        # --- ฟีเจอร์ติดตั้งผ่าน dpkg ---
        elif choice.startswith('/dpkg '):
            path = choice[6:].strip()
            if not path:
                print("❌ Please specify a file path.")
                subprocess.run(['sleep', '1.5'])
                continue
                
            if path.startswith('home/'):
                path = path.replace('home/', '/storage/emulated/0/', 1)
                
            print(f"\n⏳ Preparing to install file: {path}")
            
            if SIMULATION_MODE:
                print("🛡️ SIMULATION: Would run dpkg -i", path)
            else:
                print("🔥 REAL INSTALL: dpkg -i", path)
                subprocess.run(['dpkg', '-i', path])
                
            input("\nPress Enter to continue...")

        # --- ฟีเจอร์ถอนการติดตั้ง ---
        elif choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < total_apps:
                app_to_remove = apps[index]
                
                if app_to_remove in system_blacklist:
                    print(f"\n🚨 DANGER! Cannot remove '{app_to_remove}' (System App).")
                    subprocess.run(['sleep', '2'])
                    continue

                confirm = input(f"\n⚠️ UNINSTALL '{app_to_remove}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    if SIMULATION_MODE:
                        print(f"\n🛡️ SIMULATING purge of {app_to_remove}...\n")
                        subprocess.run(['apt', 'purge', app_to_remove, '-s'])
                    else:
                        print(f"\n🔥 REAL PURGING {app_to_remove}...\n")
                        subprocess.run(['apt', 'purge', app_to_remove, '-y'])
                    
                    input("\nPress Enter to return...")
            else:
                print("❌ Invalid number.")
                subprocess.run(['sleep', '1.5'])
        else:
            print("❌ Invalid command.")
            subprocess.run(['sleep', '1.5'])

if __name__ == "__main__":
    main()
