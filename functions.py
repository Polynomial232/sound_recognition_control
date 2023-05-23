import subprocess
import json

def get_pm2_status(name):
    jlist = subprocess.check_output(['pm2', 'jlist'])
    jlist = json.loads(jlist)

    for i in jlist:
        if i.get('name') == name:
            status = i
            break

    return status
