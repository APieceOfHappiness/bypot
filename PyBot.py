import random
import telebot
from telebot import types

TOKEN = '5788792002:AAG7KnVLSnErx8lIHIGbCyrRC8d_gXEfr1w' # указываем токен нашего бота (для этого надо создать бота в @BotFather)


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=["new_chat_members"])
def adding_new_member(message):
    global users_id
    bot.send_message(message.chat.id, "Hello " + message.from_user.first_name)
    bot.send_message(message.chat.id, "Ты тоже убеждён, что первая группа изоморфна, а вторая нет?")
    if message.from_user.id not in users_id:
        users_id.append(message.from_user.id)
    print(users_id)


users_id = []
try:
    with open('members.txt', 'r') as f:
        s = f.readline()
        while s != "":
            users_id.append(int(s))
            s = f.readline()
except FileNotFoundError:
    f = open('members.txt', 'w') # Создаём файл
    f.close()

@bot.message_handler(commands=['start'])
def menu(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text="Сделать кого-то в чате админом", callback_data="promote")
    button2 = types.InlineKeyboardButton(text="Забань кого-нибудь", callback_data="ban")
    button3 = types.InlineKeyboardButton(text="Дай стату", callback_data="statistics")
    button4 = types.InlineKeyboardButton(text="Уйди отсюда😢", callback_data="leave")
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, '<------menu------>', reply_markup=markup)
    bot.send_message(message.chat.id, 'To unban a person, you need to write: unban <user_id>')

@bot.callback_query_handler(func=lambda callback: len(callback.data) > 0)
def actions(callback):
    if callback.data == "statistics":
        ch_memb = bot.get_chat_member_count(callback.message.chat.id)
        admins_list = bot.get_chat_administrators(callback.message.chat.id)
        bot.send_message(callback.message.chat.id, "Chat members: " + str(ch_memb))
        bot.send_message(callback.message.chat.id, "Admins: " + str(len(admins_list)))
        s = ""
        for i in admins_list:
            s += i.user.first_name + '\n'
        bot.send_message(callback.message.chat.id, "They are(Admins):\n" + s)
        return

    if callback.data == "leave":
        bot.send_message(callback.message.chat.id, "Bye:(")
        bot.leave_chat(callback.message.chat.id)
        return

    global users_id
    if len(users_id) == 0:
        bot.send_message(callback.message.chat.id, "Sorry, but I have no people to work with...")
        return


    random_user = users_id[random.randint(0, len(users_id) - 1)]
    if callback.data == "promote":
        bot.promote_chat_member(callback.message.chat.id, random_user, True, True, True)
        return

    # if callback.data == "unban":
    #     bot.send_message(callback.message.chat.id, "id " + str(random_user) + " was unbanned")
    #     bot.unban_chat_member(callback.message.chat.id, random_user)

    if callback.data == "ban":
        bot.send_message(callback.message.chat.id, "id " + str(random_user) + " was banned")
        bot.ban_chat_member(callback.message.chat.id, random_user)
        users_id.remove(random_user)
        return



@bot.message_handler(content_types=['text'])
def unban(message):
    text = message.text.split()
    if len(text) == 2:
        bot.unban_chat_member(message.chat.id, int(text[1]))
        bot.send_message(message.chat.id, "id " + text[1] + " was unbanned")

bot.polling(none_stop=True, interval=0) #запускаем нашего бота

with open('members.txt', 'w') as f:
    for i in users_id:
        f.write(str(i) + '\n')
