# sound_recognition_control

Masuk ke folder sound_recognition_control
```bash
cd sound_recognition_control
```

Pastikan Virtual Enviroment sudah digunakan
```bash
source venv/bin/activate
```

## Otomatis Menerima SSH Fingerprint (Pertama kali SSH)

Buat file txt berisi ip,password. seperti file example_ip.txt
```bash
cat example_ip.txt
```

Ubah File .env
```bash
nano .env
```

Jalankan program new_host.py
```bash
python3.8 new_host.py -f [ip_file.txt]
```

## Cara menggunakan change_env.py

Buat file txt berisi ip,password. seperti file example_ip.txt
```bash
cat example_ip.txt
```

Jalankan program change_env.py
```bash
python3.8 change_env.py -f [ip_file.txt]
```
