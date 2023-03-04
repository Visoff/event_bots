import copy
import json
import telebot
from telebot import types
from count_votes import calculate
from table import SendTable
from sheets import update_sheets
def generate_judge_helper():
    bot_token = "5481709675:AAHXiR9vkhImbsGriupoCvlo1cSCC61KUMY"
    bot = telebot.TeleBot(bot_token)

    file = open("setup.json", "r", encoding='utf-8')
    setup_object = json.loads(file.read())
    file.close()

    def generate_empty_categories():
        result = {}
        for el in setup_object["categories"]:
            result.update({el:0})
        return result
    categories = generate_empty_categories()

    def generate_empty_votes():
        result = {}
        for el in setup_object["teams"]:
            result.update({el:generate_empty_categories()})
        return result
    teams = generate_empty_votes()

    def generate_empty_judges():
        result = {}
        for el in setup_object["judges"]:
            result.update({el:{"chat_id":0, "team":"", "category":"", "teams":copy.deepcopy(teams), "editing":False}})
        return result
    current_vote = generate_empty_judges()

    def UpdateJudgeById(id, update):
        for key, value in current_vote.items():
            if value["chat_id"] == id:
                current_vote[key].update(update)

    def GetJudgeById(id):
        for key, value in current_vote.items():
            if value["chat_id"] == id:
                return value

    def GetJudgeNameById(id):
        for key, value in current_vote.items():
            if value["chat_id"] == id:
                return key
        return id

    def HasJudgeWithId(id):
        for key, value in current_vote.items():
            if value["chat_id"] == id:
                return True
        return False

    def AddListToMarkup(markup, list):
        for el in list:
            markup.add(types.KeyboardButton(el))
        return markup

    @bot.message_handler(commands=['start'])
    def start_command_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if HasJudgeWithId(message.chat.id):
            markup.add(GetJudgeNameById(message.chat.id))
        else:
            judges = []
            for judge in setup_object["judges"]:
                if current_vote[judge]["chat_id"] == 0:
                    judges.append(judge)
            AddListToMarkup(markup, judges)
        bot.send_message(message.chat.id, "Пожелуйста представьтесь", reply_markup=markup)

    @bot.message_handler(commands=['values'])
    def start_message(message):
        bot.send_message(message.chat.id, str(current_vote).replace("{", "{\n").replace("}", "\n}").replace(",", ",\n"))

    @bot.message_handler(commands=['load'])
    def start_message(message):
        file = open("votes.json", "r", encoding='utf-8')
        global current_vote
        current_vote = json.loads(file.read())
        file.close()
        bot.send_message(message.chat.id, "Данные успешно загружены")

    @bot.message_handler(commands=['calculate'])
    def start_message(message):
        calculate()
        update_sheets(current_vote)
        bot.send_message(message.chat.id, "Успешно")

    @bot.message_handler(commands=['table'])
    def start_message(message):
        SendTable(GetJudgeById(message.chat.id), bot, message)

    def TeamSellector(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        arr = []
        judge = GetJudgeById(message.chat.id)
        for key1, value in judge["teams"].items():
            for key2, value in value.items():
                if value == 0 or judge["editing"]:
                    arr.append(key1)
                    break
        arr.append("Изменить Оценку")
        AddListToMarkup(markup, arr)
        bot.send_message(message.chat.id, "Выберите комманду", reply_markup=markup)

    def CategorySellector(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        arr = []
        judge = GetJudgeById(message.chat.id)
        for key, value in judge["teams"][judge["team"]].items():
            if value == 0 or judge["editing"]:
                arr.append(key)
        AddListToMarkup(markup, arr)
        if judge["editing"]:
            markup.add("Завершить редактирование")
        else:
            markup.add("Вернуться к выбору комманды")
        bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup)

    @bot.message_handler(content_types="text")
    def log_judge_in(message):
        print(str(GetJudgeNameById(message.chat.id))+": "+message.text)
        if message.text in setup_object["judges"]:
            current_vote[message.text]["chat_id"] = message.chat.id
            TeamSellector(message)

        if not HasJudgeWithId(message.chat.id):
            start_command_message(message)
            return

        if message.text == "Вернуться к выбору комманды":
            TeamSellector(message)

        if message.text == "Завершить редактирование":
            UpdateJudgeById(message.chat.id, {"editing":False})
            TeamSellector(message)

        if message.text == "Изменить Оценку":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            AddListToMarkup(markup, setup_object["teams"])
            bot.send_message(message.chat.id, "Выберите комманду", reply_markup=markup)
            UpdateJudgeById(message.chat.id, {"editing":True})

        if message.text in setup_object["teams"]:
            UpdateJudgeById(message.chat.id, {"team":message.text})
            CategorySellector(message)
            SendTable(GetJudgeById(message.chat.id), bot, message)

        if message.text in setup_object["categories"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("1", "2", "3")
            markup.add("4", "5", "6")
            markup.add("7", "8", "9")
            markup.add("10")
            bot.send_message(message.chat.id, "Выберите оценку", reply_markup=markup)
            UpdateJudgeById(message.chat.id, {"category":message.text})

        if message.text.isnumeric():
            bot.send_message(message.chat.id, "Спасибо за отметку")
            vote = GetJudgeById(message.chat.id)
            vote["teams"][vote["team"]][vote["category"]] = int(message.text)
            GoTo = 0
            categoriesArr = []
            for key, value in vote["teams"][vote["team"]].items():
                if value == 0 or vote["editing"]:
                    GoTo=1
                    categoriesArr.append(key)
            if GoTo == 1:
                CategorySellector(message)
            else:
                bol = False
                for key, value in vote["teams"].items():
                    bl = False
                    for key1, value1 in value.items():
                        if value1 == 0 or vote["editing"]:
                            bl = True
                            break
                    if bl:
                        bol = True
                        break
                if bol:
                    TeamSellector(message)
                else:
                    markup = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, "Спасибо за оценку, комманды закончились", reply_markup=markup)
            SendTable(vote, bot, message)
        file = open("votes.json", "w", encoding='utf-8')
        json.dump(current_vote, file, ensure_ascii=False)
        file.close()
    print("bot is ready to work!")
    return bot

if (__name__ == "__main__"):
    generate_judge_helper().infinity_polling()