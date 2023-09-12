import telebot
from telebot import types

#DEVICE TYPES
# 1 - LED
# 2 - TEMPERATURE MEASURING
# 3 - LIGHT MEASURING
# 4 PRESSURE MEASURING
bot = telebot.TeleBot('6570224062:AAG43G3pLc3DnB3BFFbQC9_jCvKpywZ3BAs')

#DEVICE PARAMETRS (back part of the project that will use micropython to communicate with sensors, lamps and etc)

#---LED---
led_status = 0 # on/off

#---TEMPERATURE MEASURING---
tempMeasure  = 27
humidityMeasure = 60

#---LIGHT MEASURING----
lightMeasure = 100

@bot.message_handler(commands=['start'])

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    led_button = types.KeyboardButton(text='LED лента')
    tempMeasure = types.KeyboardButton(text = 'Температура')
    lightMeasure = types.KeyboardButton(text = 'Освещенность')

    markup.row(led_button,tempMeasure)
    markup.add(lightMeasure)
    bot.send_message(message.from_user.id, "👋Приветствую, я чат-бот, созданный для управления умным домом")
    bot.send_message(message.from_user.id, "Все доступные на данный момент функции будут отображены внизу⬇️")
    bot.send_message(message.from_user.id, "Умные устройства:\n 🔸Управляемая LED лента \n 🔸Датчик температуры \n 🔸Датчик влажности \n 🔸Датчик освещенности",reply_markup = markup)
    bot.send_message(message.from_user.id, "Основное меню чат-бота:",reply_markup = markup)

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    led_button1 = types.InlineKeyboardButton(text='LED лента')
    tempMeasure1 = types.KeyboardButton(text = 'Температура')
    lightMeasure1 = types.KeyboardButton(text = 'Освещенность')

    markup.row(led_button1,tempMeasure1)
    markup.add(lightMeasure1)
    bot.send_message(message.from_user.id, "Основное меню чат-бота:")
    bot.send_message(message.from_user.id, "Умные устройства:\n 🔸Управляемая LED лента \n 🔸Датчик температуры \n 🔸Датчик влажности \n 🔸Датчик освещенности",reply_markup = markup)
@bot.message_handler(content_types=['text'])


def get_text_message(message):
    #-----------------LED SETTINGS-----------------------
    global status
    if message.text == "LED лента":
        if led_status == 1:
            status = "Устройство включено🔆"
        else:
            status = "Устройство отключено💤"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        setOn = types.KeyboardButton('Включить')
        setOff = types.KeyboardButton('Выключить')
        backMenu1 = types.InlineKeyboardButton('Вернуться в главное меню💾')
        markup.row(setOn, setOff)
        markup.add(backMenu1)
        bot.send_message(message.from_user.id, "Тип устройства: LED лента")
        bot.send_message(message.from_user.id, status, reply_markup = markup)
    #--------------TEMPERATURE-----------------------------
    # need to add temp measuring in real time
    if message.text == "Температура":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        realTemp = types.KeyboardButton('Измерить температуру')
        backMenu = types.InlineKeyboardButton('Вернуться в главное меню💾')
        markup.add(realTemp)
        markup.add(backMenu)
        bot.send_message(message.from_user.id, "Тип устройства: датчик температуры📈")
        bot.send_message(message.from_user.id, "Температура на данный момент:")
        bot.send_message(message.from_user.id, tempMeasure, reply_markup = markup)
        bot.send_message(message.from_user.id, "Подсказка: Вы также можете измерить температуру в помещении в реальном времени(пока недоступно)")
        
    #-------------MAIN MENU--------------------------------
    if message.text == "Вернуться в главное меню💾":
        main_menu(message)
    
        
bot.polling(none_stop=True, interval=0)