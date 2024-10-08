import os
import time
import datetime as dt
import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import motor.motor_asyncio

def get_connection():
  '''
  You need to re-establish the connection
  each time, here's an example:
  https://github.com/mongodb-developer/vercel-mongodb-next-fastapi-starter/blob/main/api/index.py#L67
  '''
  client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['uri'])
  events = client.get_database('events')

  return events

def get_local_time():
  utc_time = dt.datetime.now(pytz.utc)
  central_time = utc_time.astimezone(pytz.timezone('America/Chicago'))
  return central_time.strftime('%m/%d/%Y %I:%M %p')

app = FastAPI()

origins = [
  '*',
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

@app.get('/')
def hello_world():
  return 'Hello, world!'

@app.post('/upvote/')
async def create_upvote():

  votes = get_connection().get_collection('votes')

  vote = {
    'type': 'up',
    'created_utc': int(time.time()),
    'local_time': get_local_time()
  }

  _ = await votes.insert_one(vote)

  return {'message': 'Upvote successfully submitted.'}

@app.get('/passcode/')
async def check_passcode(passcode: str):
  return {'valid': passcode in [
    'cat'
  ]}

if __name__ == '__main__':
  uvicorn.run(app)

