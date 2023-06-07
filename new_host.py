import os
import argparse

def main(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        all_ip = f.read().splitlines()

    for i in all_ip:
        ip = i.split(',')[0]
        os.system(f'ssh-keyscan -H {ip} >> ~/.ssh/known_hosts')

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--ip_file', required=True, help="File berisi IP yang ingin diubah")
    args = parser.parse_args()

    main(args.ip_file)