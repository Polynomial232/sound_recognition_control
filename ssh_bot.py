from paramiko import SSHClient
from paramiko_expect import SSHClientInteraction

# with open('ip.txt', 'r', encoding='utf-8') as ip_file:
with open('ip_notes/all_ip.txt', 'r', encoding='utf-8') as ip_file:
    ip_server = ip_file.read().splitlines()

def main(ip, password):
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ip, username='app', password=password, timeout=30)

    interact = SSHClientInteraction(client, timeout=10, display=True)

    stdin, stdout, stderr = client.exec_command('cd /home/app/sound_recognition/ && git reset --hard HEAD && git pull')
    
    print('='*100)

    interact.send('pm2 restart sound-recognition')
    interact.send('exit')
    interact.expect()

    print(f'[{ip}]\tSTDOUT: {stdout.read().decode("utf8")}')

    # Because they are file objects, they need to be closed
    stdin.close()
    stdout.close()
    stderr.close()

    # Close the client itself
    client.close()

for i in ip_server:
    try:
        ip, password = i.split(',')

        # Connect
        main(ip, password)
    except:
        with open('error.txt', 'a', encoding='utf-8') as file:
            file.write(f'{ip}\n')
        pass
