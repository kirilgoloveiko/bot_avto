import telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup


bot = telebot.TeleBot("TOKEN")

user_input_dict = {}


class States(StatesGroup):
    marka = State()
    model = State()
    avatar = State()


def starting(chat_id):
    bot.send_message(chat_id, 'Добро пожаловать ✌🏻')
    user_input_dict[chat_id] = {}


@bot.message_handler(commands=['add_car'])
def add_car(message):
    starting(message.chat.id)
    bot.set_state(message.from_user.id, States.marka, message.chat.id)
    bot.send_message(message.chat.id, 'Введите МАРКУ машины (Пример: Audi )')


# @bot.message_handler(state="*", commands=['cancel'])
# def any_state(message):
#     bot.send_message(message.chat.id, "Your state was cancelled.")
#     bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=States.marka)
def get_marka(message):
    bot.send_message(message.chat.id, 'Введите МОДЕЛЬ машины (пример: R8 )')
    bot.set_state(message.from_user.id, States.model, message.chat.id)
    user_input_dict[message.chat.id]['Марка'] = message.text


@bot.message_handler(state=States.model)
def get_avatar(message):
    bot.send_message(message.chat.id, "Выберите картинку для аватарки (ссылку)")
    bot.set_state(message.from_user.id, States.avatar, message.chat.id)
    user_input_dict[message.chat.id]['Модель'] = message.text



@bot.message_handler(state=States.avatar)#, is_digit=True)
def ready_for_answer(message):
    user_input_dict[message.chat.id]['Картинка'] = message.text
    msg = ( f"Марка: <b>{user_input_dict[message.from_user.id]['Марка']}</b>\n"
            f"Модель: <b>{user_input_dict[message.from_user.id]['Модель']}</b>\n"
            f"Картинка: {user_input_dict[message.from_user.id]['Картинка']}")
    print(user_input_dict)
    bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.chat.id, message.chat.id)



bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

print('Ready..')
bot.infinity_polling(skip_pending=True)