import json
import requests
import time
import urllib
import config
from sqlconf import DBHelper

db = DBHelper()

URL = "https://api.telegram.org/bot426181493:AAGbT_LuD9ll4d_0yefhpGDzr4cs5PiZhKE/"


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def string_format(text):
    i = 0
    text=text.lower()
    new = list(text)
    while (i < len(new)):
        if not((new[i] < 'z' and new[i] > 'A')or((new[i] < 'я' and new[i] > 'А'))):
            if i == 0:
                del (new[i])
            elif i + 1 == len(new):
                del (new[i])
                i=i-1
            else:
                new[i] = chr(32)
                if new[i - 1] == chr(32):
                    del (new[i - 1])
                else:
                    i=i+1
        else:
            i = i + 1

    text = ''.join(new)
    return text


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items(chat)
        if text == "/start":
            send_message(
                "Welcome to your personal Word counter. Send any text to me and I'll parse words and store them as items. All punctuation marks and symbols will be ignored",
                chat)
        elif text == "/reset":
            db.deletetable()
            db.setup()
            send_message("Everything deleted", chat)
        elif text=="/beoperator":
            operators=db.get_operators(chat)
            if str(chat) in operators:
                send_message("You have already become an operator",
                    chat)
            else:
                db.add_operator(chat)
                send_message("Now you are operator, wait for your clients, you can stop this with /stopoperator command",
                    chat)
        elif text=="/findoperator":
            operator=db.get_operator(chat)
            if operator:
                send_message(
                    "You already have an operator",
                    chat)
                continue
            freeoperator=db.get_freeoperator()
            if freeoperator:
                db.update_operator(freeoperator[0],chat)
                send_message(
                    "Now you have an operator, /killoperator will stop this if you want",
                    chat)
                send_message(
                    "Now you have a client, /stopoperator will stop this if u want",
                    freeoperator[0])
            else:
                send_message(
                    "We dont have free operators now",
                    chat)
        elif text=="/clientwords":
            client=db.get_client(chat)
            if len(client)==0:
                send_message("You dont have a client", chat)
            else:
                words=db.get_top5words(chat)
                for word in words:
                    count=db.get_countforitem(word)
                    send_message("Client have used *" + word + "* " + str(count) + " times", chat)
        elif text == "/killoperator":
            operator=db.get_operator(chat)
            if len(operator)==0:
                send_message("You dont have an operator", chat)
                continue
            db.update_operator(operator[0],'')
            send_message("Now you dont have an operator",chat)
            send_message("You have been killed by your client",operator[0])
        elif text == "/stopoperator":
            operators=db.get_operators(chat)
            if str(chat) not  in operators:
                send_message("You are not an operator",
                    chat)
            else:
                client = db.get_client(chat)
                db.delete_operator(chat)
                if len(client)!=0:
                    send_message("Now you dont have an operator", client[0])
                send_message("You have been killed by yourself",chat)
        elif text.startswith("/"):
            continue
        else:
            text = string_format(text)
            if(text.find(" ")!=-1):
                texts = text.split(' ')
            else:
                texts=list([text])
            for temp in texts:
                if temp in items and len(temp) > 0:
                    count = db.update_item(temp, chat)
                    count = count[0]
                    items = db.get_items(chat)
                    keyboard = build_keyboard(items)
                    send_message("You have used *" + temp + "* " + str(count) + " times", chat, keyboard)
                else:
                    db.add_item(temp, chat)
                    items = db.get_items(chat)
                    send_message("You have used *" + temp + "* " + "1" + " time", chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": False}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates['result']) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
