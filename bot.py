import telebot
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

token = "5685287693:AAGR5y8lytOjiF_2Cqrq72XjaNQ1l-mebWI"
bot = telebot.TeleBot(token)

driver = webdriver.Edge()
driver.get("https://portal.unn.ru/ruz/main")
elemLogin = driver.find_element(By.NAME, "USER_LOGIN")
elemLogin.send_keys("INPUT_LOGIN")
elemPassword = driver.find_element(By.NAME, "USER_PASSWORD")
elemPassword.send_keys("INPUT_PASSWORD")
elemPassword.send_keys(Keys.ENTER)
userGroup = {}

assert "No results found." not in driver.page_source

@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text == "/start":
        bot.reply_to(message, 'Добро пожаловать в бота расписаний. Для просмотра команд введите /help.')
    elif message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/help - просмотр команд;\n/rasp - выдать расписание (доступно после ввода группы)\n/mygroup - указать свою группу;\n/myname - указать ФИО.\n\n Администратор: @olithiumsunset.")
    elif message.text == "/mygroup":
        msg = bot.send_message(message.from_user.id, "Введите номер вашей группы: ")
        bot.register_next_step_handler(msg, group_step)
    elif message.text == "/rasp":
        if len(userGroup) == 0:
            bot.send_message(message.from_user.id, "Пожалуйста, введите номер своей группы через /mygroup!")
        else:
            elemGroup = driver.find_element(By.ID, "autocomplete-group") 
            elemGroup.send_keys("")
            elemGroup.send_keys(userGroup) # Добавить sleep 1000
            time.sleep(2)
            elemGroup.send_keys(Keys.RETURN)
            s = BeautifulSoup(driver.page_source, 'html.parser')
            l = s.find_all_next("span", {'class:' 'bx-im-fullscreen-bg'})
            bot.send_message(message.from_user.id, l.text)
    else:
        bot.send_message(message.from_user.id, "По всей видимости такой команды нет. Список команд: /help.\n\nВы написали: " + message.text)

def group_step(message):
    user_info = {}
    user_info['group'] = message.text
    bot.send_message(message.from_user.id, "Номер группы ({}) сохранен.".format(user_info["group"]))
    global userGroup
    userGroup = user_info["group"]

if __name__ == '__main__':
    bot.polling(none_stop=True)
