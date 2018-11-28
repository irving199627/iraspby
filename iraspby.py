#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os
import sys
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TOKEN = "387854799:AAHmnIEimiLXzZX959RHbX-8LFYIKkuqJOQ"  # SUSTITUIR

#establecemos modo de operacion del pin.

sensor=26
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(9,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)

previous_state = False
current_state = False

commands = {
              'start': 'Arranca el bot',
              'ayuda': 'Comandos disponibles',
}

# COLOR TEXTO
class color:
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

userStep = {}
knownUsers = []

#opciones de menu
menu = types.ReplyKeyboardMarkup()
menu.add("Luces", "Sensor")

#opciones de boton
luz_menu = types.ReplyKeyboardMarkup()
luz_menu.add("Z1", "Z1 off")
luz_menu.add("Z2", "Z2 off")
luz_menu.add("Z3", "Z3 off")
luz_menu.add("Z4", "Z4 off")
luz_menu.add("Z5", "Z5 off")
luz_menu.add("Z6", "Z6 off")
luz_menu.add("Z7", "Z7 off")
luz_menu.add("LMP", "LMP off")
luz_menu.add("Todo", "Todo off")
luz_menu.add("Atras")

menu_sensor = types.ReplyKeyboardMarkup()
menu_sensor.add("Iniciar", "Detener")
menu_sensor.add("Atras")

# USER STEP
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print(color.RED + " [Â¡] Â¡Â¡NUEVO USUARIO!!" + color.ENDC)

# LISTENER
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("[" + str(m.chat.id) + "] " + str(m.chat.first_name) + ": " + m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

# Comando START
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    userStep[cid] = 0
    bot.send_message(cid, "Buen dÃ­a " + str(m.chat.first_name) + "...")
    time.sleep(1)
    bot.send_message(cid, "Que tengas un excelente dÃ­a...\n", reply_markup=menu)

# AYUDA
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Grabar sesion: TermRecord -o /tmp/botlog.html\n"
    help_text += "Comandos disponibles: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)
    bot.send_chat_action(cid, "upload_photo")
    foto = "/tmp/" + (time.strftime("%H%M%S-%d%m%y")) + ".jpeg"
    os.system('fswebcam -d /dev/video0 -r 640x480 --no-banner %s' % foto)
    bot.send_photo(cid, open(foto, 'rb'))
    print 'Foto enviada!'

# MENU PRINCIPAL
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 0)
def main_menu(m):
    cid = m.chat.id
    text = m.text
    if text == "Luces":  # Menu luces
        bot.send_message(cid, "Opciones para Luces:", reply_markup=luz_menu)
        userStep[cid] = 1
    elif text == "Sensor": #Menu sensor
        bot.send_message(cid, "Opciones para Sensor:", reply_markup=menu_sensor)
        userStep[cid]=2
    elif text == "Atras":  # ATRAS
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)


# MENU ENCENDIDO
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def luz_op(m):
    cid = m.chat.id
    txt = m.text
    if txt == "Z1":
        bot.send_message(cid, "[+]LUZ DEL Z1, encendido")
        print(color.GREEN + "[+]Luz del Z1, encendido")
        GPIO.output(21, 1)
    elif txt== "Z1 off":
        bot.send_message(cid, "[+]LUZ DEL Z1, apagado")
        print(color.RED + "[+]Luz del Z1, apagado")
        GPIO.output(21, 0)

    elif txt == "Z2":
        bot.send_message(cid, "[+]LUZ DEL Z2, encendido")
        print(color.GREEN + "[+]LUZ DEL Z2, encendido")
        GPIO.output(9, 1)
    elif txt== "Z2 off":
        bot.send_message(cid, "[+]LUZ DEL Z2, apagado")
        print(color.RED + "[+]Luz del Z2, apagado")
        GPIO.output(9, 0)

    elif txt == "Z3":
        bot.send_message(cid, "[+]LUZ DEL Z3, encendido")
        print(color.GREEN + "[+]Luz del Z3, encendido")
        GPIO.output(10, 1)
    elif txt == "Z3 off":
        bot.send_message(cid, "[+]LUZ DEL Z3, apagado")
        print(color.RED + "[+]Luz del Z3, apagado")
        GPIO.output(10, 0)

    elif txt == "Z4":
        bot.send_message(cid, "[+]LUZ DEL Z4, encendido")
        print(color.GREEN + "[+]Luz del Z4, encendido")
        GPIO.output(22, 1)
    elif txt== "Z4 off":
        bot.send_message(cid, "[+]LUZ DEL Z4, apagado")
        print(color.RED + "[+]Luz del Z4, apagado")
        GPIO.output(22, 0)

    elif txt == "Z5":
        bot.send_message(cid, "[+]LUZ DEL Z5, encendido")
        print(color.GREEN + "[+]Luz del Z5, encendido")
        GPIO.output(27, 1)
    elif txt== "Z5 off":
        bot.send_message(cid, "[+]LUZ DEL Z5, apagado")
        print(color.RED + "[+]Luz del Z5, apagado")
        GPIO.output(27, 0)

    elif txt == "Z6":
        bot.send_message(cid, "[+]LUZ DEL Z6, encendido")
        print(color.GREEN + "[+]Luz del Z6, encendido")
        GPIO.output(17, 1)
    elif txt== "Z6 off":
        bot.send_message(cid, "[+]LUZ DEL Z6, apagado")
        print(color.RED + "[+]Luz del Z6, apagado")
        GPIO.output(17, 0)

    elif txt == "Z7":
        bot.send_message(cid, "[+]LUZ DEL Z7, encendido")
        print(color.GREEN + "[+]Luz del Z7, encendido")
        GPIO.output(20, 1)
    elif txt== "Z7 off":
        bot.send_message(cid, "[+]LUZ DEL Z7, apagado")
        print(color.RED + "[+]Luz del Z7, apagado")
        GPIO.output(20, 0)

    elif txt == "LMP":
        bot.send_message(cid, "[+]LUZ DEL LMP, encendido")
        print(color.GREEN + "[+]Luz del LMP, encendido")
        GPIO.output(16, 1)
    elif txt== "LMP off":
        bot.send_message(cid, "[+]LUZ DEL LMP, apagado")
        print(color.RED + "[+]Luz del LMP, apagado")
        GPIO.output(16, 0)

    elif txt == "Todo":
        bot.send_message(cid, "[+]TODAS las luces, encendidas")
        print(color.GREEN + "[+]TODAS las luces, encendidas")
        GPIO.output(9, 1)
        GPIO.output(10, 1)
        GPIO.output(16, 1)
        GPIO.output(17, 1)
        GPIO.output(20, 1)
        GPIO.output(21, 1)
        GPIO.output(22, 1)
        GPIO.output(27, 1)
    elif txt == "Todo off":
        bot.send_message(cid, "[+]TODAS las luces, apagadas")
        print(color.RED + "[+]TODAS las luces, apagadas")
        GPIO.output(9, 0)
        GPIO.output(10, 0)
        GPIO.output(16, 0)
        GPIO.output(17, 0)
        GPIO.output(20, 0)
        GPIO.output(21, 0)
        GPIO.output(22, 0)
        GPIO.output(27, 0)

    elif txt == "Atras":
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def sensor_op(m):
    cid = m.chat.id
    txt = m.text

    if txt== "Iniciar":
        previous_state = False
        current_state = False
        cid = m.chat.id
        while True:
            time.sleep(1)
            previous_state = current_state
            current_state = GPIO.input(sensor)
            # print("Current State : %s" % current_state)
            if current_state != previous_state:
                new_state = "HIGH" if current_state else "LOW"
                print("GPIO pin %s is %s" % (sensor, new_state))
                bot.send_message(cid, "Movimiento detectado")

                if new_state == "HIGH":
                    print("Movimiento Detectado")
                    bot.send_chat_action(cid, "upload_photo")
                    foto = "/tmp/" + (time.strftime("%H%M%S-%d%m%y")) + ".jpeg"
                    os.system('fswebcam -d /dev/video0 -r 640x480 --no-banner %s' % foto)
                    bot.send_photo(cid, open(foto, 'rb'))

    elif txt == "Detener":
        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")
        os.execv(sys.executable, ['python'] + sys.argv)
    elif txt == "Atras":
        userStep[cid] = 0
        bot.send_message(cid, "Menu Principal:", reply_markup=menu)
    else:
        command_text(m)

# FILTRAR MENSAJES
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_text(m):
        cid = m.chat.id
        if (m.text.lower() in ['hola', 'hi', 'buenas', 'buenos dias', 'holi', 'hello']):
            bot.send_message(cid, 'Muy buenas, ' + str(m.from_user.first_name) + '. Me alegra verte de nuevo.',
                             parse_mode="Markdown")
        elif (m.text.lower() in ['adios', 'aios', 'adeu', 'ciao']):
            bot.send_message(cid, 'Hasta luego, ' + str(m.from_user.first_name) + '. Te echarÃ© de menos.',
                             parse_mode="Markdown")

print 'Corriendo...'
bot.polling(none_stop=True)
