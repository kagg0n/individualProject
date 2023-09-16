#---------LIBARARIES---------------

import telebot
from telebot import types
import socket

#--------SOCKET SETTINGS------------
bot = telebot.TeleBot('6570224062:AAG43G3pLc3DnB3BFFbQC9_jCvKpywZ3BAs')

#DEVICE PARAMETRS (back part of the project that will use micropython to communicate with sensors, lamps and etc)

#---LED---
led_value = '' # on/off

#---TEMPERATURE MEASURING---
tempValues = ''
humidityValues = ''

#---LIGHT MEASURING----
lightMeasure = 100

@bot.message_handler(commands=['start'])

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    led_button = types.KeyboardButton( text="LED лента")
    tempMeasure = types.KeyboardButton(text = 'Температура')
    lightMeasure = types.KeyboardButton(text = 'Освещенность')
    updateData = types.KeyboardButton(text = "Обновить данные")


    markup.row(led_button,tempMeasure)
    markup.add(lightMeasure)
    markup.add(updateData)
    bot.send_message(message.from_user.id, "👋Приветствую, я чат-бот, созданный для управления умным домом")
    bot.send_message(message.from_user.id, "Все доступные на данный момент функции будут отображены внизу⬇️")
    bot.send_message(message.from_user.id, "Основное меню чат-бота:")
    bot.send_message(message.from_user.id, "Умные устройства:\n 🔸Управляемая LED лента \n 🔸Датчик температуры \n 🔸Датчик влажности \n 🔸Датчик освещенности",reply_markup = markup)

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    led_button1 = types.KeyboardButton(text='LED лента')
    tempMeasure1 = types.KeyboardButton(text = 'Температура')
    lightMeasure1 = types.KeyboardButton(text = 'Освещенность')
    updateData1 = types.KeyboardButton(text = "Обновить данные")

    markup.row(led_button1,tempMeasure1)
    markup.add(lightMeasure1)
    markup.add(updateData1)
    bot.send_message(message.from_user.id, "Основное меню чат-бота:")
    bot.send_message(message.from_user.id, "Умные устройства:\n 🔸Управляемая LED лента \n 🔸Датчик температуры \n 🔸Датчик влажности \n 🔸Датчик освещенности",reply_markup = markup)
@bot.message_handler(content_types=['text'])


def get_text_message(message):
    #-----------------LED SETTINGS-----------------------

    global status
    global rawData
    global tempValues
    global led_value
    if message.text == "Обновить данные":
        sock = 0
        try:
            led_value = ''
            tempValues = ''
            humidityValues = ''
            sock = socket.socket()
            sock.connect(('192.168.0.104', 3030))
            key = sock.send('1'.encode('utf-8'))
            data = sock.recv(1024) # Получаем данные из сокета.
            rawData = data.decode('utf-8')
            sock.close()
            decoding_protocol()
            bot.send_message(message.from_user.id, "Обновили данные умного дома")
            main_menu(message)
        except:
            bot.send_message(message.from_user.id, "Не удалось подключиться к хабу умного дома")
            sock.close()
            main_menu(message)
    if message.text == "LED лента":
        if led_value == '1':
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
        backMenu = types.InlineKeyboardButton('Вернуться в главное меню💾')
        markup.add(backMenu)
        bot.send_message(message.from_user.id, "Тип устройства: датчик температуры📈")
        bot.send_message(message.from_user.id, "Температура на данный момент:")
        bot.send_message(message.from_user.id, tempValues, reply_markup = markup)
        
    #-------------MAIN MENU--------------------------------

    if message.text == "Вернуться в главное меню💾":
        main_menu(message)

def decoding_protocol():
	global led_value
	global tempValues
	global humidityValues
    
	i = 0
	while rawData[i] != '/':
		tempValues = tempValues + rawData[i]
		i = i + 1
	i = i + 1
	while rawData[i] != '/':
		humidityValues = humidityValues + rawData[i]
		i = i + 1
	for n in range(len(rawData) - (i + 1)):
		f = n + 1
		led_value = led_value + rawData[i + f]
bot.polling(none_stop=True, interval=0)