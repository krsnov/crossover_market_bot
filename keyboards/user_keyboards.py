from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

kb_reg = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Зарегистрироваться')]],
                             resize_keyboard=True,
                             one_time_keyboard=True)

kb_information = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Информация о бонусном счете')],
                                               [KeyboardButton(text='Основной канал и акции')]
                                               ],
                                     resize_keyboard=True,
                                     one_time_keyboard=True)

ikb1 = InlineKeyboardButton(text='Магазин', url='https://vk.com/crossover_market')
ikb2 = InlineKeyboardButton(text='Задать вопрос', url='https://t.me/m1khalevich')
ikb3 = InlineKeyboardButton(text='Основной канал', url='https://t.me/crossover_market')
ib_channel = InlineKeyboardMarkup(inline_keyboard=[[ikb1, ikb2], [ikb3]])
