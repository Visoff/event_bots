import threading
import asyncio

data = {}

def judge_helper_function():
    from judge_helper_bot.main import generate_judge_helper
    judge_helper_bot = generate_judge_helper()
    judge_helper_bot.infinity_polling()
judge_helper_thread = threading.Thread(target=judge_helper_function)
judge_helper_thread.start()


def telegram_function():
    from telegram.main import generate_bot
    telegram_bot = generate_bot()
    telegram_bot.infinity_polling()
telegram_thread = threading.Thread(target=telegram_function)
telegram_thread.start()