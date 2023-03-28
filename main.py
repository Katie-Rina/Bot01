import json

import telebot
token = '6205132405:AAHQkHhIcmx9j6frjRd_1mseV7qdqUCCBzw'

bot = telebot.TeleBot(token)

with open('day.json', 'r', encoding='utf-8') as file:
    dict_day = json.load(file)


    @bot.message_handler(commands=['start'])
    def welcome(message):

        bot.send_message(message.chat.id, "Добро пожаловать! Я определю день недели по числу и месяцу в 2023 году")
        bot.send_message(message.chat.id, "Введите месяц (число от 1 до 12): ")
        bot.register_next_step_handler(message, month)

    @bot.message_handler(commands=['text'])
    def month(message):
        global m
        m = message.text
        # print(m)
        if int(m) < 1 or int(m) > 12:
            bot.send_message(message.chat.id, 'Месяцев всего 12!! Попробуйте ещё раз: ')
            bot.register_next_step_handler(message, month)
        else:
            global m_code
            if m == '1' or m == '10':
                m_code = 6
            elif m == '5':
                m_code = 0
            elif m == '8':
                m_code = 1
            elif m == '2' or m == '3' or m == '11':
                m_code = 2
            elif m == '6':
                m_code = 3
            elif m == '9' or m == '12':
                m_code = 4
            elif m == '4' or m == '7':
                m_code = 5
            bot.send_message(message.chat.id, 'Введите день (число от 1 до 31): ')
            bot.register_next_step_handler(message, day)

    @bot.message_handler(commands=['text'])
    def day(message):
        global d
        d = message.text
        # print(d)
        if int(d) < 1 or int(d) > 31:
            bot.send_message(message.chat.id, 'Нет такого числа в кадендаре!! Попробуйте ещё раз: ')
            bot.register_next_step_handler(message, day)
        elif d == '31' and (m == '2' or m == '4' or m == '6' or m == '9' or m == '11') or m == '2' and (d == '30' or d == '29'):

            bot.send_message(message.chat.id, 'Нет такого числа в этом месяце. Попробуйте ещё: ')
            bot.register_next_step_handler(message, day)
        else:
            dw = (int(d) + m_code) % 7
            # print(int(d))
            # print(m_code)
            # print(dw)
            bot.send_message(message.chat.id, dict_day[str(dw)])
            bot.send_message(message.chat.id, "Ещё? (да / нет)")
            bot.register_next_step_handler(message, loop)

    @bot.message_handler(commands=['text'])
    def loop(message):
        if message.text.lower() == 'да' or message.text.lower() == 'Да':
            bot.send_message(message.chat.id, "Введите месяц (число от 1 до 12): ")
            bot.register_next_step_handler(message, month)
        elif message.text.lower() == 'нет' or message.text.lower() == 'Нет':
            bot.send_message(message.chat.id, "Пока!")
            bot.stop_polling()
        else:
            bot.send_message(message.chat.id, 'Не понимаю Вас. Пожалуйста, напишите "да" или "нет"')
            bot.register_next_step_handler(message, loop)

bot.polling(none_stop=True)

