import os
import sys
import time

lang = "th"

texts = {
    "th": {
        "title": "🔐 โปรแกรมเข้ารหัสและถอดรหัสข้อความ 🔐",
        "choose_lang": "เลือกภาษา / Select Language:\nพิมพ์ 't' สำหรับภาษาไทย\nพิมพ์ 'e' สำหรับ English\nเลือก: ",
        "invalid_lang": "❌ กรุณาพิมพ์ 't' หรือ 'e' เท่านั้น",
        "menu": "\n[1] เข้ารหัสข้อความ (Encrypt)\n[2] ถอดรหัสข้อความ (Decrypt)\n[3] ออกจากโปรแกรม (Exit)\nเลือกเมนู: ",
        "invalid_menu": "❌ กรุณาพิมพ์ 1, 2 หรือ 3 เท่านั้น",
        "enter_text": "พิมพ์ข้อความของคุณ: ",
        "enter_key": "ใส่รหัสลับ (ตัวเลข เช่น 3): ",
        "invalid_key": "❌ กรุณาใส่เฉพาะตัวเลขเท่านั้น!",
        "encrypting": "\n⏳ กำลังเข้ารหัส...",
        "decrypting": "\n⏳ กำลังถอดรหัส...",
        "result": "\n✅ ผลลัพธ์: {result}\n",
        "press_enter": "(กด Enter เพื่อกลับไปหน้าเมนู...)",
        "exit": "\nปิดโปรแกรมเรียบร้อยแล้วครับ 👋\n"
    },
    "en": {
        "title": "🔐 TEXT ENCRYPTOR & DECRYPTOR 🔐",
        "choose_lang": "Select Language / เลือกภาษา:\nType 't' for Thai\nType 'e' for English\nChoose: ",
        "invalid_lang": "❌ Please type only 't' or 'e'",
        "menu": "\n[1] Encrypt Text\n[2] Decrypt Text\n[3] Exit\nSelect menu: ",
        "invalid_menu": "❌ Please type only 1, 2, or 3",
        "enter_text": "Enter your text: ",
        "enter_key": "Enter secret key (number e.g., 3): ",
        "invalid_key": "❌ Please enter numbers only!",
        "encrypting": "\n⏳ Encrypting...",
        "decrypting": "\n⏳ Decrypting...",
        "result": "\n✅ Result: {result}\n",
        "press_enter": "(Press Enter to return to menu...)",
        "exit": "\nProgram closed successfully 👋\n"
    }
}

def t(key, **kwargs):
    text = texts[lang].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def caesar_cipher(text, key, mode):
    result = ""
    if mode == 'decrypt':
        key = -key
        
    for char in text:
        if char.isalpha():
            # จัดการตัวพิมพ์เล็ก
            if char.islower():
                start = ord('a')
                result += chr((ord(char) - start + key) % 26 + start)
            # จัดการตัวพิมพ์ใหญ่
            else:
                start = ord('A')
                result += chr((ord(char) - start + key) % 26 + start)
        else:
            # ถ้าเป็นตัวเลข สัญลักษณ์ หรือช่องว่าง ให้คงเดิมไว้
            result += char
    return result

def main():
    global lang
    os.system('clear')
    
    # --- Language Selection ---
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

    # --- Main Menu ---
    while True:
        os.system('clear')
        print("========================================")
        print(t("title"))
        print("========================================")
        
        choice = input(t("menu")).strip()
        
        if choice == '3':
            print(t("exit"))
            break
            
        elif choice in ['1', '2']:
            mode = 'encrypt' if choice == '1' else 'decrypt'
            
            print("\n" + "-" * 40)
            text_to_process = input(t("enter_text"))
            
            # รับค่า Key (ต้องเป็นตัวเลข)
            while True:
                key_input = input(t("enter_key")).strip()
                if key_input.isdigit():
                    key = int(key_input)
                    break
                else:
                    print(t("invalid_key"))
            
            # แสดงสถานะกำลังประมวลผล
            if mode == 'encrypt':
                print(t("encrypting"))
            else:
                print(t("decrypting"))
            time.sleep(1) # ดีเลย์ให้ดูสมจริง
            
            # ประมวลผล
            result = caesar_cipher(text_to_process, key, mode)
            
            # แสดงผลลัพธ์
            print(t("result", result=result))
            input(t("press_enter"))
            
        else:
            print(t("invalid_menu"))
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye! 👋\n")
