import telebot

def generate_bot(data, sendData):
    token = "5255432703:AAHr8pBOON_KUih3uC1lTHczGTdkUypYvMo"
    bot = telebot.TeleBot(token=token)

    @bot.message_handler(commands=["send"])
    def q(message):
        if (message.reply_to_message):
            sendData({"text":message.reply_to_message.text})
            bot.send_message(message.chat.id, "sent\n\n"+message.reply_to_message.text)
    
    print("bot is ready to work!")
    return bot

if (__name__ == "__main__"):
    bot = generate_bot()
    bot.infinity_polling()