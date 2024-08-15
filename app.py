import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['uri'])
database = client.events
votes = database.get_collection('votes')

origins = [
    'http://localhost:5173',  # Development
    'http://localhost:5173/feed-study/feed',
    'https://jackiec1998.github.io',  # Production
    'https://jackiec1998.github.io/feed-study/feed',
    'https://feed-study-backend.vercel.app'
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
    'created_utc': int(time.time())
  }

  _ = await votes.insert_one(vote)

  return vote

if __name__ == '__main__':
  uvicorn.run(app)

