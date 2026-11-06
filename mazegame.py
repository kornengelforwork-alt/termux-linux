import os
import sys
import termios
import tty

# แผนที่เขาวงกตขนาดใหญ่ 15x15 (P = ผู้เล่น, E = ทางออก, # = กำแพง)
maze = [
    "###############",
    "#P    #       #",
    "# ### # ##### #",
    "# #   #     # #",
    "# # ##### # # #",
    "# #       # # #",
    "# ####### # # #",
    "#       # # # #",
    "####### # # # #",
    "#       # # # #",
    "# ####### # # #",
    "# #       #   #",
    "# # ######### #",
    "#   #        E#",
    "###############"
]

def clear_screen():
    os.system('clear')

def print_maze(steps):
    clear_screen()
    print("=========================================")
    print(f" 🏃 MAZE GAME | Steps: {steps} | W/A/S/D | Q: Quit")
    print("=========================================\n")
    for row in maze:
        # แสดงผลโดยแทนที่ช่องว่างด้วยจุด เพื่อให้เห็นรอยทางที่เดินผ่าน
        print("  " + row.replace(" ", "·"))
    print("\n=========================================")

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = os.read(fd, 1).decode('utf-8', errors='ignore')
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old_settings)
    return ch

def find_player():
    for r_idx, row in enumerate(maze):
        for c_idx, char in enumerate(row):
            if char == 'P':
                return r_idx, c_idx
    return None, None

def main():
    steps = 0
    while True:
        print_maze(steps)
        player_r, player_c = find_player()

        key = get_key().lower()

        if key == 'q':
            clear_screen()
            print("\nออกจากเกมแล้ว ขอบคุณที่เล่นครับ! 👋")
            break

        new_r, new_c = player_r, player_c
        if key == 'w': new_r -= 1
        elif key == 's': new_r += 1
        elif key == 'a': new_c -= 1
        elif key == 'd': new_c += 1
        else: continue

        # ตรวจสอบการชนกำแพง
        if maze[new_r][new_c] != '#':
            if maze[new_r][new_c] == 'E':
                print_maze(steps)
                print(f"\n🎉 ยินดีด้วย! คุณหาทางออกเจอแล้วใน {steps} ก้าว! 🎉")
                break
            
            # อัปเดตตำแหน่ง: เปลี่ยนที่เก่าเป็นจุด (รอยเท้า) และที่ใหม่เป็น P
            maze[player_r] = maze[player_r][:player_c] + '.' + maze[player_r][player_c+1:]
            maze[new_r] = maze[new_r][:new_c] + 'P' + maze[new_r][new_c+1:]
            steps += 1

if __name__ == "__main__":
    main()
