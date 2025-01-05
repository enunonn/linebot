from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import requests
import dotenv
import os

dotenv.load_dotenv()
app = FastAPI()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'

def send_line_message(to, messages):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    data = {
        'to': to,
        'messages': messages
    }
    response = requests.post(LINE_API_URL, headers=headers, json=data)
    return response.status_code, response.json()

class LineMessage(BaseModel):
    events: list

@app.post("/webhook")
async def webhook(request: Request, line_message: LineMessage):
    for event in line_message.events:
        # Process the event here
        print(event)
        # 예시: 메시지 보내기
        user_id = event['source']['userId']
        message = [{
            'type': 'text',
            'text': 'Hello from FastAPI!'
        }]
        status_code, response = send_line_message(user_id, message)
        print(f'Status: {status_code}, Response: {response}')
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)