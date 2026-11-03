import os
import time
import random

def clear_screen():
    os.system('clear')

def calculate_wpm(text, time_taken):
    # คำนวณจากจำนวนคำ หารด้วยเวลาที่ใช้ (วินาที) คูณ 60 เพื่อให้เป็นต่อนาที
    words = len(text.split())
    minutes = time_taken / 60
    if minutes > 0:
        return int(words / minutes)
    return 0

def calculate_accuracy(original, typed):
    # คำนวณความแม่นยำโดยการเทียบทีละตัวอักษร
    correct_chars = 0
    # ใช้ความยาวสูงสุดเพื่อไม่ให้การพิมพ์สั้นเกินไปได้เปรียบ
    length = max(len(original), len(typed))
    
    for i in range(min(len(original), len(typed))):
        if original[i] == typed[i]:
            correct_chars += 1
            
    if length == 0:
        return 0
    return int((correct_chars / length) * 100)

def main():
    # รวบรวมประโยคภาษาอังกฤษไว้ให้สุ่ม
    sentences = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a powerful programming language.",
        "Termux brings the power of Linux to Android.",
        "Practice makes perfect when learning to code.",
        "Artificial intelligence is changing the world.",
        "Keep calm and write more code."
    ]
sentences = [
    "Learning to write computer code is a very useful skill because it allows you to create new programs, solve complex problems, and understand how modern technology works in our daily lives.",
    "When you practice typing on a regular basis, your speed and accuracy will naturally improve over time, which makes it much easier to complete your homework and school assignments quickly.",
    "The quick brown fox jumps over the lazy dog, but the dog does not seem to mind at all because it is too tired after playing outside in the warm afternoon sun.",
    "Building a custom operating system simulator using Python on your Android phone is a great way to learn about file management, system commands, and user interface design.",
    "Always remember to save your work frequently when you are writing long documents, because unexpected power outages or system crashes can cause you to lose important data.",
    "The internet is a vast network that connects millions of computers around the world, allowing people to share information, communicate instantly, and access knowledge from anywhere.",
    "If you want to become a successful software developer, you should focus on writing clean code, learning how to debug errors, and collaborating effectively with other people.",
    "Reading books and articles every single day will expand your vocabulary, improve your communication skills, and open your mind to many different ideas and perspectives.",
    "The weather forecast predicts heavy rain and strong winds for tomorrow, so please make sure to bring an umbrella and wear a warm jacket before leaving the house.",
    "Artificial intelligence is rapidly changing the way we live and work, but it is important to use these new tools responsibly and ethically for the benefit of everyone."
]
    clear_screen()
    print("==================================================")
    print("        ⌨️  ENGLISH TYPING SPEED TEST ⌨️          ")
    print("==================================================")

    while True:
        # สุ่มเลือกประโยค
        target_sentence = random.choice(sentences)
        
        print("\nType the following sentence exactly as shown:\n")
        print(f"👉  {target_sentence}\n")
        
        input("Press Enter when you are ready to start...")
        
        # เริ่มจับเวลา
        start_time = time.time()
        
        # รับข้อความที่ผู้ใช้พิมพ์
        user_input = input("\nStart typing:\n> ")
        
        # หยุดจับเวลา
        end_time = time.time()
        time_taken = end_time - start_time

        # ประมวลผล
        wpm = calculate_wpm(user_input, time_taken)
        accuracy = calculate_accuracy(target_sentence, user_input)

        # แสดงผลลัพธ์
        print("\n" + "=" * 50)
        print("📊 RESULTS")
        print("=" * 50)
        print(f"⏱️  Time taken : {time_taken:.2f} seconds")
        print(f"🚀 Speed      : {wpm} WPM (Words Per Minute)")
        print(f"🎯 Accuracy   : {accuracy}%")
        
        if accuracy == 100:
            print("🌟 Perfect! You typed it exactly right.")
        elif accuracy >= 80:
            print("👍 Good job! Keep practicing.")
        else:
            print("💡 Don't worry, practice makes perfect!")

        print("=" * 50)
        
        # ถามว่าต้องการเล่นอีกรอบหรือไม่
        play_again = input("\nDo you want to try again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("\nThank you for playing! Goodbye. 👋")
            break
        clear_screen()

if __name__ == "__main__":
    main()
