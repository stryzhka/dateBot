from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

available_sex = ['мальчик :)', 'девочка :(', 'няшка ^_^']
profile_kb = ['изменить анкету', 'сохранить анкету']
static_kb = ['смотреть анкеты', 'моя анкета', "симпатии"]
profile_kb1 = ['изменить анкету', 'вкл выкл анкету', 'вернуться в меню']
start_kb = ['создать анкету']
watching_kb = ['+', '-', 'вернуться в меню', 'жалоба']
got_match_kb = ["<3", "фу"]
admin_kb = ["сообщение всем пользователям", "жалобы", "черный список", "вернуться в меню"]
banlist_kb = ["далее", "выйти"]
def make_keyboard(items: list[str]) -> types.ReplyKeyboardMarkup:
    #row = [KeyboardButton(text=item) for item in items]
    kb = [[]]
    for item in items:
        kb[0].append(types.KeyboardButton(text=item))
    #print(types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
#a = make_keyboard(available_sex)