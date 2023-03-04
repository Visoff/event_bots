import copy
import json
import telebot
from telebot import types
bot_token = "5481709675:AAHXiR9vkhImbsGriupoCvlo1cSCC61KUMY"
bot = telebot.TeleBot(bot_token)

file = open("setup.json", "r", encoding='utf-8')
setup_object = json.loads(file.read())
file.close()

#imports from custom modules
import imgkit
import gspread
#count_votes -> calculate
def calculate():
    file = open("votes.json", "r", encoding='utf-8')
    votes = json.loads(file.read())
    file.close()

    for key, value in votes.items():
        file = open("results/"+key+"_"+str(value["chat_id"])+".txt", "w", encoding='utf-8')
        for key, value in value["teams"].items():
            file.write(key+":\n")
            for key, value in value.items():
                file.write(
                    "   "+key+": "+str(value)+"\n"
                )
        file.close()

    teams = {}
    categories = {"Сумма":{"team":"", "points":0}}
    for key, value in votes.items():
        for team, value in value["teams"].items():
            if team not in teams:
                teams.update({team:{}})
            for category, points in value.items():
                if category not in teams[team]:
                    teams[team].update({category:0})
                    categories.update({category:{"team":"", "points":-1}})
                teams[team][category] += points


    file = open("results/total.txt", "w", encoding='utf-8')
    for team, value in teams.items():
        file.write(team+":\n")
        total = 0
        for category, points in value.items():
            if categories[category]["points"] < points:
                categories[category]["points"] = points
                categories[category]["team"] = team
            if categories[category]["points"] == points and categories[category]["team"] != team:
                categories[category]["team"] += " и " + team
            total += points
            file.write("   "+category+": "+str(points)+"\n")
        file.write("   Сумма: "+str(total)+"\n")
        if categories["Сумма"]["points"] < total:
            categories["Сумма"]["points"] = total
            categories["Сумма"]["team"] = team
            if categories["Сумма"]["points"] == total and categories["Сумма"]["team"] != team:
                categories["Сумма"]["team"] += " и " + team

    file.write("\n\n")

    for category, value in categories.items():
        file.write(category+":\n"+value["team"]+": "+str(value["points"])+"\n")
    file.close()
#table -> SendTable
def SendTable(judge, bot, message):
    tableList = [[""]]
    for team, value in judge["teams"].items():
        tableList.append([team])
        i = 1
        for category, points in value.items():
            if i >= len(tableList[0]):
                tableList[0].append(category)
            tableList[len(tableList)-1].append(str(points))
            i+=1

    html = """
    <style>
        * {
            background: transparent;
        }
        table tr td {
            outline: 1px solid black;
            font-size:2rem;
        }
    </style>
    <table style="width:1000px; position: absolute; top:0; left:0;">
    TableInside
    </table>
    """

    table = ""
    for row in tableList:
        if row[0] == judge["team"]:
            table+="<tr style='color:green; font-weight: bold;'>"
        else:
            table+="<tr>"
        for el in row:
            table+="<td>"+el+"</td>"
        table+="</tr>"

    html = html.split("TableInside")
    html = html[0] + table + html[1]

    img = imgkit.from_string(html, False, options={
        "transparent":"",
        "crop-w":1000
    })
    bot.send_photo(message.chat.id, img)
#sheets -> update_sheets
def update_sheets(votes):
    gc = gspread.service_account(filename="circular-light-367014-d28e8061df54.json")
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/19uFrYI3_TsF0jGYvx4fUvWVH8_i1IDVxFyznkGmPiOc')
    table = [["City Heroes"]]
    judgeI = 0
    for judge, value in votes.items():
        teamI = 1
        for team, value1 in value['teams'].items():
            if judgeI==0:
                i = len(table)
                table.append([team])
            total = 0
            for category, points in value1.items():
                total += points
                if (category not in table[0]):
                    table[0].append(category)
                if (judgeI==0):
                    table[i].append(points)
                else:
                    table[teamI][table[0].index(category)] += points
            if ("Сумма" not in table[0]):
                table[0].append("Сумма")
            if (judgeI==0):
                table[i].append(total)
            else:
                table[teamI][table[0].index("Сумма")] += total
            teamI += 1
        judgeI += 1
    sh.sheet1.update('A1', table)
    i = 2
    while True:
        col = sh.sheet1.col_values(i)
        if (len(col) >= 2):
            color = col.index(str(max([int(el) for el in col[1::]])))+1
            sh.sheet1.format(chr(ord("a")+i-1).upper()+str(color), {"backgroundColor":{"red":1.0, "green":1.0, "blue":0.0}})
        else:
            break
        i+=1

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
bot.infinity_polling()