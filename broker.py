import socket

# Daftar 3 Worker dalam Cluster beserta status jumlah request yang sudah dilayani
# Format: (ip, port, total_request_handled)
WORKERS = [
    {'host': 'localhost', 'port': 9001, 'id': 1, 'load': 0},
    {'host': 'localhost', 'port': 9002, 'id': 2, 'load': 0},
    {'host': 'localhost', 'port': 9003, 'id': 3, 'load': 0}
]

def get_least_loaded_worker():
    """
    Memilih worker berdasarkan pendekatan pemerataan (Least Connections/Requests),
    yaitu memilih worker dengan jumlah beban (load) paling sedikit.
    """
    # Mencari worker dengan nilai 'load' minimum
    selected_worker = min(WORKERS, key=lambda w: w['load'])
    return selected_worker

def start_broker():
    broker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    broker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broker.bind(('localhost', 8000))
    broker.listen(5)
    print("[Broker] Load Balancer (Least Requests Strategy) aktif di port 8000...")

    while True:
        client_sock, addr = broker.accept()
        data = client_sock.recv(1024)
        if not data:
            continue

        print(f"\n[Broker] Mendapatkan request dari klien {addr}")
        
        # Pilih worker dengan beban paling sedikit
        target_worker = get_least_loaded_worker()
        print(f"[Broker] Alokasi beban -> Worker {target_worker['id']} ({target_worker['host']}:{target_worker['port']}) | Beban saat ini: {target_worker['load']} request")

        # Tambahkan beban pada worker yang dipilih
        target_worker['load'] += 1

        try:
            # Teruskan request ke worker terpilih
            worker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            worker_sock.connect((target_worker['host'], target_worker['port']))
            worker_sock.sendall(data)

            # Terima balasan dari worker
            response = worker_sock.recv(1024)
            worker_sock.close()

            # Kirim balik ke klien
            client_sock.sendall(response)
        except Exception as e:
            print(f"[Broker Error] Gagal terhubung ke worker: {e}")
        finally:
            client_sock.close()

if __name__ == "__main__":
    start_broker()
