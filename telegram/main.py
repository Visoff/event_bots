import telebot

def generate_bot(data, sendData):
    token = "5255432703:AAHr8pBOON_KUih3uC1lTHczGTdkUypYvMo"
    bot = telebot.TeleBot(token=token)

    @bot.message_handler(content_types="text")
    def q(message):
        sendData({"text":message.text})
        print(message.chat.id)
        bot.send_message(message.chat.id, data)
    
    print("bot is ready to work!")
    return bot

if (__name__ == "__main__"):
    bot = generate_bot()
    bot.infinity_polling()