import subprocess
import json

def get_pm2_status():
    jlist = subprocess.check_output(['pm2', 'jlist'])
    jlist = json.loads(jlist)

    for i in jlist:
        if i.get('name') == 'sound-recognition':
            status = i
            break

    return status
