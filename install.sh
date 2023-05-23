python3.8 -m venv venv
source venv/bin/activate
pip install -r requiremets.txt
pm2 start app --interpreter venv/bin/python3.8 --name sound-recognition-control