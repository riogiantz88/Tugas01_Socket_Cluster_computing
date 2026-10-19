import socket
import sys
import time

def run_worker(port, worker_id):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', port))
    server.listen(5)
    print(f"[Worker {worker_id}] Siap berjalan di port {port}...")

    while True:
        client_sock, addr = server.accept()
        data = client_sock.recv(1024).decode('utf-8')
        if not data:
            break
        
        app_id, payload = data.split(":", 1)
        print(f"[Worker {worker_id}] Menerima Request - App ID: {app_id}, Payload: {payload}")

        # Simulasi jenis aplikasi (Long vs Short)[span_11](start_span)[span_11](end_span)
        if app_id == "1":
            print(f"[Worker {worker_id}] Memproses komputasi kompleks (Long)...")
            time.sleep(3) # Simulasi proses lama
            response = f"Worker {worker_id} (Long Task Selesai): Hasil dari {payload}"
        else:
            print(f"[Worker {worker_id}] Memproses task ringan (Short/Echo)...")
            response = f"Worker {worker_id} (Short Task Selesai): {payload}"

        client_sock.sendall(response.encode('utf-8'))
        client_sock.close()

if __name__ == "__main__":
    port_arg = int(sys.argv[1])
    id_arg = sys.argv[2]
    run_worker(port_arg, id_arg)
