import socket
import datetime
import os
import traceback
import threading

HOST = "0.0.0.0"   
PORT = 2222       

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "Logs\honeypot_log.txt")


def log_event(message):
    """Append a timestamped line to the log file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.datetime.now()} - {message}\n")


def recv_line(conn, max_len=100):
    """
    Receive a line of text (until \n or \r or max_len).
    Returns a decoded string (without newline).
    """
    data = b""
    try:
        while len(data) < max_len:
            chunk = conn.recv(1)
            if not chunk:
                break
            if chunk in (b"\n", b"\r"):
                break
            data += chunk
    except Exception:
        pass
    return data.decode(errors="ignore").strip()


def handle_client(conn, addr):
    """Handle one attacker connection in a thread."""
    attacker_ip, attacker_port = addr
    print(f"[!] Connection from: {attacker_ip}:{attacker_port}")
    log_event(f"Connection from {attacker_ip}:{attacker_port}")

    try:
        
        conn.sendall(b"SSH-2.0-OpenSSH_7.9p1 Debian-10\r\n")

        
        conn.sendall(b"login: ")
        username = recv_line(conn)

        
        conn.sendall(b"Password: ")
        password = recv_line(conn)

        
        log_event(
            f"Credentials attempt from {attacker_ip}:{attacker_port} "
            f"username='{username}' password='{password}'"
        )
        print(f"[+] Captured credentials from {attacker_ip}: {username} / {password}")

    
        conn.sendall(b"Access denied\r\n")
        conn.sendall(b"Permission denied, please try again.\r\n")

    except Exception as e:
        print(f"[!] Error handling client {attacker_ip}: {e}")
        log_event(f"Error handling client {attacker_ip}: {e}")
        log_event(traceback.format_exc())
    finally:
        conn.close()


def main():
    print(f"[+] Advanced honeypot starting on port {PORT}...")
    print(f"[+] Script directory: {SCRIPT_DIR}")
    print(f"[+] Log file path: {LOG_FILE}")

    
    log_event("Advanced honeypot started")

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(10)  
        print(f"[+] Listening on {HOST}:{PORT}")
    except Exception as e:
        print("[!] Failed to bind/listen:", e)
        log_event("FATAL error in bind/listen: " + str(e))
        log_event(traceback.format_exc())
        input("Press Enter to exit...")
        return

    
    while True:
        try:
            conn, addr = server.accept()
        except Exception as e:
            print("[!] Error on accept():", e)
            log_event("Error on accept: " + str(e))
            log_event(traceback.format_exc())
            continue

        
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    main()
