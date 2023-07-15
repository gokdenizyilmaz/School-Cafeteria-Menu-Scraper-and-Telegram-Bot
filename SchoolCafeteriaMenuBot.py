from pyrogram import Client, filters
import asyncio
import requests
from bs4 import BeautifulSoup
import re
res = requests.get('https://sksdb.hacettepe.edu.tr/bidbnew/grid.php?parameters=qbapuL6kmaScnHaup8DEm1B8maqturW8haidnI%2Bsq8F%2FgY1fiZWdnKShq8bTlaOZXq%2BmwWjLzJyPlpmcpbm1kNORopmYXI22tLzHXKmVnZykwafFhImVnZWipbq0f8qRnJ%2BioF6go7%2FOoplWqKSltLa805yVj5agnsGmkNORopmYXam2qbi%2Bo5mqlXRrinJdf1BQUFBXWXVMc39QUA%3D%3D')
soup = BeautifulSoup(res.text, 'html.parser') 


match = soup.find('div', class_ ='col-lg-9 col-12 mb-3')
yemekler = match.text



# Telegram API anahtarları
api_id = " "
api_hash = ' '
bot_token = ' '

# Pyrogram istemcisini oluşturma
app = Client("client", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


def find_menu_items(input_date, text):
    regex = r"(\d{1,2}\.\d{1,2}\.\d{4})\s.*?Menü:\s(.*?)\s\*"
    matches = re.findall(regex, text)

    for match in matches:
        date = match[0]
        menu_items = match[1]
        if date == input_date:
            return menu_items.strip()
    
    return "Tarih bulunamadı"



@app.on_message(filters.private)
def handle_message(client, message):
    content = message.text
    print("Kullanıcının gönderdiği mesaj:", content)
    
    #kullanıcının gönderdiği mesaja ait tarihin günün yemek menüsü
    output = find_menu_items(content, yemekler)
    #kullanıcının söylediği tarihe ait yemek menüsünü  chatte gösteren kod
    client.send_message(
        chat_id=message.chat.id,
        text=f"{content} tarihindeki yemek menüsü: {output}"
    )
    

# Pyrogram istemcisini başlatma
app.run()
