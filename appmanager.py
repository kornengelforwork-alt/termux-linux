import os
import subprocess

# --- ตั้งค่าเริ่มต้น ---
# True = ซิมูเลเตอร์ (ไม่ทำจริง), False = ทำจริง
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

    while True:
        os.system('clear')
        print("==================================================")
        print("       🛠️ TERMUX APP MANAGER (v1.0) 🛠️          ")
        
        if SIMULATION_MODE:
            print("       MODE: [ 🛡️ SIMULATION (SAFE) ]              ")
        else:
            print("       MODE: [ ⚠️ REAL MODE (DANGEROUS) ]          ")
        print("==================================================")
        
        apps = get_installed_apps()
        
        # แสดงรายชื่อแอป (โชว์ 30 ตัวแรกเพื่อไม่ให้จอล้น)
        for i, app in enumerate(apps[:30], 1):
            if app in system_blacklist:
                print(f" [{i:03d}] ❌ {app} (SYSTEM)")
            else:
                print(f" [{i:03d}] 📦 {app}")
        
        if len(apps) > 30:
            print(f" ... and {len(apps)-30} more apps.")
            
        print("==================================================")
        print(" 📥 /apt <package_name or number> : Install via apt")
        print(" 📥 /dpkg <home/path/file.deb>    : Install local file")
        print(" 🗑️  [Number]                       : Remove App")
        print(" ⚙️  [s] Toggle Mode | [q] Quit")
        print("==================================================")
        
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
            
        # --- ฟีเจอร์ติดตั้งผ่าน apt ---
        elif choice.startswith('/apt '):
            arg = choice[5:].strip()
            if not arg:
                print("❌ Please specify a package name or number.")
                subprocess.run(['sleep', '1.5'])
                continue
                
            # ระบบจำเลข: ถ้าพิมพ์มาเป็นตัวเลข ให้ไปดึงชื่อแพ็กเกจจากลิสต์
            if arg.isdigit() and 1 <= int(arg) <= len(apps):
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
                
            # แปลง home/ เป็น /storage/emulated/0/
            if path.startswith('home/'):
                path = path.replace('home/', '/storage/emulated/0/', 1)
                
            print(f"\n⏳ Preparing to install file: {path}")
            
            if SIMULATION_MODE:
                print("🛡️ SIMULATION: Would run dpkg -i", path)
                print("(Note: dpkg doesn't have a real simulation mode, so no output will be shown here.)")
            else:
                print("🔥 REAL INSTALL: dpkg -i", path)
                subprocess.run(['dpkg', '-i', path])
                
            input("\nPress Enter to continue...")

        # --- ฟีเจอร์ถอนการติดตั้ง ---
        elif choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(apps):
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
