import os
import time

# --- ระบบจัดการภาษา (Language System) ---
lang = "th"

texts = {
    "th": {
        "choose_lang": "🦉 ยินดีต้อนรับสู่ Little Owl Simulator 🦉\n\nเลือกภาษา / Select Language:\nพิมพ์ 't' สำหรับภาษาไทย\nพิมพ์ 'e' สำหรับ English\nเลือก: ",
        "invalid_lang": "❌ กรุณาพิมพ์ 't' หรือ 'e' เท่านั้น",
        "menu_title": "\n=========================================\n   🦉 เริ่มต้นการเลี้ยงน้องฮูก 🦉\n=========================================",
        "menu_cmds": "พิมพ์คำสั่งเพื่อดูแลน้องฮูก:\n [f] ป้อนนมเอนฟาโกร (Feed)\n [p] เล่นกับน้อง (Play)\n [s] พาน้องเข้านอน (Sleep)\n [q] ออกจากเกม (Quit)\n=========================================",
        "status_hunger": " 🍼 ความอิ่มท้อง (Enfagrow) : {val}/100",
        "status_happy": " 🎈 ความสุข                 : {val}/100",
        "status_energy": " 💤 พลังงาน                 : {val}/100",
        "warn_hunger": "\n🚨 น้องฮูกร้องไห้! หิวนมเอนฟาโกรมากๆ เลย",
        "warn_happy": "\n😢 น้องฮูกงอน! ไม่มีใครมาเล่นด้วยเลย",
        "warn_energy": "\n😴 น้องฮูกง่วงนอนมาก ตาแทบปิดแล้ว",
        "prompt": "\nทำอะไรกับน้องฮูกดี? (f/p/s/q): ",
        "act_feed": "\n🍼 อื๊บ อื๊บ! น้องฮูกกินนมเอนฟาโกรอร่อยจังเลย",
        "act_play": "\n🎈 น้องฮูกกระโดดโลดเต้นดีใจที่ได้เล่นด้วย!",
        "act_play_tired": "\n😴 น้องฮูกง่วงเกินไป จะเล่นไม่ไหวแล้วนะ",
        "act_sleep": "\n💤 Zzz... น้องฮูกหลับปุ๋ย ฝันหวานถึงคุณยาย",
        "act_quit": "\n👋 บ๊ายบายน้องฮูก! ไว้มาเล่นใหม่นะ",
        "act_invalid": "\n❌ น้องฮูกทำหน้างง (พิมพ์ f, p, s, หรือ q เท่านั้นนะ)"
    },
    "en": {
        "choose_lang": "🦉 Welcome to Little Owl Simulator 🦉\n\nSelect Language / เลือกภาษา:\nType 't' for Thai\nType 'e' for English\nChoose: ",
        "invalid_lang": "❌ Please type only 't' or 'e'",
        "menu_title": "\n=========================================\n   🦉 Start Raising Little Owl 🦉\n=========================================",
        "menu_cmds": "Type commands to take care of Little Owl:\n [f] Feed Enfagrow milk\n [p] Play with Little Owl\n [s] Put Little Owl to sleep\n [q] Quit game\n=========================================",
        "status_hunger": " 🍼 Hunger (Enfagrow) : {val}/100",
        "status_happy": " 🎈 Happiness         : {val}/100",
        "status_energy": " 💤 Energy            : {val}/100",
        "warn_hunger": "\n🚨 Little Owl is crying! Very hungry for Enfagrow.",
        "warn_happy": "\n😢 Little Owl is sulking! No one to play with.",
        "warn_energy": "\n😴 Little Owl is very sleepy, eyes are closing.",
        "prompt": "\nWhat will you do with Little Owl? (f/p/s/q): ",
        "act_feed": "\n🍼 Gulp gulp! Little Owl loves Enfagrow milk.",
        "act_play": "\n🎈 Little Owl jumps with joy playing with you!",
        "act_play_tired": "\n😴 Little Owl is too sleepy to play.",
        "act_sleep": "\n💤 Zzz... Little Owl is fast asleep, dreaming of grandma.",
        "act_quit": "\n👋 Bye bye Little Owl! Come play again soon.",
        "act_invalid": "\n❌ Little Owl looks confused (Type f, p, s, or q only)"
    }
}

def t(key, **kwargs):
    text = texts[lang].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

# --- ข้อมูลสถานะของน้องฮูก ---
hunger = 50
happiness = 50
energy = 50

def clear_screen():
    os.system('clear')

def show_little_owl():
    print("        ___")
    print("       (o,o)   < Little Owl")
    print("       /)  )")
    print("      --\"-\"--")
    print("=======================")

def print_status():
    show_little_owl()
    print(t("status_hunger", val=hunger))
    print(t("status_happy", val=happiness))
    print(t("status_energy", val=energy))
    print("=======================")

def main():
    global lang, hunger, happiness, energy

    clear_screen()
    # --- เริ่มต้นเลือกภาษา ---
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

    clear_screen()
    print(t("menu_title"))
    print(t("menu_cmds"))
    time.sleep(3)

    while True:
        clear_screen()
        print_status()
        
        # เช็กว่าน้องฮูกงอนหรือหิวเกินไปไหม
        if hunger <= 10:
            print(t("warn_hunger"))
        if happiness <= 10:
            print(t("warn_happy"))
        if energy <= 10:
            print(t("warn_energy"))

        choice = input(t("prompt")).strip().lower()

        if choice == 'f':
            hunger = min(100, hunger + 20)
            happiness = min(100, happiness + 5)
            print(t("act_feed"))
            
        elif choice == 'p':
            if energy < 15:
                print(t("act_play_tired"))
            else:
                happiness = min(100, happiness + 20)
                energy = max(0, energy - 10)
                hunger = max(0, hunger - 10)
                print(t("act_play"))
                
        elif choice == 's':
            energy = min(100, energy + 30)
            hunger = max(0, hunger - 5)
            print(t("act_sleep"))
            
        elif choice == 'q':
            print(t("act_quit"))
            break
        else:
            print(t("act_invalid"))
            
        # เวลาผ่านไป สถานะจะลดลงเรื่อยๆ
        time.sleep(1.5)
        hunger = max(0, hunger - 5)
        happiness = max(0, happiness - 3)
        energy = max(0, energy - 2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋\n")
