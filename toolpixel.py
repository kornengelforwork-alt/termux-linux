import os
import time

# ฟอนต์ตัวเลขแบบพิกเซล 3x5
digits = {
    '0': ["###", "# #", "# #", "# #", "###"],
    '1': ["  #", "  #", "  #", "  #", "  #"],
    '2': ["###", "  #", "###", "#  ", "###"],
    '3': ["###", "  #", "###", "  #", "###"],
    '4': ["# #", "# #", "###", "  #", "  #"],
    '5': ["###", "#  ", "###", "  #", "###"],
    '6': ["###", "#  ", "###", "# #", "###"],
    '7': ["###", "  #", "  #", "  #", "  #"],
    '8': ["###", "# #", "###", "# #", "###"],
    '9': ["###", "# #", "###", "  #", "###"],
    ':': ["   ", " # ", "   ", " # ", "   "],
    ' ': ["   ", "   ", "   ", "   ", "   "]
}

def print_pixel_text(text):
    # สร้างตัวเลข 5 บรรทัด
    lines = ["", "", "", "", ""]
    for char in text:
        if char in digits:
            for i in range(5):
                lines[i] += digits[char][i] + "  " # เว้นวรรคระหว่างตัวเลข
    
    for line in lines:
        print("      " + line)

def clear_screen():
    os.system('clear')

def main():
    try:
        while True:
            clear_screen()
            current_time = time.strftime("%H:%M:%S")
            current_date = time.strftime("%d/%m/%Y")
            
            print("\n\n=========================================")
            print("       ⏰ PIXEL ART CLOCK & CALENDAR      ")
            print("=========================================\n")
            
            print_pixel_text(current_time)
            
            print("\n\n=========================================")
            print(f"             Date: {current_date}")
            print("        Press 'CTRL + C' to EXIT")
            print("=========================================\n")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nปิดนาฬิกาเรียบร้อยแล้วครับ 👋\n")

if __name__ == "__main__":
    main()

