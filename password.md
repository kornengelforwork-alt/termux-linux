# 🔐 Text Encryptor & Decryptor

[🇬🇧 English](#english) | [🇹🇭 ภาษาไทย](#thai)

---

## <a name="english"></a>🇬🇧 English

A simple yet powerful Command-Line Interface (CLI) tool for encrypting and decrypting text using the classic **Caesar Cipher** method. It allows you to shift letters by a specific number (Key) to hide your messages from prying eyes.

### ✨ Features
- **Bilingual Support:** Choose Thai or English at the start.
- **Encrypt & Decrypt:** Easily encode or decode messages.
- **Case-Sensitive:** Preserves uppercase and lowercase letters correctly (e.g., 'W' becomes 'C' with Key 6).
- **Safe Formatting:** Only shifts English letters (A-Z, a-z). Numbers, spaces, and symbols remain untouched.

### 🚀 How to Use
1. Run the tool: `python encryptor.py`
2. Select Language: Type `t` for Thai or `e` for English.
3. Choose an option from the menu:
   - Type `1` to **Encrypt** (Hide the message).
   - Type `2` to **Decrypt** (Reveal the message).
   - Type `3` to **Exit**.
4. Enter your text (e.g., `Hello World`).
5. Enter the secret Key (must be a number, e.g., `3`).
6. The program will display the encrypted or decrypted result.

---

## <a name="thai"></a>🇹🇭 ภาษาไทย (For Thai Users)

โปรแกรมแบบ Command-Line Interface (CLI) สำหรับการเข้ารหัสและถอดรหัสข้อความ โดยใช้วิธีการเลื่อนตัวอักษรแบบคลาสสิกที่เรียกว่า **Caesar Cipher** เหมาะสำหรับการส่งข้อความลับให้เพื่อน โดยใช้ตัวเลข (Key) เป็นกุญแจในการไข

### ✨ ฟีเจอร์หลัก
- **รองรับ 2 ภาษา:** เลือกไทยหรืออังกฤษได้ตอนเริ่มเกม
- **เข้ารหัสและถอดรหัส:** ซ่อนหรือเปิดเผยข้อความได้ง่ายๆ
- **รักษาตัวพิมพ์เล็ก-ใหญ่ (Case-Sensitive):** ตัวพิมพ์ใหญ่ยังคงเป็นตัวพิมพ์ใหญ่ (เช่น พิมพ์ `W` ใส่ Key 6 จะได้ `C` ตัวใหญ่)
- **ปลอดภัยต่อรูปแบบข้อความ:** เปลี่ยนเฉพาะตัวอักษรภาษาอังกฤษ (A-Z, a-z) ส่วนตัวเลข ช่องว่าง และสัญลักษณ์ต่างๆ จะคงเดิม

### 🚀 วิธีใช้งาน
1. รันโปรแกรมด้วยคำสั่ง: `python encryptor.py`
2. เลือกภาษา: พิมพ์ `t` สำหรับภาษาไทย หรือ `e` สำหรับภาษาอังกฤษ
3. เลือกเมนูที่ต้องการ:
   - พิมพ์ `1` เพื่อ **เข้ารหัส** (ซ่อนข้อความ)
   - พิมพ์ `2` เพื่อ **ถอดรหัส** (เปิดเผยข้อความ)
   - พิมพ์ `3` เพื่อ **ออกจากโปรแกรม**
4. พิมพ์ข้อความที่ต้องการ (เช่น `Hello World`)
5. ใส่รหัสลับ (Key) เป็นตัวเลข (เช่น `3`)
6. โปรแกรมจะแสดงผลลัพธ์ที่เข้ารหัสหรือถอดรหัสให้คุณดู
