import gspread
import json

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

if __name__ == "__main__":
    f = open("votes.json", "r", encoding='utf-8')
    votes = json.loads(f.read())
    f.close()
    update_sheets(votes)