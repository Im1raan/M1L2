import telebot
from telebot import types
import time
import random

bot = telebot.TeleBot("7867158538:AAGtS4RWri-MpO1PQjGdCvV103ddBDYh0rQ")
user_command = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Таймер")
    btn2 = types.KeyboardButton("Калькулятор")
    btn3 = types.KeyboardButton("Инлайн-кнопки")
    btn4 = types.KeyboardButton("Угадай число")
    btn5 = types.KeyboardButton("Кидание кубика")
    btn7 = types.KeyboardButton("Монетка")
    btn8 = types.KeyboardButton("Случайное число")
    btn9 = types.KeyboardButton("Обратный отсчет")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn7, btn8, btn9)
    bot.send_message(message.chat.id, "Привет! Выберите функцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def menu_handler(message):
    user_id = message.chat.id
    if message.text == "Таймер":
        bot.send_message(user_id, "Введите время в секундах для таймера.")
        user_command[user_id] = "timer"
    elif message.text == "Калькулятор":
        bot.send_message(user_id, "Введите выражение для калькулятора, например: 2+2.")
        user_command[user_id] = "calc"
    elif message.text == "Инлайн-кнопки":
        send_buttons(message)
    elif message.text == "Угадай число":
        guess_number(message)
        user_command[user_id] = "guess"
    elif message.text == "Кидание кубика":
        roll_dice(message)
    elif message.text == "Монетка":
        flip_coin(message)
    elif message.text == "Случайное число":
        bot.send_message(user_id, "Введите диапазон в формате 'начало конец', например: 1 100.")
        user_command[user_id] = "random"
    elif message.text == "Обратный отсчет":
        bot.send_message(user_id, "Введите время в секундах для обратного отсчета.")
        user_command[user_id] = "countdown"
    else:

        if user_id in user_command:
            command = user_command[user_id]
            if command == "timer":
                set_timer(message)
            elif command == "calc":
                calculate(message)
            elif command == "guess":
                check_answer(message)
            elif command == "random":
                random_number(message)
            elif command == "countdown":
                countdown(message)
            user_command.pop(user_id)

def set_timer(message):
    try:
        seconds = int(message.text)
        bot.send_message(message.chat.id, f'Таймер на {seconds} секунд запущен!')
        time.sleep(seconds)
        bot.send_message(message.chat.id, 'Время вышло!')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите целое число.')

def calculate(message):
    try:
        expression = message.text
        result = eval(expression)
        bot.send_message(message.chat.id, f'Результат: {result}')
    except (SyntaxError, NameError):
        bot.send_message(message.chat.id, 'Неверное выражение, попробуйте снова.')

def send_buttons(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Кнопка 1", callback_data="button1")
    btn2 = types.InlineKeyboardButton("Кнопка 2", callback_data="button2")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Нажмите на кнопку:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "button1":
        bot.answer_callback_query(call.id, "Вы нажали Кнопка 1")
    elif call.data == "button2":
        bot.answer_callback_query(call.id, "Вы нажали Кнопка 2")

def guess_number(message):
    global number_to_guess
    number_to_guess = random.randint(1, 10)
    bot.send_message(message.chat.id, "Я загадал число от 1 до 10. Попробуйте угадать, напишите число.")

def check_answer(message):
    try:
        guess = int(message.text)
        if guess == number_to_guess:
            bot.send_message(message.chat.id, 'Поздравляю! Ты угадал!')
        else:
            bot.send_message(message.chat.id, f'Неправильно. Я загадал {number_to_guess}.')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите целое число.')

def roll_dice(message):
    dice = random.randint(1, 6)
    bot.send_message(message.chat.id, f'Ты выкинул {dice}!')

def flip_coin(message):
    result = "Орёл" if random.choice([True, False]) else "Решка"
    bot.send_message(message.chat.id, f'Результат: {result}')

def random_number(message):
    try:
        start, end = map(int, message.text.split())
        number = random.randint(start, end)
        bot.send_message(message.chat.id, f'Случайное число от {start} до {end}: {number}')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите два целых числа, например: 1 100.')

def countdown(message):
    try:
        seconds = int(message.text)
        for i in range(seconds, 0, -1):
            bot.send_message(message.chat.id, f"{i}...")
            time.sleep(1)
        bot.send_message(message.chat.id, "Время вышло!")
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите целое число.')

bot.polling()
