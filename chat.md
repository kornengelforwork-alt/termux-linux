# 💬 Local Network Chat (Python Sockets)

[🇬🇧 English](#english) | [🇹🇭 ภาษาไทย](#thai)

---

## <a name="english"></a>🇬🇧 English

A simple, terminal-based chat application written in Python. It allows two devices on the same Local Area Network (LAN) or Wi-Fi to communicate with each other without needing an internet connection.

### ✨ Features
- **Server-Client Architecture:** Uses TCP sockets for reliable communication.
- **Real-time Messaging:** Chat instantly over the local network.
- **No Internet Required:** Works completely offline on a local router or hotspot.

### 🚀 How to Use
1. **Start the Server (Device 1):**
   Run `python chatserver.py` on the first device. It will wait for a connection.
2. **Start the Client (Device 2):**
   Run `python chatuser.py` on the second device. 
   *(Note: You may need to edit `SERVER_IP` in the `chatuser.py` file to match the local IP address of the server device).*
3. **Chat:** Type your message and press Enter to send.

---

## <a name="thai"></a>🇹🇭 ภาษาไทย (For Thai Users)

โปรแกรมแชทผ่าน Terminal ที่เขียนด้วยภาษา Python สำหรับการสื่อสารระหว่างอุปกรณ์ 2 เครื่องที่เชื่อมต่ออยู่ในวง Wi-Fi หรือ Local Network (LAN) เดียวกัน โดยไม่ต้องใช้อินเทอร์เน็ต

### ✨ ฟีเจอร์หลัก
- **ระบบ Server-Client:** ใช้ TCP Socket เพื่อการรับส่งข้อมูลที่เสถียร
- **แชทแบบเรียลไทม์:** พิมพ์คุยกันได้ทันทีผ่านวง LAN
- **ไม่ต้องใช้อินเทอร์เน็ต:** ทำงานแบบออฟไลน์ 100% ผ่านเราเตอร์หรือฮอตสปอต

### 🚀 วิธีใช้งาน
1. **เปิดฝั่ง Server (เครื่องที่ 1):**
   รันคำสั่ง `python chatserver.py` เครื่องจะรอการเชื่อมต่อ
2. **เปิดฝั่ง Client (เครื่องที่ 2):**
   รันคำสั่ง `python chatuser.py` 
   *(หมายเหตุ: อาจต้องแก้ไข `SERVER_IP` ในไฟล์ `chatuser.py` ให้เป็น IP ของเครื่องที่รัน Server)*
3. **เริ่มแชท:** พิมพ์ข้อความแล้วกด Enter เพื่อส่ง

