import json
import os

def calculate():
    file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "votes.json"), "r", encoding='utf-8')
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