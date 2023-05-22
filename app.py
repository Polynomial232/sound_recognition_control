from fastapi import FastAPI, HTTPException, status
import uvicorn
import os
from functions import get_pm2_status
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/pm2/{command}")
def start_pm2(command):
    try:
        os.system(f"pm2 {command} sound-recognition")
        status_pm2 = get_pm2_status()

        return {
            "status": status_pm2.get('pm2_env').get('status')
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='failed'
        )

@app.get("/pm2/status")
def get_status_pm2():
    status = get_pm2_status()

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

@app.post("/git/update")
def git_update():
    update_output = subprocess.check_output(['git','pull'], cwd='/home/app/sound_recognition')

    return update_output.splitlines()

if __name__=='__main__':
    uvicorn.run(app, host='0.0.0.0', port=9001)