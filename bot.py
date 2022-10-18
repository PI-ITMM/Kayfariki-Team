import telebot

token = INPUT_TOKEN_YOUR_BOT
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text == "/start":
        bot.reply_to(message, 'Добро пожаловать в бота расписаний. Для просмотра команд введите /help.')
    elif message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/help - просмотр команд;\n/mygroup - указать свою группу;\n/myname - указать ФИО.\n\n Администратор: @olithiumsunset.")
    else:
        bot.send_message(message.from_user.id, "По всей видимости такой команды нет. Список команд: /help.\n\nВы написали: " + message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)