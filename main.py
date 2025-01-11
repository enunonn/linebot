import asyncio
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
import dotenv
import os
from google import genai
from google.genai import types

from linebot.v3.webhook import WebhookParser, WebhookHandler
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

dotenv.load_dotenv()


LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

client = genai.Client(api_key='GEMINI_API_KEY')



app = FastAPI()


parser = WebhookParser(LINE_CHANNEL_SECRET)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.post("/callback")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        await app.line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

    return 'OK'

@app.get("/")
async def read_root():
    return {"Hello": "World"}

async def get_gemini_response():
    response = await client.aio.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents='high',
        config=types.GenerateContentConfig(
            temperature=1.0,
            top_p=0.95,
            top_k=20,
            candidate_count=1,
            max_output_tokens=100,
            stop_sequences=["STOP!"],
            presence_penalty=0.0,
            frequency_penalty=0.0,
        )
    )
    return response.result

@app.post("/webhook")
async def webhook(request: Request):
    # Your webhook handling code here
    pass


async def main():
    with app:
        app.configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
        app.async_api_client = AsyncApiClient(app.configuration)
        app.line_bot_api = AsyncMessagingApi(app.async_api_client)
    # Your other async code here

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)