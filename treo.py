import os
import ssl
import json
import time
import threading
from queue import Queue, Empty, Full
import secrets
import random
import base64
import requests
from dataclasses import dataclass, field
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
from colorama import Fore, Style
import asyncio
import aiohttp
import concurrent.futures
from requests_futures.sessions import FuturesSession
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import httpx
import base64
import hashlib
from bs4 import BeautifulSoup
import sys

MAX_RETRIES = 3
MAX_MSG_BEFORE_CLEAR = 80
MAX_QUEUE_SIZE = 15
SMART_RETRY = 2
REQUEST_TIMEOUT = 12
MAX_WORKERS = 3
CONNECTION_POOL_SIZE = 10
BATCH_SIZE = 20

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.141 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
]

def banner():
    print(Fore.CYAN + r"""
██▓    ▓█████     ██ ▄█▀ ██░ ██  ▄▄▄       ███▄    █  ██░ ██     ▄▄▄█████▓ █    ██ 
▓██▒    ▓█   ▀     ██▄█▒ ▓██░ ██▒▒████▄     ██ ▀█   █ ▓██░ ██▒    ▓  ██▒ ▓▒ ██  ▓██▒
▒██░    ▒███      ▓███▄░ ▒██▀▀██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██▀▀██░    ▒ ▓██░ ▒░▓██  ▒██░
▒██░    ▒▓█  ▄    ▓██ █▄ ░▓█ ░██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█ ░██     ░ ▓██▓ ░ ▓▓█  ░██░
░██████▒░▒████▒   ▒██▒ █▄░▓█▒░██▓ ▓█   ▓██▒▒██░   ▓██░░▓█▒░██▓      ▒██▒ ░ ▒▒█████▓ 
░ ▒░▓  ░░░ ▒░ ░   ▒ ▒▒ ▓▒ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒ ░░▒░▒      ▒ ░░   ░▒▓▒ ▒ ▒ 
░ ░ ▒  ░ ░ ░  ░   ░ ░▒ ▒░ ▒ ░▒░ ░  ▒   ▒▒ ░░ ░░   ░ ▒░ ▒ ░▒░ ░        ░    ░░▒░ ░ ░ 
  ░ ░      ░      ░ ░░ ░  ░  ░░ ░  ░   ▒      ░   ░ ░  ░  ░░ ░      ░       ░░░ ░ ░ 
    ░  ░   ░  ░   ░  ░    ░  ░  ░      ░  ░         ░  ░  ░  ░                ░
                                   Author : Le Khanh Tu
    """ + Style.RESET_ALL)
    print()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def init_msg():
    print(Fore.BLUE + 'ĐANG TẢI TOOL ĐA TOKEN.......' + Style.RESET_ALL)
    print()

def check_token(token):
    if not token or len(token.strip()) < 200:
        return False

    headers = {
        "Authorization": token.strip(),
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers=headers,
            timeout=12,
            verify=False
        )

        if response.status_code == 200:
            try:
                data = response.json()
                return 'id' in data and 'username' in data
            except:
                return False
        elif response.status_code == 401:
            return False
        elif response.status_code == 403:
            return True
        elif response.status_code == 429:
            time.sleep(1)
            try:
                retry_response = requests.get(
                    "https://discord.com/api/v10/users/@me",
                    headers=headers,
                    timeout=12,
                    verify=False
                )
                return retry_response.status_code in [200, 403]
            except:
                return False
        else:
            return False

    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return False

def _kiemtratoken_(tokens):
    valid_tokens = []
    print(f"{Fore.YELLOW}Đang kiểm tra {len(tokens)} token...{Style.RESET_ALL}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_token = {executor.submit(check_token, token): token for token in tokens}
        for future in concurrent.futures.as_completed(future_to_token):
            token = future_to_token[future]
            try:
                if future.result():
                    valid_tokens.append(token)
            except:
                pass

    print(f"{Fore.GREEN}Token hợp lệ: {len(valid_tokens)}/{len(tokens)}{Style.RESET_ALL}")
    return valid_tokens

class _money_:
    def __init__(self, files):
        self.messages = []
        self.load_messages(files)

    def load_messages(self, files):
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        self.messages.append(content)

    def lktcute(self):
        if not self.messages:
            return "Default message"
        return random.choice(self.messages)

def _get_kenh_(channel_id, token):
    headers = {
        "Authorization": token,
        "User-Agent": random.choice(USER_AGENTS)
    }
    try:
        response = requests.get(f"https://discord.com/api/v10/channels/{channel_id}", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('name', 'Unknown')
        return 'Unknown'
    except:
        return 'Unknown'

class _money_:
    def __init__(self, message_cache, channels, tokens):
        self.message_cache = message_cache
        self.channels = channels
        self.tokens = tokens
        self.running = True
        self.batch_sessions = {}

    def _create_ss_(self, batch_tokens):
        session = FuturesSession(max_workers=len(batch_tokens))
        retry_strategy = Retry(
            total=MAX_RETRIES,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=0.5
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=CONNECTION_POOL_SIZE,
            pool_maxsize=CONNECTION_POOL_SIZE
        )
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _headers_(self, token):
        d = secrets.token_hex(16)
        s = secrets.token_hex(32)

        build_number = random.randint(240000, 250000)

        dev = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": random.choice(["en-US", "en-GB"]),
            "browser_user_agent": random.choice(USER_AGENTS),
            "browser_version": "120.0.0.0",
            "os_version": "10",
            "referrer": "https://discord.com/",
            "referring_domain": "discord.com",
            "release_channel": "stable",
            "client_build_number": build_number,
            "client_event_source": None
        }

        return {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": dev['browser_user_agent'],
            "X-Super-Properties": base64.b64encode(json.dumps(dev, separators=(',', ':')).encode()).decode(),
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me"
        }

    def _send_tin_nhan_(self, session, token, channel, message):
        nonce = str(int(time.time() * 1000) + random.randint(1000, 9999))
        data = json.dumps({
            "content": message,
            "tts": False,
            "nonce": nonce,
            "flags": 0
        })

        headers = self._headers_(token)
        url = f"https://discord.com/api/v10/channels/{channel}/messages"

        for attempt in range(SMART_RETRY):
            try:
                response = session.post(url, data=data, headers=headers, timeout=REQUEST_TIMEOUT)

                if response.status_code == 429:
                    retry_after = response.json().get('retry_after', 1.5)
                    time.sleep(retry_after)
                    continue

                if response.status_code == 401:
                    return False

                if response.status_code == 403:
                    return False

                if 200 <= response.status_code < 300:
                    return True

            except Exception as e:
                time.sleep(random.uniform(0.8, 1.2))

        return False

    def _lkt_(self, token, delay):
        session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=0.5
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        channel_index = 0

        while self.running:
            try:
                channel = self.channels[channel_index]
                message = self.message_cache.lktcute()

                self._send_tin_nhan_(session, token, channel, message)

                channel_index = (channel_index + 1) % len(self.channels)
                time.sleep(delay)

            except Exception:
                time.sleep(1.5)

        session.close()

def _thong_bao_(channels, token):
    print(f"{Fore.YELLOW}Đang spam vào {len(channels)} kênh{Style.RESET_ALL}")
    for i, channel in enumerate(channels, 1):
        channel_name = _get_kenh_(channel, token)
        print(f"{Fore.CYAN}{i} > Id:{channel} - Tên:{channel_name}{Style.RESET_ALL}")
    print()

def file_ngon():
    files = []
    print(f"{Fore.YELLOW}Nhập file tin nhắn ( 'done' để dừng):{Style.RESET_ALL}")

    while True:
        file_path = input(f"{Fore.CYAN}File: {Style.RESET_ALL}").strip()
        if file_path.lower() == 'done':
            break
        if file_path and os.path.exists(file_path):
            files.append(file_path)
        elif file_path:
            pass

    return files

def main():
    cls()
    banner()
    init_msg()

    token_file = input(f"{Fore.GREEN}Nhập file chứa token: {Style.RESET_ALL}").strip()
    if not token_file:
        print(f"{Fore.RED}Bạn chưa nhập file{Style.RESET_ALL}")
        return

    try:
        with open(token_file, 'r', encoding='utf-8') as f:
            all_tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}Không tìm thấy file '{token_file}'{Style.RESET_ALL}")
        return

    if not all_tokens:
        print(f"{Fore.RED}Không tìm thấy token nào trong {token_file}{Style.RESET_ALL}")
        return

    tokens = _kiemtratoken_(all_tokens)

    if not tokens:
        print(f"{Fore.RED}Không có token hợp lệ nào{Style.RESET_ALL}")
        return

    channels = []
    print(f"{Fore.YELLOW}Nhập ID kênh :{Style.RESET_ALL}")
    while True:
        channel = input(f"{Fore.CYAN}> ID (Enter để kết thúc): {Style.RESET_ALL}").strip()
        if not channel:
            break
        channels.append(channel)

    if not channels:
        print(f"{Fore.RED}Cần ít nhất 1 kênh để gửi tin nhắn{Style.RESET_ALL}")
        return

    message_files = file_ngon()
    if not message_files:
        print(f"{Fore.RED}Cần ít nhất 1 file tin nhắn{Style.RESET_ALL}")
        return

    message_cache = _money_(message_files)

    delays = {}
    for token in tokens:
        while True:
            try:
                delay = float(input(f"{Fore.CYAN}Delay cho token {token[-4:]} (giây): {Style.RESET_ALL}"))
                delays[token] = delay
                break
            except ValueError:
                print(f"{Fore.RED}Vui lòng nhập số hợp lệ{Style.RESET_ALL}")

    lich = _money_(message_cache, channels, tokens)

    print(f'{Fore.YELLOW}Đang khởi động...{Style.RESET_ALL}')
    time.sleep(2)
    cls()
    banner()
    init_msg()
    _thong_bao_(channels, tokens[0])

    threads = []
    for token in tokens:
        thread = threading.Thread(
            target=lich._lkt_,
            args=(token, delays[token]),
            daemon=True
        )
        threads.append(thread)
        thread.start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Đang dừng tab...{Style.RESET_ALL}")
        lich.running = False

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    main()
