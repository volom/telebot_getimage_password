# import libraries
import telebot
import requests
from db_handler.db_formation import *

API_TOKEN = 'API TOKEN' # API token of bot
PASSWORD = 'password' # password for getting access to the bot
ATTEMPTS_NUMBER = 5 # number of attempts to input the password. 
FLAG_ENTERED_PASSWORD = False


# Initializing bot 
bot = telebot.TeleBot(API_TOKEN)


# Greetings and password
greetings_txt =  """
Hi! I am YOURBOTNAME bot. Please, enter password for using the bot
                 """

@bot.message_handler(commands=['start'])
def greeting_msg(message):
    bot.send_message(message.chat.id, greetings_txt)


# Checking password and further interaction
@bot.message_handler(content_types=['text'])
def get_password(message):
    global FLAG_ENTERED_PASSWORD

    if not FLAG_ENTERED_PASSWORD:
        csv_save_user(message.chat.id, message.text)

        if user_pass(message.chat.id, attempts_number=ATTEMPTS_NUMBER, right_password=PASSWORD)[0]:
            # actions in case of correct password input
            FLAG_ENTERED_PASSWORD = True
            bot.send_message(message.chat.id, "OK. Send me a photo, please") 
        else:
            if user_pass(message.chat.id, attempts_number=ATTEMPTS_NUMBER, right_password=PASSWORD)[1] >= ATTEMPTS_NUMBER:
                bot.send_message(message.chat.id, "ACCESS TO THE BOT DENIED!")
            else:
                bot.send_message(message.chat.id, f"Wrong password! Attempts {user_pass(message.chat.id, attempts_number=ATTEMPTS_NUMBER, right_password=PASSWORD)[1]}/{ATTEMPTS_NUMBER}")
    
    else:
        bot.send_message(message.chat.id, "Please, send photo in propper format")   


# get image from user and save it
@bot.message_handler(content_types=['photo'])
def on_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
    with open('photo.jpg','wb') as f:
        f.write(file.content)
    bot.send_message(message.chat.id, "Thank you! You can put another photo!")


# prevent user from sending photo in file format
@bot.message_handler(content_types=['file'])
def not_photo(message):
    bot.send_message(message.chat.id, "Please, send photo in propper format")


bot.infinity_polling()