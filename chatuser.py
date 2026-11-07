import socket

def main():
    # ถ้าทดสอบในเครื่องเดียวกัน ให้ใช้ 127.0.0.1
    # ถ้าทดสอบคนละเครื่อง ให้เปลี่ยนเป็น IP ของเครื่องที่รัน Server
    SERVER_IP = '127.0.0.1' 
    PORT = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Connecting to {SERVER_IP}:{PORT}...")
        client_socket.connect((SERVER_IP, PORT))
        print("✅ Connected to Server! Type 'exit' to quit.\n")

        while True:
            # ส่งข้อความไปให้ Server
            msg = input("💬 You: ")
            client_socket.send(msg.encode('utf-8'))
            if msg.lower() == 'exit':
                break
            
            # รับข้อความตอบกลับ
            reply = client_socket.recv(1024).decode('utf-8')
            if not reply or reply.lower() == 'exit':
                print("\nServer has disconnected.")
                break
            print(f"👤 Friend: {reply}")

    except ConnectionRefusedError:
        print("❌ Error: Could not connect. Is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client_socket.close()
        print("Chat closed.")

if __name__ == "__main__":
    main()

