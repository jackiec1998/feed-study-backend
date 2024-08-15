import os
import time
from fastapi import FastAPI
import uvicorn
import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['uri'])
database = client.events
votes = database.get_collection('votes')

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

