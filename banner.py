import os
import time

# --- ระบบจัดการภาษา (Language System) ---
lang = "th"

texts = {
    "th": {
        "choose_lang": "เลือกภาษา / Select Language:\nพิมพ์ 't' สำหรับภาษาไทย\nพิมพ์ 'e' สำหรับ English\nเลือก: ",
        "invalid_lang": "❌ กรุณาพิมพ์ 't' หรือ 'e' เท่านั้น",
        "title": "🎨 โปรแกรมสร้างป้ายชื่อยักษ์ (ASCII Banner) 🎨",
        "prompt": "พิมพ์ข้อความที่ต้องการ (A-Z, 0-9) หรือพิมพ์ 'quit' เพื่อออก: ",
        "generating": "\n⏳ กำลังสร้างป้ายชื่อ...\n",
        "invalid_text": "❌ กรุณาพิมพ์เฉพาะภาษาอังกฤษหรือตัวเลขเท่านั้น",
        "quit": "\nปิดโปรแกรมเรียบร้อยแล้วครับ 👋\n"
    },
    "en": {
        "choose_lang": "Select Language / เลือกภาษา:\nType 't' for Thai\nType 'e' for English\nChoose: ",
        "invalid_lang": "❌ Please type only 't' or 'e'",
        "title": "🎨 ASCII ART BANNER GENERATOR 🎨",
        "prompt": "Enter text to generate (A-Z, 0-9) or type 'quit' to exit: ",
        "generating": "\n⏳ Generating banner...\n",
        "invalid_text": "❌ Please enter only English letters or numbers.",
        "quit": "\nProgram closed successfully 👋\n"
    }
}

def t(key, **kwargs):
    text = texts[lang].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

# ฟอนต์ ASCII (ความสูง 5 บรรทัด)
font = {
    'A': [" ### ", "#   #", "#####", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#### ", "#   #", "#### "],
    'C': [" ####", "#    ", "#    ", "#    ", " ####"],
    'D': ["#### ", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#### ", "#    ", "#####"],
    'F': ["#####", "#    ", "#### ", "#    ", "#    "],
    'G': [" ####", "#    ", "#  ##", "#   #", " ####"],
    'H': ["#   #", "#   #", "#####", "#   #", "#   #"],
    'I': [" ### ", "  #  ", "  #  ", "  #  ", " ### "],
    'J': ["  ###", "   # ", "   # ", "#  # ", " ##  "],
    'K': ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#### ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    'S': [" ####", "#    ", " ### ", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "# # #", "## ##", "#   #"],
    'X': ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    'Y': ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "   # ", "  #  ", " #   ", "#####"],
    '0': [" ### ", "#  ##", "# # #", "##  #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "#   #", "   # ", "  #  ", "#####"],
    '3': ["#### ", "    #", " ### ", "    #", "#### "],
    '4': ["#   #", "#   #", "#####", "    #", "    #"],
    '5': ["#####", "#    ", "#### ", "    #", "#### "],
    '6': [" ### ", "#    ", "#### ", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", "  #  "],
    '8': [" ### ", "#   #", " ### ", "#   #", " ### "],
    '9': [" ### ", "#   #", " ####", "    #", " ### "],
    ' ': ["     ", "     ", "     ", "     ", "     "]
}

def generate_banner(text):
    lines = ["", "", "", "", ""]
    
    for char in text.upper():
        if char in font:
            for i in range(5):
                lines[i] += font[char][i] + "  " # เว้นวรรคระหว่างตัวอักษร
    
    for line in lines:
        print(line)

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

    # --- Main Loop ---
    while True:
        os.system('clear')
        print("========================================")
        print(t("title"))
        print("========================================\n")
        
        user_input = input(t("prompt")).strip()
        
        if user_input.lower() == 'quit':
            print(t("quit"))
            break
            
        if not user_input:
            continue
            
        print(t("generating"))
        time.sleep(1)
        
        print("\n")
        generate_banner(user_input)
        print("\n")
        
        input("(Press Enter to continue...)" )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye! 👋\n")
