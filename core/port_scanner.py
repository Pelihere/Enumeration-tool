import socket
from concurrent.futures import ThreadPoolExecutor
import threading

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.lock = threading.Lock()

    def scan_port(self, port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            try:
                result = sock.connect_ex((self.target, port))

                if result == 0:
                    print(f"FOUND {port}")
                    with self.lock:
                        self.open_ports.append(port)

            except Exception as e:
                print(port, e)

            finally:
                sock.close()


    def scan(self, start_port=1, end_port=65535):
        print(f"\n[#] Scanning Target: {self.target} from port {start_port} to {end_port}")

        self.open_ports.clear()

        with ThreadPoolExecutor(max_workers=100) as executor:
            list(executor.map(self.scan_port, range(start_port, end_port + 1)))

        return sorted(self.open_ports)