from fastapi import FastAPI
import uvicorn
import os
import subprocess
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pm2/start")
def start_pm2():
    os.system("pm2 start sound-recognition")
    
    jlist = subprocess.check_output(['pm2', 'jlist'])
    jlist = json.loads(jlist)

    for i in jlist:
        if i.get('name') == 'sound-recognition':
            status = i
            break

    return {
        "status": status.get('pm2_env').get('status')
    }

@app.get("/pm2/stop")
def stop_pm2():
    os.system("pm2 stop sound-recognition")
    
    jlist = subprocess.check_output(['pm2', 'jlist'])
    jlist = json.loads(jlist)

    for i in jlist:
        if i.get('name') == 'sound-recognition':
            status = i
            break

    return {
        "status": status.get('pm2_env').get('status')
    }

@app.get("/pm2/status")
def status_pm2():
    jlist = subprocess.check_output(['pm2', 'jlist'])
    jlist = json.loads(jlist)

    for i in jlist:
        if i.get('name') == 'sound-recognition':
            status = i
            break

    return {
        "status": status.get('pm2_env').get('status'),
        "detail": status
    }

@app.get("/pm2/logs")
def logs_pm2(desc='true', limit=15):
    with open('/home/app/.pm2/logs/sound-recognition-out.log', 'r', encoding='utf-8') as logs_file:
        logs = logs_file.read().splitlines()

    logs = logs[::-1] if desc=='true' else logs

    return logs[:int(limit)]

@app.get("/env")
def get_env():
    with open('/home/app/sound_recognition/.env', 'r', encoding='utf-8') as env_file:
        env = env_file.read().splitlines()

    env_dict = dict()
    for line in env:
        keys, value = line.split('=')
        env_dict[keys] = value
    
    return env_dict

@app.put("/env")
def put_env(env:dict):
    text = str()

    for key, value in zip(env.keys(), env.values()):
        text = text + f'{key}={value}\n'

    with open('/home/app/sound_recognition/.env', 'w', encoding='utf-8') as env_file:
        env_file.write(text)

    return {
        'status': 'success',
        'env': env
    }

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=9001)