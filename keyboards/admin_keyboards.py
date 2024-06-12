from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_find = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Найти покупателя')]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

kb_transaction = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Списать баллы')],
                                               [KeyboardButton(text='Начислить баллы')],
                                               [KeyboardButton(text='Отменить операцию')]],
                                     resize_keyboard=True,
                                     one_time_keyboard=True)

kb_bool = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')],
                                        [KeyboardButton(text='Нет')]],
                              resize_keyboard=True,
                              one_time_keyboard=True)

ib_bool = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Да', callback_data='yes_answer')],
                     [InlineKeyboardButton(text='Нет', callback_data='no_answer')]])

ib_admin = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Дать админку', callback_data='get_admin')],
                     [InlineKeyboardButton(text='Отмена', callback_data='cancel')]])

ib_not_admin = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Лишить админки', callback_data='no_admin')],
                     [InlineKeyboardButton(text='Отмена', callback_data='cancel')]])

ib_bonus = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Изменить количество бонусов', callback_data='set_bonus')],
                     [InlineKeyboardButton(text='Отмена', callback_data='cancel')]])

ib_picture = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data='cancel')]])

ib_text = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Отправить', callback_data='set_text')],
                     [InlineKeyboardButton(text='Выйти', callback_data='cancel')]])

ib_root = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Разослать сообщение', callback_data='send_msg')],
                     [InlineKeyboardButton(text='Админка', callback_data='admin')],
                     [InlineKeyboardButton(text='Накинуть бонусов', callback_data='bonus')],
                     [InlineKeyboardButton(text='Выйти', callback_data='exit')]])

kb_cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отменить операцию')]],
                                resize_keyboard=True,
                                one_time_keyboard=True)
