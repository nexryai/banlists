import re
import requests

# JSONファイルをダウンロードする
my_ip="39.110.162.11"
json_url = "https://raw.githubusercontent.com/MatrixTM/MHDDoS/main/config.json"
response = requests.get(json_url)
data = response.json()
ipv4_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

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
                print(f"{url}: {__ip_list}")
                ip_list += __ip_list

    except Exception as e:
         print(f"Exception: {e}")

# 重複を削除
ip_list = list(set(ip_list))
print(len(ip_list))

with open("nginx.conf", "w") as f:
    for ip in ip_list:
        f.write(f"deny {ip};\n")

    f.write("# Add other directives here as necessary\n")