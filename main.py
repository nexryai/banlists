import re
import requests


my_ip = "0.0.0.0"
ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"


def get_ipset(url):
    __ip_list = []
    response = requests.get(url)
    if response.status_code == 200:
        for line in response.text.splitlines():
            if not "#" in line:
                __ip_list.append(line)

    return __ip_list


def block_bulletproof() -> list:
    __ip_list = []
    block_asn = ["397702", "398088", "53667", "8473", "17318", "7941", "211298", "209366", "37963", "40065", "57523", "34665", "57509", "397702", "398088", "53667"]

    # IPv4
    for asn in block_asn:
        __ip_list.extend(get_ipset(f"https://raw.githubusercontent.com/ipverse/asn-ip/master/as/{asn}/ipv4-aggregated.txt"))

    # IPv6
    for asn in block_asn:
        __ip_list.extend(get_ipset(f"https://raw.githubusercontent.com/ipverse/asn-ip/master/as/{asn}/ipv6-aggregated.txt"))

    return __ip_list


def block_tor() -> list:
    __ip_list = []

    response = requests.get("https://check.torproject.org/torbulkexitlist?ip=1.1.1.1")
    for line in response.text.splitlines():
        print(f"🧅 Block tor IP: {line}")
        __ip_list.append(line)

    return __ip_list


def block_public_proxy() -> list:
    ip_list = []
    ip_list.extend(get_ipset("https://iplists.firehol.org/files/firehol_proxies.netset"))
    ip_list.extend(get_ipset("https://iplists.firehol.org/files/sslproxies_30d.ipset"))
    ip_list.extend(get_ipset("https://iplists.firehol.org/files/socks_proxy_30d.ipset"))

    return ip_list


def block_abuse_ip() -> list:
    ip_list = []
    ip_list.extend(get_ipset("https://iplists.firehol.org/files/firehol_abusers_30d.netset"))
    ip_list.extend(get_ipset("https://iplists.firehol.org/files/botscout_30d.ipset"))
    ip_list.extend(get_ipset("https://iplists.firehol.org/files/bruteforceblocker.ipset"))
    ip_list.extend(get_ipset("https://iplists.firehol.org/files/blocklist_de.ipset"))
    ip_list.extend(get_ipset("https://raw.githubusercontent.com/LittleJake/ip-blacklist/main/ustc_blacklist_ip.txt"))
    ip_list.extend(get_ipset("https://raw.githubusercontent.com/LittleJake/ip-blacklist/main/abuseipdb_blacklist_ip_score_75.txt"))

    return ip_list


public_proxy_ips = list(set(block_public_proxy()))
bulletproof_ips = list(set(block_bulletproof()))
abuse_ips = list(set(block_abuse_ip()))

with open("block-public-proxy.conf", "w") as f:
    for ip in public_proxy_ips:
        f.write(f"deny {ip};\n")

with open("block-bulletproof.conf", "w") as f:
    for ip in bulletproof_ips:
        f.write(f"deny {ip};\n")

with open("block-abuseip.conf", "w") as f:
    for ip in abuse_ips:
        f.write(f"deny {ip};\n")

with open("public-proxy.ipset", "w") as f:
    for ip in public_proxy_ips:
        f.write(f"{ip}\n")

with open("bulletproof.ipset", "w") as f:
    for ip in bulletproof_ips:
        f.write(f"{ip}\n")

with open("abuse.ipset", "w") as f:
    for ip in abuse_ips:
        f.write(f"{ip}\n")

print("✨ Done!!")
