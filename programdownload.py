import os
import sys
import time
import socket
import urllib.request
import urllib.parse

# --- ระบบจัดการภาษา (Language System) ---
lang = "th"

texts = {
    "th": {
        "choose_lang": "เลือกภาษา / Select Language:\nพิมพ์ 't' สำหรับภาษาไทย\nพิมพ์ 'e' สำหรับ English\nเลือก: ",
        "invalid_lang": "❌ กรุณาพิมพ์ 't' หรือ 'e' เท่านั้น",
        "check_net": "🔍 กำลังตรวจสอบการเชื่อมต่ออินเทอร์เน็ต...",
        "net_ok": "✅ เชื่อมต่ออินเทอร์เน็ตสำเร็จ!",
        "net_fail": "❌ ไม่พบการเชื่อมต่ออินเทอร์เน็ต! กรุณาเปิด WiFi หรือข้อมูลมือถือ",
        "mobile_warning": "⚠️ คุณกำลังใช้งานอินเทอร์เน็ตผ่านมือถือ (4G/5G) อยู่หรือไม่? (y/n): ",
        "switch_wifi": "คุณต้องการสลับไปใช้ WiFi เพื่อประหยัด Data หรือไม่? (y/n): ",
        "wifi_recommend": "💡 แนะนำ: กรุณาเปลี่ยนไปใช้ WiFi ก่อนดาวน์โหลดไฟล์ขนาดใหญ่",
        "enter_url": "\n🔗 พิมพ์ลิงก์ที่ต้องการดาวน์โหลด (หรือพิมพ์ '/quit' เพื่อออก): ",
        "invalid_url": "❌ ลิงก์ไม่ถูกต้อง! ต้องขึ้นต้นด้วย http:// หรือ https://",
        "confirm_dl": "📥 ต้องการดาวน์โหลดไฟล์นี้หรือไม่? (กด Enter เพื่อโหลด, พิมพ์ 'n' เพื่อยกเลิก): ",
        "dl_cancel": "❌ ยกเลิกการดาวน์โหลด",
        "dl_start": "⏳ กำลังดาวน์โหลด: {filename}...",
        "dl_success": "\n✅ ดาวน์โหลดสำเร็จ! บันทึกไว้ที่: {path}",
        "dl_error": "\n❌ เกิดข้อผิดพลาดในการดาวน์โหลด: {error}",
        "exit": "\n👋 ปิดโปรแกรมดาวน์โหลดเรียบร้อยแล้วครับ"
    },
    "en": {
        "choose_lang": "Select Language / เลือกภาษา:\nType 't' for Thai\nType 'e' for English\nChoose: ",
        "invalid_lang": "❌ Please type only 't' or 'e'",
        "check_net": "🔍 Checking internet connection...",
        "net_ok": "✅ Internet connected successfully!",
        "net_fail": "❌ No internet connection found! Please turn on WiFi or Mobile Data.",
        "mobile_warning": "⚠️ Are you currently using Mobile Data (4G/5G)? (y/n): ",
        "switch_wifi": "Do you want to switch to WiFi to save Data? (y/n): ",
        "wifi_recommend": "💡 Recommendation: Please switch to WiFi before downloading large files.",
        "enter_url": "\n🔗 Enter URL to download (or type '/quit' to exit): ",
        "invalid_url": "❌ Invalid URL! It must start with http:// or https://",
        "confirm_dl": "📥 Do you want to download this file? (Press Enter to download, type 'n' to cancel): ",
        "dl_cancel": "❌ Download cancelled",
        "dl_start": "⏳ Downloading: {filename}...",
        "dl_success": "\n✅ Download successful! Saved to: {path}",
        "dl_error": "\n❌ Download error: {error}",
        "exit": "\n👋 Downloader closed successfully."
    }
}

def t(key, **kwargs):
    text = texts[lang].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def check_internet():
    print(t("check_net"))
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print(t("net_ok"))
        return True
    except OSError:
        print(t("net_fail"))
        return False

# ฟังก์ชันใหม่: ดึงชื่อไฟล์และนามสกุลให้แม่นยำ
def get_real_filename(url):
    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path)
    
    # ถ้าไม่ได้นามสกุลมาจาก URL ให้ลองถามเซิร์ฟเวอร์
    if not filename or "." not in filename:
        try:
            req = urllib.request.Request(url, method='HEAD')
            with urllib.request.urlopen(req, timeout=5) as response:
                # 1. ลองดูจาก Content-Disposition (ชื่อไฟล์ที่แท้จริง)
                cd = response.headers.get('Content-Disposition')
                if cd and 'filename=' in cd:
                    filename = cd.split('filename=')[1].strip('"\' ')
                else:
                    # 2. ถ้าไม่มีชื่อ ลองดูจากชนิดไฟล์ (Content-Type)
                    ct = response.headers.get('Content-Type', '')
                    if 'zip' in ct: filename = "downloaded_file.zip"
                    elif 'pdf' in ct: filename = "downloaded_file.pdf"
                    elif 'image' in ct: filename = "downloaded_file.jpg"
                    elif 'text' in ct: filename = "downloaded_file.txt"
        except Exception:
            pass
            
    # ถ้ายังไม่ได้ชื่อ ให้ใช้ชื่อเริ่มต้นพร้อมนามสกุล .bin
    if not filename:
        filename = "downloaded_file.bin"
        
    return filename

def main():
    global lang
    os.system('clear')
    
    # 1. Language Selection
    while True:
        choice = input(t("choose_lang")).strip().lower()
        if choice == 't':
            lang = 'th'
            break
        elif choice == 'e':
            lang = 'en'
            break
        else:
            print(t("invalid_lang"))
    
    os.system('clear')
    # 2. Internet Check
    if not check_internet():
        return

    time.sleep(1)
    mobile_choice = input(t("mobile_warning")).strip().lower()
    if mobile_choice == 'y':
        switch_choice = input(t("switch_wifi")).strip().lower()
        if switch_choice == 'y':
            print(t("wifi_recommend"))
            time.sleep(2)
            return
        else:
            print(t("wifi_recommend"))
            time.sleep(1.5)

    # 3. URL Input Loop
    os.system('clear')
    while True:
        url = input(t("enter_url")).strip()
        
        if url.lower() == '/quit':
            print(t("exit"))
            break
            
        if not url.startswith(("http://", "https://")):
            print(t("invalid_url"))
            time.sleep(1.5)
            continue

        # 4. Download Confirmation
        print("🔍 กำลังตรวจสอบข้อมูลไฟล์จากเซิร์ฟเวอร์...")
        filename = get_real_filename(url)

        confirm = input(t("confirm_dl")).strip().lower()
        
        if confirm == 'n':
            print(t("dl_cancel"))
            time.sleep(1)
            os.system('clear')
            continue
        else:
            # 5. Download Process
            print(t("dl_start", filename=filename))
            
            download_path = f"/storage/emulated/0/Download/{filename}"
            
            try:
                urllib.request.urlretrieve(url, download_path)
                print(t("dl_success", path=download_path))
            except Exception as e:
                print(t("dl_error", error=e))
            
            print("\n" + "-"*40)
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye! 👋\n")

