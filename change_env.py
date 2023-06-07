from paramiko import SSHClient
from paramiko_expect import SSHClientInteraction
import argparse

with open('.env', 'r', encoding='utf-8') as env_file:
    NEW_ENV = env_file.read().splitlines()

def change_env(ip, password):
    """
        Melakukan SSH ke server dan mengganti file .env pada folder sound_recognition
    """

    # ssh ke server
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(ip, username='app', password=password, timeout=10)

    interact = SSHClientInteraction(client, timeout=10, display=True)
    
    _, stdout_git, _ = client.exec_command('cd /home/app/sound_recognition/ && git reset --hard HEAD && git pull')

    # membaca file .env lama
    stdin, stdout, stderr = client.exec_command('cd /home/app/sound_recognition/ && cat .env')
    
    # mengubah file .env lama menjadi file .env baru disimpan di lokal
    env_arr = stdout.read().decode("utf8").splitlines()
    for i, _ in enumerate(env_arr):
        if i == 0:
            continue
        env_arr[i] = NEW_ENV[i]
    
    stdin, stdout, stderr = client.exec_command('cd /home/app/sound_recognition/ && mv .env .env.save')

    # mengubah menjadi file .env baru di server
    for text in env_arr:
        _ = client.exec_command(f'cd /home/app/sound_recognition/ && echo {text} >> .env')

    # membaca file .env baru
    stdin, stdout, stderr = client.exec_command('cd /home/app/sound_recognition/ && cat .env')

    # melakukan restart pm2 pada program sound-recognition
    interact.send('pm2 restart sound-recognition')
    interact.send('exit')
    interact.expect()
    print()
    print("="*100)
    print("git pull update")
    print("\n", stdout_git.read().decode("utf8"))
    print("\nFile .env: ")

    # output file .env baru
    print(stdout.read().decode("utf8"))


    # Close Objects
    stdin.close()
    stdout.close()
    stderr.close()

    # Close Client
    client.close()

def main(file_path):

    with open(file_path, 'r', encoding='utf-8') as ip_file:
        ip_server = ip_file.read().splitlines()

    for i in ip_server:
        try:
            ip, password = i.split(',')
            change_env(ip, password)
        except Exception as e:
            print(e)
            with open('error.txt', 'a', encoding='utf-8') as file:
                file.write(f'{ip}\n')
            pass

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--ip_file', required=True, help="File berisi IP yang ingin diubah")
    args = parser.parse_args()

    main(args.ip_file)