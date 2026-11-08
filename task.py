import os
import json
import sys
import time

# กำหนดชื่อโฟลเดอร์และไฟล์
FOLDER_NAME = "TaskManager"
FILE_NAME = os.path.join(FOLDER_NAME, "tasks.json")

def setup_folder():
    # ถ้าไม่มีโฟลเดอร์ ให้สร้างขึ้นมาใหม่
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

def load_tasks():
    setup_folder() # เช็กและสร้างโฟลเดอร์ก่อนโหลด
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def clear_screen():
    os.system('clear')

def main():
    tasks = load_tasks()

    while True:
        clear_screen()
        print("==================================================")
        print("       📝 TERMINAL TASK MANAGER 📝                ")
        print("==================================================")
        
        if not tasks:
            print("  (ยังไม่มีรายการงาน)")
        else:
            for i, task in enumerate(tasks, 1):
                status = "[✔]" if task.get("done", False) else "[ ]"
                print(f"  {i}. {status} {task['name']}")
                
        print("==================================================")
        print(" [1] เพิ่มงานใหม่")
        print(" [2] ทำเครื่องหมายว่าเสร็จแล้ว / ยกเลิก")
        print(" [3] ลบงาน")
        print(" [4] ออกจากโปรแกรม")
        print("==================================================")
        
        choice = input(" เลือกเมนู (1-4): ").strip()

        if choice == '1':
            new_task = input("\nพิมพ์ชื่องานที่ต้องการเพิ่ม: ").strip()
            if new_task:
                tasks.append({"name": new_task, "done": False})
                save_tasks(tasks)
                print("\n✅ เพิ่มงานเรียบร้อยแล้ว!")
            else:
                print("\n❌ ยกเลิก: ไม่ได้พิมพ์ชื่องาน")
            time.sleep(1.5)

        elif choice == '2':
            if not tasks:
                print("\n❌ ไม่มีงานให้ทำเครื่องหมาย")
                time.sleep(1.5)
                continue
            
            task_num = input("\nพิมพ์หมายเลขงานที่ทำเสร็จแล้ว: ").strip()
            if task_num.isdigit():
                index = int(task_num) - 1
                if 0 <= index < len(tasks):
                    tasks[index]["done"] = not tasks[index]["done"]
                    save_tasks(tasks)
                    print("\n✅ อัปเดตสถานะเรียบร้อยแล้ว!")
                else:
                    print("\n❌ หมายเลขไม่ถูกต้อง")
            else:
                print("\n❌ กรุณาพิมพ์เป็นตัวเลข")
            time.sleep(1.5)

        elif choice == '3':
            if not tasks:
                print("\n❌ ไม่มีงานให้ลบ")
                time.sleep(1.5)
                continue

            task_num = input("\nพิมพ์หมายเลขงานที่ต้องการลบ: ").strip()
            if task_num.isdigit():
                index = int(task_num) - 1
                if 0 <= index < len(tasks):
                    deleted = tasks.pop(index)
                    save_tasks(tasks)
                    print(f"\n🗑️ ลบงาน '{deleted['name']}' เรียบร้อยแล้ว!")
                else:
                    print("\n❌ หมายเลขไม่ถูกต้อง")
            else:
                print("\n❌ กรุณาพิมพ์เป็นตัวเลข")
            time.sleep(1.5)

        elif choice == '4':
            print("\nปิดโปรแกรม... ข้อมูลถูกบันทึกเรียบร้อยแล้ว 👋")
            break
        else:
            print("\n❌ กรุณาเลือก 1-4 เท่านั้น")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nปิดโปรแกรมกะทันหัน... 👋\n")
