'''
stub для запуска админки. 
uvicorn app.main:app --reload
bot пока запускается через
python bot.py
'''
from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def read_root():
    return {'Hello': 'FastAPI'}
