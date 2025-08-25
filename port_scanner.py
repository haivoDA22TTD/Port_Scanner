import os
import shutil
import socket
import threading

PURPLE = "\033[95m"
RESET = "\033[0m"

ASCII_LOGO = """
  ____                                        _             
 / ___|___  _ __ ___  _ __   __ _ _ __   ___| |_ ___  _ __ 
| |   / _ \| '_ ` _ \| '_ \ / _` | '_ \ / _ \ __/ _ \| '__|
| |__| (_) | | | | | | |_) | (_| | | | |  __/ || (_) | |   
 \____\___/|_| |_| |_| .__/ \__,_|_| |_|\___|\__\___/|_|   
                     |_|                                    
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text, color=PURPLE):
    columns, lines = shutil.get_terminal_size()
    text_lines = text.strip('\n').splitlines()
    start_line = (lines // 2) - (len(text_lines) // 2) - 3

    print("\n" * max(start_line, 0), end="")

    for line in text_lines:
        padding = (columns - len(line)) // 2
        print(" " * padding + color + line + RESET)

def main():
    clear_screen()
    print_centered(ASCII_LOGO)
    print("\n")

    ip = input("Nhập địa chỉ IP: ").strip()
    try:
        socket.inet_aton(ip)
    except socket.error:
        print("[!] Địa chỉ IP không hợp lệ.")
        return

    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 8080]

    print(f"\nĐang quét các port phổ biến trên {ip}...\n")

    threads = []
    def scan_port(ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)
                result = s.connect_ex((ip, port))
                if result == 0:
                    print(f"[+] Port {port} đang mở")
        except:
            pass

    for port in ports:
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n✅ Quét hoàn tất.")

if __name__ == "__main__":
    main()
