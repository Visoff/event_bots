import imgkit

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