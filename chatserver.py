import socket

def main():
    HOST = '0.0.0.0' # รับการเชื่อมต่อจากทุก IP
    PORT = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ป้องกัน Error เวลารันซ้ำๆ
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print("========================================")
        print("   📡 CHAT SERVER IS RUNNING (Port: 9999) ")
        print("========================================")
        print("Waiting for a client to connect...\n")

        conn, addr = server_socket.accept()
        print(f"✅ Connected by: {addr}\n")

        while True:
            # รับข้อความจาก Client
            data = conn.recv(1024).decode('utf-8')
            if not data or data.lower() == 'exit':
                print("\nClient has disconnected.")
                break
            
            print(f"👤 Friend: {data}")
            
            # ส่งข้อความกลับ
            reply = input("💬 You: ")
            conn.send(reply.encode('utf-8'))
            if reply.lower() == 'exit':
                break

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    main()

