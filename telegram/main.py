import telebot

def generate_bot(data, sendData):
    token = "5255432703:AAHr8pBOON_KUih3uC1lTHczGTdkUypYvMo"
    bot = telebot.TeleBot(token=token)

    @bot.message_handler(commands=["send"])
    def q(message):
        if (message.reply_to_message):
            print(message.reply_to_message.text)
        else:
            sendData({"text":message.text})
            bot.send_message(message.chat.id, "sent")
    
    print("bot is ready to work!")
    return bot

if (__name__ == "__main__"):
    bot = generate_bot()
    bot.infinity_polling()