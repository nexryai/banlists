import re
import requests

my_ip = "0.0.0.0"
ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"


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

# 重複を削除
__block_ips = block_tor()
__block_ips += block_public_proxy()

block_ips = list(set(__block_ips))

print("✨ Done!!")
print(f"Total 🤭 IPs: {len(block_ips)}")

with open("nginx.conf", "w") as f:
    for ip in block_ips:
        f.write(f"deny {ip};\n")

    f.write("# Add other directives here as necessary\n")