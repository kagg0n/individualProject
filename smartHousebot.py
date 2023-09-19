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
lightMeasure = ''

#--- CODENAME "RADAR" -----
anyBodyThere = ''

@bot.message_handler(commands=['start'])


def start(message):
    Inlinemarkup = types.InlineKeyboardMarkup(row_width=2)

    led_button = types.InlineKeyboardButton("LED лента", callback_data="LED лента")
    tempMeasure = types.InlineKeyboardButton("Температура", callback_data="Температура")
    lightMeasure = types.InlineKeyboardButton("Освещенность", callback_data="Освещенность")
    anyAround = types.InlineKeyboardButton("Датчик присутствия", callback_data="Датчик присутствия")
    humidityButton = types.InlineKeyboardButton("Датчик влажности",callback_data="Датчик влажности")

    KeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    updateData = types.InlineKeyboardButton("Обновить данные",callback_data = "Обновить данные")


    Inlinemarkup.add(led_button,tempMeasure)
    Inlinemarkup.add(lightMeasure,anyAround)
    Inlinemarkup.add(humidityButton)
    Inlinemarkup.add(updateData)
    bot.send_message(message.from_user.id, "👋Приветствую, я чат-бот, созданный для управления умным домом")
    bot.send_message(message.from_user.id, "Все доступные на данный момент функции будут отображены внизу⬇️")
    bot.send_message(message.from_user.id, "Умные устройства:", reply_markup=Inlinemarkup)
 

def main_menu(reply):
    Inlinemarkup = types.InlineKeyboardMarkup(row_width=2)

    led_button = types.InlineKeyboardButton("LED лента", callback_data="LED лента")
    tempMeasure = types.InlineKeyboardButton("Температура", callback_data="Температура")
    lightMeasure = types.InlineKeyboardButton("Освещенность", callback_data="Освещенность")
    anyAround = types.InlineKeyboardButton("Датчик присутствия", callback_data="Датчик присутствия")
    humidityButton = types.InlineKeyboardButton("Датчик влажности",callback_data="Датчик влажности")

    KeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    updateData = types.InlineKeyboardButton("Обновить данные",callback_data = "Обновить данные")


    Inlinemarkup.add(led_button,tempMeasure)
    Inlinemarkup.add(lightMeasure,anyAround)
    Inlinemarkup.add(humidityButton)
    Inlinemarkup.add(updateData)
    
    bot.send_message(reply.from_user.id, "Основное меню чат-бота:")
    bot.send_message(reply.from_user.id, "Умные устройства:",reply_markup = Inlinemarkup)

@bot.message_handler(content_types=['text'])

def get_text_message(message):
    if message.text == "Вернуться в главное меню💾":
        main_menu(message)

@bot.callback_query_handler(func = lambda call: True)

def get_callback(call):

    global status
    global rawData
    global tempValues
    global led_value
    global lightMeasure
    global anyBodyThere
    global humidityValues
    try:
        if call.data == "Обновить данные":
            sock = 0
            try:
                led_value = ''
                tempValues = ''
                humidityValues = ''
                lightMeasure = ''
                anyBodyThere  = ''
                sock = socket.socket()
                sock.connect(('192.168.0.111', 3030))
                key = sock.send('1'.encode('utf-8'))
                data = sock.recv(1024) # Получаем данные из сокета.
                rawData = data.decode('utf-8')
                sock.close()
                decoding_protocol()
                
                bot.send_message(call.message.chat.id, "Обновили данные умного дома")
                main_menu(call)
            except:
                bot.send_message(call.message.chat.id, "Не удалось подключиться к хабу умного дома")
                sock.close()
                main_menu(call)
        if call.data == "LED лента":
            if led_value == '1':
                status = "Устройство включено🔆"
            else:
                status = "Устройство отключено💤"

            Inlinemarkup = types.InlineKeyboardMarkup(row_width = 2) #создание новых кнопок
            setOn = types.InlineKeyboardButton('Включить', callback_data='Включить')
            setOff = types.InlineKeyboardButton('Выключить', callback_data='Выключить')
            KeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard= True)
            backMenu1 = types.InlineKeyboardButton('Вернуться в главное меню💾')
            Inlinemarkup.add(setOn, setOff)
            KeyboardMarkup.add(backMenu1)
            bot.send_message(call.message.chat.id, "Тип устройства: LED лента")
            bot.send_message(call.message.chat.id, status, reply_markup = Inlinemarkup)
            bot.send_message(call.message.chat.id, "Вы также можете вернуться в главное меню", reply_markup = KeyboardMarkup)

        if call.data == "Включить":
            if led_value == '1' or led_value == '2':
                bot.send_message(call.message.chat.id, "Устройство уже включено")
            elif led_value == '0':
                sock = socket.socket()
                sock.connect(('192.168.0.111', 3030))
                key = sock.send('2'.encode('utf-8'))
                sock.close()
                bot.send_message(call.message.chat.id,"Устройство включено")
        if call.data == "Выключить":
            if led_value != 0:
                sock = socket.socket()
                sock.connect(('192.168.0.111', 3030))
                key = sock.send('3'.encode('utf-8'))
                sock.close()
                bot.send_message(call.message.chat.id,"Устройство выключено")
            else:
                bot.send_message(call.message.chat.id, "Устройство уже выключено")
                  
            #--------------TEMPERATURE-----------------------------
            # need to add temp measuring in real time

        if call.data == "Температура":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
            backMenu = types.InlineKeyboardButton('Вернуться в главное меню💾')
            markup.add(backMenu)
            bot.send_message(call.message.chat.id, "Тип устройства: датчик температуры📈")
            bot.send_message(call.message.chat.id, "Температура на данный момент:")
            bot.send_message(call.message.chat.id, tempValues, reply_markup = markup)
        
        if call.data == "Датчик присутствия":
            if anyBodyThere == '1':
                anyBodyThereStatus = "На данный момент в помещении кто-то есть"
            else:
                anyBodyThereStatus = "На данный момент в комнате никого"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
            backMenu = types.InlineKeyboardButton('Вернуться в главное меню💾')
            markup.add(backMenu)
            bot.send_message(call.message.chat.id, "Тип устройства: датчик присутствия")
            bot.send_message(call.message.chat.id, "На данный момент:")
            bot.send_message(call.message.chat.id, anyBodyThereStatus, reply_markup = markup)

        if call.data == "Освещенность":

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
            backMenu = types.InlineKeyboardButton('Вернуться в главное меню💾')
            markup.add(backMenu)
            bot.send_message(call.message.chat.id, "Тип устройства: датчик освещенности")
            bot.send_message(call.message.chat.id, "На данный момент количетство единиц освещенности:") # нужно добавить единицу измерения
            bot.send_message(call.message.chat.id, lightMeasure, reply_markup = markup)
        
        if call.data == "Датчик влажности":

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
            backMenu = types.InlineKeyboardButton('Вернуться в главное меню💾')
            markup.add(backMenu)
            bot.send_message(call.message.chat.id, "Тип устройства: датчик влажности воздуха")
            bot.send_message(call.message.chat.id, "На данный момент влажность воздуха в процентах:") # нужно добавить единицу измерения
            bot.send_message(call.message.chat.id, humidityValues, reply_markup = markup)


        #-------------MAIN MENU--------------------------------

    except Exception as e:
         print(repr(e))

def decoding_protocol():
    # ПЕРВОЕ - ТЕМПЕРАТУРА ВТОРОЕ - ВЛАЖНОСТЬ ТРЕТЬЕ - СВЕТОДИОДНАЯ ЛЕНТА ЧЕТВЕРТОЕ - ОСВЕЩЕННОСТЬ ПЯТОЕ - ДАТЧИК ПРИСУТСТВИЯ
    global led_value
    global tempValues
    global humidityValues
    global lightMeasure
    global anyBodyThere
    
    i = 0
    while rawData[i] != '/':
        tempValues = tempValues + rawData[i]
        i = i + 1

    i = i + 1
    while rawData[i] != '/':
        humidityValues = humidityValues + rawData[i]
        i = i + 1
    i = i + 1
    while rawData[i] != '/':
        led_value = led_value + rawData[i]
        i = i + 1
    i = i + 1
    while rawData[i] != '/':
        lightMeasure = lightMeasure + rawData[i]
        i = i + 1
    for n in range(len(rawData) - (i + 1)):
        f = n + 1
        anyBodyThere = anyBodyThere + rawData[i + f]
          
bot.polling(none_stop=True, interval=0)