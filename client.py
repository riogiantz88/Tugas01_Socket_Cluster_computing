import socket

def send_request(app_id, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8000)) # Kirim ke Broker
    
    payload = f"{app_id}:{message}"
    client.sendall(payload.encode('utf-8'))

    response = client.recv(1024).decode('utf-8')
    print(f"[Client] Respon dari Server: {response}")
    client.close()

if __name__ == "__main__":
    # Contoh mengirim request aplikasi jenis 1 (Long) dan jenis 2 (Short)
    send_request("1", "Matriks 100x100")
    send_request("2", "Pesan Echo")
