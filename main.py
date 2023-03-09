import threading
import asyncio
import websockets
import time
import json

data_to_send = {
}

def sendData(inp):
    data_to_send = {**data_to_send, **inp}

async def socket_function():
    global data
    async with websockets.connect('wss://api.visoff.ru') as websocket:
        while True:
            await websocket.send(json.dumps(data_to_send))
            recv = await websocket.recv()
            data = json.loads(recv)
            print(data)
            await asyncio.sleep(5)
def main_socket_function():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(socket_function())
socket_thread = threading.Thread(target=main_socket_function)
socket_thread.start()
time.sleep(10)

def judge_helper_function():
    from judge_helper_bot.main import generate_judge_helper
    judge_helper_bot = generate_judge_helper()
    judge_helper_bot.infinity_polling()
judge_helper_thread = threading.Thread(target=judge_helper_function)
judge_helper_thread.start()


def telegram_function():
    global data
    from telegram.main import generate_bot
    telegram_bot = generate_bot(data, sendData)
    telegram_bot.infinity_polling()
telegram_thread = threading.Thread(target=telegram_function)
telegram_thread.start()
