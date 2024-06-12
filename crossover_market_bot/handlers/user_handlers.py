from aiogram.filters.command import Command
from aiogram import types, Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from pybots.user_bot import insert_user, insert_phone_numbers, insert_birthday, create_card, select_card_information, \
    check_users
from keyboards import user_keyboards, admin_keyboards
from state.user_state import Registration
from state.admin_state import AdminState
from pybots.admin_bot import select_user, update_bonus, check_ttl_gift_bonus, check_super_adm, super_find_user, \
    select_all_users
from crossover import user_bot
import re
from datetime import datetime
import time

router = Router()


@router.message(Command("start"))
async def user_start(message: types.Message):
    user_inf = check_users(message.from_user.id)
    if user_inf[0]:
        if not user_inf[1]:
            await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=user_keyboards.kb_information)
        else:
            await message.answer(f"Привет {message.from_user.full_name}!\n"
                                 f"Ты имеешь права администратора!", reply_markup=admin_keyboards.kb_find)
    else:
        await message.answer(
            f"Привет, {message.from_user.full_name}, я не нашел тебя у нас в системе, не хочешь зарегистрироваться, "
            f"чтобы получить доступ к бонусной системе?",
            reply_markup=user_keyboards.kb_reg)


@router.message(Command('root'))
async def adm_add_bonus(message: types.Message):
    if check_super_adm(message.from_user.id):
        await message.answer('😎Вы имеете права супер администатора!\n'
                             'Выбери операцию',
                             reply_markup=admin_keyboards.ib_root)


@router.callback_query(F.data == 'admin')
async def reg_user(message: types.Message, state: FSMContext):
    await user_bot.send_message(chat_id=message.from_user.id,
                                text='🔎  Введи номер телефона или карты, кому дать права администратора')
    await state.set_state(AdminState.get_admin)


@router.message(AdminState.get_admin)
async def admin_start2(message: types.Message, state: FSMContext):
    await state.update_data(admin=message.text)
    num = await state.get_data()
    try:
        info = select_user(num['admin'])
        gift_bonus, string = check_ttl_gift_bonus(info[5], info[6])
        roles = '👤<b>Является администратором:</b> ✅\n' if info[8] else ''
        msg = f'<i>Информация о пользователе:</i>\n\n' \
              f'👤<b>Имя:</b> {info[0]}\n' \
              f'👤<b>Дата рождения:</b> {datetime.strftime(info[7], "%d.%m.%Y")}\n' \
              f'{roles}' \
              f'📱<b>Номер телефона:</b> {info[1]}\n\n' \
              f'💳<b>Номер карты:</b> {info[2]}\n\n' \
              f'🤑<b>Баланс:</b> {"%.2f" % (float(info[3] + gift_bonus))} баллов\n' \
              f'{string}\n'
        if info[8]:
            await message.answer(text=msg, parse_mode='HTML', reply_markup=admin_keyboards.ib_not_admin)
        else:
            await message.answer(text=msg, parse_mode='HTML', reply_markup=admin_keyboards.ib_admin)

        await state.update_data(admin=info)
    except Exception:
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text='❗️Пользователь не найден или неверно введен номер телефона/карты',
                                    reply_markup=admin_keyboards.ib_root)


@router.callback_query(F.data == 'get_admin')
async def reg_user(message: types.Message, state: FSMContext):
    try:
        value = await state.get_data()
        name = value['admin'][0]
        super_find_user(value['admin'][4], True)
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text=f'❗️Пользователь {name} получил права администратора!',
                                    reply_markup=admin_keyboards.ib_root)
    except Exception:
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text='❗️Операция отменена!', reply_markup=admin_keyboards.ib_root)


@router.callback_query(F.data == 'no_admin')
async def reg_user(message: types.Message, state: FSMContext):
    try:
        value = await state.get_data()
        name = value['admin'][0]
        super_find_user(value['admin'][4], False)
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text=f'❗️Пользователь {name} лишился прав администратора!',
                                    reply_markup=admin_keyboards.ib_root)
    except Exception:
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text='❗️Операция отменена!', reply_markup=admin_keyboards.ib_root)


@router.callback_query(F.data == 'bonus')
async def reg_user(message: types.Message, state: FSMContext):
    await user_bot.send_message(chat_id=message.from_user.id,
                                text='🔎  Введи номер телефона или карты, кому изменить количество бонусов')
    await state.set_state(AdminState.bonus)


@router.message(AdminState.bonus)
async def admin_start2(message: types.Message, state: FSMContext):
    await state.update_data(bonus=message.text)
    num = await state.get_data()
    try:
        info = select_user(num['bonus'])
        gift_bonus, string = check_ttl_gift_bonus(info[5], info[6])
        await message.answer(f'<i>Информация о пользователе:</i>\n\n'
                             f'👤<b>Имя:</b> {info[0]}\n'
                             f'👤<b>Дата рождения:</b> {datetime.strftime(info[7], "%d.%m.%Y")}\n\n'
                             f'📱<b>Номер телефона:</b> {info[1]}\n\n'
                             f'💳<b>Номер карты:</b> {info[2]}\n\n'
                             f'🤑<b>Баланс:</b> {"%.2f" % float(info[3])} баллов\n'
                             f'{string}\n',
                             parse_mode='HTML',
                             reply_markup=admin_keyboards.ib_bonus)
        await state.update_data(bonus=info)
    except Exception:
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text='❗️Пользователь не найден или неверно введен номер телефона/карты!',
                                    reply_markup=admin_keyboards.ib_root)


@router.callback_query(F.data == 'set_bonus')
async def reg_user(message: types.Message, state: FSMContext):
    await user_bot.send_message(chat_id=message.from_user.id, text='❗️Введи новое количество бонусов!')
    await state.set_state(AdminState.set_bonus)


@router.message(AdminState.set_bonus)
async def admin_start2(message: types.Message, state: FSMContext):
    try:
        bonus = message.text
        assert bonus.isdigit()
        value = await state.get_data()
        gift_bonus = value['bonus'][5] if value['bonus'][5] else 0
        card = value['bonus'][2]
        update_bonus(bonus, gift_bonus, card)
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text='❗️Количество бонусов обновлено!', reply_markup=admin_keyboards.ib_root)
    except Exception:
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text='❗️Данные введены неверно!', reply_markup=admin_keyboards.ib_root)


@router.callback_query(F.data == 'send_msg')
async def reg_user(message: types.Message, state: FSMContext):
    await user_bot.send_message(chat_id=message.from_user.id,
                                text='🏞  Отправь мне картинку и текст под ней!\n'
                                     '        Если картинки нет, то отправь только текст',
                                reply_markup=admin_keyboards.ib_picture)
    await state.set_state(AdminState.picture)


@router.message(AdminState.picture)
async def admin_start2(message: types.Message, state: FSMContext):
    # users = select_all_users()
    try:
        pic = message.photo[-1].file_id
        msg = message.caption
        # for user_tlgm_id in users:
        await user_bot.send_photo(chat_id=message.from_user.id,
                                  photo=pic,
                                  caption=msg)
    except Exception:
        msg = message.text
        # for user_tlgm_id in users:
        await user_bot.send_message(chat_id=message.from_user.id,
                                    text=msg)
    await user_bot.send_message(chat_id=message.from_user.id,
                                text='❗️Сообщение всем отправлено!',
                                reply_markup=admin_keyboards.ib_root)
    await state.set_state(AdminState._pass)


@router.callback_query(F.data == 'cancel')
async def reg_user(message: types.Message):
    await user_bot.send_message(chat_id=message.from_user.id,
                                text='❗️Операция отменена!', reply_markup=admin_keyboards.ib_root)


@router.callback_query(F.data == 'exit')
async def reg_user(message: types.Message, state: FSMContext):
    await user_bot.send_message(chat_id=message.from_user.id,
                                text='❗️Пока!', reply_markup=admin_keyboards.kb_find)
    await state.set_state(AdminState._pass)


@router.message(F.text == 'Зарегистрироваться')
async def reg_user(message: types.Message, state: FSMContext):
    if insert_user(message.from_user.id, message.from_user.full_name):
        await message.answer('Давай начнем регистрацию.\n'
                             'Для начала поделись своим номером телефона\n'
                             'В формате <i>89123456789</i>',
                             parse_mode='HTML',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.phone)


@router.message(Registration.phone)
async def reg_user(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    num_phone = await state.get_data()
    if re.search('^((8)+([0-9]){10})$', num_phone['phone']):
        if insert_phone_numbers(num_phone['phone'], message.from_user.id):
            await message.answer(
                'Следующий шаг.\n'
                'Введи дату рождения, чтобы получать поздравительные баллы в этот день.\n'
                'В формате <i>дд.мм.гггг</i>',
                parse_mode='HTML',
                reply_markup=ReplyKeyboardRemove())
            await state.set_state(Registration.bd)
    else:
        await message.answer('❗️Неверный формат, попробуй еще раз (<i>89123456789</i>)',
                             parse_mode='HTML',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.phone)


@router.message(Registration.bd)
async def reg_user(message: types.Message, state: FSMContext):
    await state.update_data(bd=message.text)
    birthday = await state.get_data()
    try:
        if time.strptime(birthday['bd'], '%d.%m.%Y'):
            dt = datetime.strptime(birthday['bd'], '%d.%m.%Y')
            if insert_birthday(str(datetime.strftime(dt, '%Y-%m-%d')), message.from_user.id):
                create_card(message.from_user.id)
                await message.answer('Добро пожаловать в бонусную программу Crossover Market!',
                                     reply_markup=user_keyboards.kb_information)
                await state.set_state(Registration._pass)
    except Exception:
        await message.answer('❗️Неверный формат, попробуй еще раз (<i>дд.мм.гггг</i>)',
                             parse_mode='HTML',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(Registration.bd)


@router.message(F.text == 'Информация о бонусном счете')
async def reg_user(message: types.Message):
    inf = select_card_information(message.from_user.id)
    gift_bonus, string = check_ttl_gift_bonus(inf[2], inf[3])
    await message.answer(f'💳<b>Номер карты:</b> {inf[0]}\n\n'
                         f'🤑<b>Ваш баланс:</b> {"%.2f" % (float(inf[1] + gift_bonus))} баллов\n'
                         f'{string}\n'
                         f'<i>Информация по покупке:\n'
                         f'1 балл = 1 рубль\n'
                         f'Списать можно 10% от стоимости товара.</i>',
                         parse_mode='HTML',
                         reply_markup=user_keyboards.kb_information)


@router.message(F.text == 'Основной канал и акции')
async def question_user(message: types.Message):
    await message.answer('Вы можете узнать наличие товара\n'
                         'или посмотреть бонусные акции',
                         reply_markup=user_keyboards.ib_channel)


@router.message(F.text == 'Найти покупателя')
async def admin_start1(message: types.Message, state: FSMContext):
    await message.answer('🔎  Для поиска введи номер телефона или карты', reply_markup=admin_keyboards.kb_cancel)
    await state.set_state(AdminState.number)


@router.message(AdminState.number)
async def admin_start2(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    num = await state.get_data()
    try:
        info = select_user(num['number'])
        gift_bonus, string = check_ttl_gift_bonus(info[5], info[6])
        await message.answer(f'<i>Информация о покупателе:</i>\n\n'
                             f'👤<b>Имя:</b> {info[0]}\n'
                             f'👤<b>Дата рождения:</b> {datetime.strftime(info[7], "%d.%m.%Y")}\n\n'
                             f'📱<b>Номер телефона:</b> {info[1]}\n\n'
                             f'💳<b>Номер карты:</b> {info[2]}\n\n'
                             f'🤑<b>Баланс:</b> {"%.2f" % (float(info[3] + gift_bonus))} баллов\n'
                             f'{string}\n'
                             f'<i>Информация о покупке:\n'
                             f'1 балл = 1 рубль\n'
                             f'Списать можно 10% от стоимости товара,\n'
                             f'либо начислисть 5% от стоимости товара.</i>',
                             parse_mode='HTML',
                             reply_markup=admin_keyboards.kb_transaction)
        await state.update_data(number=info)
        await state.set_state(AdminState._pass)
    except Exception:
        await message.answer('❗️Пользователь не найден или неверно введен номер телефона/карты',
                             reply_markup=admin_keyboards.kb_find)
        await state.set_state(AdminState._pass)


@router.message(F.text == 'Списать баллы')
async def admin_start3(message: types.Message, state: FSMContext):
    try:
        value = await state.get_data()
        bonus = float(value['number'][3])
        gift_bonus = float(value['number'][5])
        assert (bonus + gift_bonus)
        await message.answer('Введи стоимость покупки')
    except Exception:
        await message.answer('❗️Баллов нет!', reply_markup=admin_keyboards.kb_find)
    await state.set_state(AdminState.minus)


@router.message(AdminState.minus)
async def admin_start4(message: types.Message, state: FSMContext):
    try:
        full_cost = float(message.text)
        percentage = full_cost * 0.1
        value = await state.get_data()
        bonus = float(value['number'][3])
        gift_bonus, string = check_ttl_gift_bonus(gift_bonus=value['number'][5], ttl_gb=value['number'][6])
        check_ttl = True if string else False
        all_bonus = bonus + gift_bonus
        if percentage < all_bonus:
            new_cost = full_cost - percentage
            difference = abs(percentage - gift_bonus)
            if bonus > gift_bonus:
                new_bonus = bonus - difference
                new_gift_bonus = 0
                string = f'Будет списано: <b>{"%.2f" % percentage}</b> баллов'
            else:
                new_bonus = bonus
                new_gift_bonus = difference
                string = f'Будет списано: <b>{"%.2f" % percentage}</b> подарочных баллов!'
        else:
            new_cost = full_cost - all_bonus
            new_bonus = 0
            new_gift_bonus = 0
            string = f'Будет списано баллов:   <b>{"%.2f" % all_bonus}</b>'
        await state.update_data(adm=message.from_user.id)
        await state.update_data(new_bonus=new_bonus)
        await state.update_data(new_gift_bonus=new_gift_bonus)
        await state.update_data(check_ttl=check_ttl)
        await message.answer(text=f'Новая цена покупки: <b>{"%.2f" % new_cost}</b>\n'
                                  f'{string}\n\n'
                                  f'❗️Ожидайте подтверждения покупателя!',
                             parse_mode='HTML')
        await user_bot.send_message(chat_id=value['number'][4],
                                    text=f'Новая цена покупки:   <b>{"%.2f" % new_cost}</b>\n'
                                         f'{string}\n\n'
                                         f'❗️Подтвердить списание?',
                                    parse_mode='HTML',
                                    reply_markup=admin_keyboards.kb_bool)
        await state.set_state(AdminState._pass)
    except Exception:
        await message.answer('❗️Неверно введена стоимость покупки', reply_markup=admin_keyboards.kb_find)
        await state.set_state(AdminState._pass)


@router.message(F.text == 'Да')
async def admin_start5(message: types.Message, state: FSMContext):
    value = await state.get_data()
    adm_id = value['adm']
    bonus = value['new_bonus']
    gift_bonus = value['new_gift_bonus']
    card = value['number'][2]
    check_ttl = value['check_ttl']
    ttl_gb = value['number'][6]
    string = f'\n❗️Успейте потратить бонусные баллы до ' \
             f'<b>{datetime.strftime(ttl_gb, "%d.%m.%Y")}</b>!\n' if check_ttl else ''
    update_bonus(bonus, gift_bonus, card)
    await message.answer(f'❗️Баллы успешно списаны!'
                         f'{string}',
                         parse_mode='HTML',
                         reply_markup=user_keyboards.kb_information)
    await user_bot.send_message(chat_id=adm_id,
                                text='❗️Баллы успешно списаны!', reply_markup=admin_keyboards.kb_find)
    await state.set_state(AdminState._pass)


@router.message(F.text == 'Нет')
async def admin_start6(message: types.Message, state: FSMContext):
    value = await state.get_data()
    adm_id = value['adm']
    await message.answer('❗️Операция отменена!', reply_markup=user_keyboards.kb_information)
    await user_bot.send_message(chat_id=adm_id, text='❗️Операция отменена!', reply_markup=admin_keyboards.kb_find)
    await state.set_state(AdminState._pass)


@router.message(F.text == 'Начислить баллы')
async def admin_start7(message: types.Message, state: FSMContext):
    await message.answer('Введи стоимость покупки')
    await state.set_state(AdminState.add)


@router.message(F.text == 'Отменить операцию')
async def admin_start7(message: types.Message, state: FSMContext):
    await message.answer(f'❗️Операция отменена!', reply_markup=admin_keyboards.kb_find)
    await state.set_state(AdminState._pass)


@router.message(AdminState.add)
async def admin_start8(message: types.Message, state: FSMContext):
    cost = float(message.text)
    percentage = cost * 0.05
    value = await state.get_data()
    card = value['number'][2]
    bonus = float(value['number'][3])
    gift_bonus, string = check_ttl_gift_bonus(gift_bonus=value['number'][5], ttl_gb=value['number'][6])
    new_bonus = bonus + percentage
    update_bonus(new_bonus, gift_bonus, card)
    await user_bot.send_message(chat_id=value['number'][4],
                                text=f'❗️{"%.2f" % (new_bonus - bonus)} '
                                     f'баллов успешно добавлены на Ваш бонусный счет!\n\n'
                                     f'🤑Балланс: {new_bonus + gift_bonus} баллов.\n\n'
                                     f'{string}\n',
                                parse_mode='HTML',
                                reply_markup=user_keyboards.kb_information)
    await message.answer(f'❗️{"%.2f" % (new_bonus - bonus)} баллов успешно добавлены покупателю {value["number"][0]}!',
                         reply_markup=admin_keyboards.kb_find)
    await state.set_state(AdminState._pass)
