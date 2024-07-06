from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from botcore.states.state import Tech
from config import BOT_TOKEN, SUPPORT_CHAT_ID
from models.setting import Setting

router = Router()


@router.message(F.text.lower() == "/start")
async def start_handler(msg: types.Message, state: FSMContext, session):
    await state.clear()
    await state.update_data({})
    kb = [[
        types.KeyboardButton(text="Обменять"),
        types.KeyboardButton(text="Тех поддержка")
    ]]

    if msg.from_user.id == SUPPORT_CHAT_ID:
        kb.append([types.KeyboardButton(text="Кнопки")])

    setting = session.get(Setting, 1)

    if setting and setting.start:
        text = setting.start
        photo = setting.start_photo
    else:
        text = 'Привет'
        photo = None

    await send_message_button_to_support("/start", msg.from_user)
    if photo:
        return await msg.answer_photo(
            photo,
            text,
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=kb, resize_keyboard=True
            )
        )
    return await msg.answer(
        text,
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=kb, resize_keyboard=True
        )
    )


@router.message(F.text.lower() == "обменять")
async def exchnage_handler(msg: types.Message, state: FSMContext, session):
    await state.clear()
    await state.update_data({})
    await send_message_button_to_support("Обменять", msg.from_user)
    await state.set_state(Tech.send_messages)


@router.message(F.text.lower() == "тех поддержка")
async def tech_handler(msg: types.Message, state: FSMContext, session):
    await state.clear()
    await state.update_data({})
    setting = session.get(Setting, 1)

    if setting and setting.tech:
        text = setting.tech
        photo = setting.tech_photo
    else:
        text = 'Тех поддержка'
        photo = None

    await send_message_button_to_support("Тех поддержка", msg.from_user)
    if photo:
        return await msg.answer_photo(str(photo), text)
    return await msg.answer(text)


@router.message(Tech.send_messages)
async def send_messages_handler(msg: types.Message):
    await send_message_to_support(msg)
    await msg.answer("Ваша заявка принята. Нажмите /start что бы начать новую")


def answer_buttons(chat_id):
    return InlineKeyboardBuilder([[
        types.InlineKeyboardButton(
            text='Написать сообщение', callback_data=f"answer_{str(chat_id)}"
        )
    ], [
        types.InlineKeyboardButton(
            text='Заблокировать', callback_data=f"block_{str(chat_id)}"
        )
    ]])


async def send_message_button_to_support(text, from_user):
    try:
        bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
        builder = answer_buttons(from_user.id)
        content = f"Пользователь: {from_user.full_name}\nID: {from_user.id}\n\n"
        content += "Нажал кнопку - " + text
        await bot.send_message(SUPPORT_CHAT_ID, content, reply_markup=builder.as_markup())
        s = await bot.get_session()
        await s.close()
    except:
        pass


async def send_message_to_support(message):
    try:
        bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
        builder = answer_buttons(message.from_user.id)
        content = f"От: {message.from_user.full_name}\nID: {message.from_user.id}\n\n"
        document = message.document
        photos = message.photo

        if message.caption:
            content += message.caption
        elif message.text:
            content += message.text

        if photos:
            await bot.send_photo(SUPPORT_CHAT_ID, photos[-1].file_id, caption=content, reply_markup=builder.as_markup())
        elif document:
            await bot.send_document(SUPPORT_CHAT_ID, document.file_id, caption=content, reply_markup=builder.as_markup())
        else:
            await bot.send_message(SUPPORT_CHAT_ID, content, reply_markup=builder.as_markup())

        s = await bot.get_session()

        await s.close()
    except:
        pass
