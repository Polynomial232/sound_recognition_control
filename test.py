import requests

with open('ip.txt', 'r', encoding='utf-8') as ip_file:
    ips = ip_file.read().splitlines()

for ip in ips:
    result = requests.post(f'http://{ip}/git/update')
    print(result.json())