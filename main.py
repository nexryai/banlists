import re
import requests


my_ip = "0.0.0.0"
ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"


def block_bulletproof() -> list:
    __ip_list = []
    block_asn = ["397702", "398088", "53667", "8473", "17318", "7941", "211298", "209366", "37963", "40065", "57523", "34665", "57509", "397702", "398088", "53667"]

    # IPv4
    for asn in block_asn:
        response = requests.get(f"https://raw.githubusercontent.com/ipverse/asn-ip/master/as/{asn}/ipv4-aggregated.txt")

        if response.status_code == 200:
            for line in response.text.splitlines():
                if not "#" in line:
                    print(f"👎 Block bulletproof🤣 hosting (AS{asn}) IPs: {line}")
                    __ip_list.append(line)

    # IPv6
    for asn in block_asn:
        response = requests.get(f"https://raw.githubusercontent.com/ipverse/asn-ip/master/as/{asn}/ipv6-aggregated.txt")

        if response.status_code == 200:
            for line in response.text.splitlines():
                if not "#" in line and line != "":
                    print(f"👎 Block bulletproof🤣 hosting (AS{asn}) IPs: {line}")
                    __ip_list.append(line)

    return __ip_list


def block_tor() -> list:
    __ip_list = []

    response = requests.get("https://check.torproject.org/torbulkexitlist?ip=1.1.1.1")
    for line in response.text.splitlines():
        print(f"🧅 Block tor IP: {line}")
        __ip_list.append(line)

    return __ip_list


def block_public_proxy() -> list:
    # JSONファイルをダウンロードする
    json_url = "https://raw.githubusercontent.com/MatrixTM/MHDDoS/main/config.json"
    response = requests.get(json_url)
    data = response.json()

    # IPアドレスのリストを作成する
    ip_list = []
    for provider in data["proxy-providers"]:
        url = provider["url"]
        timeout = provider["timeout"]

        try:
            if "http://rootjazz.com" in url:
                raise Exception("Blocked URL")

            response = requests.get(url, timeout=timeout)

            for line in response.text.splitlines():
                __ip_list = re.findall(ipv4_pattern, line)

                if my_ip in __ip_list:
                    print(f"My ip in {url} !!!!!")
                else:
                    print(f"🤬 Block public proxy IP: (source:{url}) {__ip_list}")
                    ip_list += __ip_list

        except Exception as e:
            print(f"Exception: {e}")

    return ip_list


with open("block-public-proxy.conf", "w") as f:
    for ip in list(set(block_public_proxy())):
        f.write(f"deny {ip};\n")

with open("block-bulletproof.conf", "w") as f:
    for ip in list(set(block_bulletproof())):
        f.write(f"deny {ip};\n")

with open("public-proxy.ipset", "w") as f:
    for ip in list(set(block_public_proxy())):
        f.write(f"{ip}\n")

with open("bulletproof.ipset", "w") as f:
    for ip in list(set(block_bulletproof())):
        f.write(f"{ip}\n")

print("✨ Done!!")
