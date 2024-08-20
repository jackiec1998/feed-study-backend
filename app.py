import os
import time
import datetime as dt
import pytz
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import motor.motor_asyncio

def get_local_time():
  utc_time = dt.datetime.now(pytz.utc)
  central_time = utc_time.astimezone(pytz.timezone('America/Chicago'))
  return central_time.strftime('%m/%d/%Y %I:%M %p')

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['uri'])
database = client.events
votes = database.get_collection('votes')

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

  vote = {
    'type': 'up',
    'created_utc': int(time.time()),
    'local_time': get_local_time()
  }

  await votes.insert_one(vote)

  return {'message': 'Upvote successfully submitted.'}

if __name__ == '__main__':
  uvicorn.run(app)

