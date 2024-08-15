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
    "http://localhost:5173",  # React app URL during development
    "https://jackiec1998.github.io/",  # Replace with your frontend's production URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def hello_world():
  return 'Hello, world!'

@app.post('/upvote/')
async def create_upvote():
  _ = await votes.insert_one({
    'type': 'up',
    'created_utc': int(time.time())
  })

if __name__ == '__main__':
  uvicorn.run(app)

