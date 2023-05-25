from paramiko import SSHClient
from paramiko_expect import SSHClientInteraction
import threading
import time

with open('ip.txt', 'r', encoding='utf-8') as ip_file:
    ip_server = ip_file.read().splitlines()

def main(ip, password):
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ip, username='app', password=password)

    interact = SSHClientInteraction(client, timeout=10, display=True)

    _ = client.exec_command('cd /home/app/sound_recognition/ && git reset --hard HEAD')
    stdin, stdout, stderr = client.exec_command('cd /home/app/sound_recognition/ && git pull')
    
    # print('='*100)
    # print(f'[{ip}]\tSTDOUT: {stdout.read().decode("utf8")}')
    # print('='*100)

    # interact.send('pm2 restart all')
    # interact.send('exit')
    # interact.expect()

    # cmd_output = interact.current_output_clean
    # print(cmd_output)

    # Because they are file objects, they need to be closed
    stdin.close()
    stdout.close()
    stderr.close()

    # Close the client itself
    client.close()

    print(f'[{ip}] Done')

thread_list = []
results = []

for i in ip_server:
    ip, password = i.split(',')
    thread = threading.Thread(target=main, args=(ip, password))
    thread_list.append(thread)


for thread in thread_list:
    try:
        thread.start()
    except:
        with open('error.txt', 'a', encoding='utf-8') as file:
            file.write(f'{ip}\n')
        pass

strt = time.perf_counter()

for thread in thread_list:
    thread.join()

print(f'time: {round(time.perf_counter() - strt, 3)}s')