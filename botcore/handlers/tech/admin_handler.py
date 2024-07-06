from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from botcore.states.state import Tech
from config import BOT_TOKEN
from models.chat import Chat
from models.setting import Setting

router = Router()


@router.message(F.text.lower() == "кнопки")
async def tech_handler(msg: types.Message):
    builder = InlineKeyboardBuilder([[
        types.InlineKeyboardButton(
            text='/start', callback_data=f"button_edit_start"
        )
    ], [
        types.InlineKeyboardButton(
            text='Тех поддержка', callback_data=f"button_edit_tech"
        )
    ]])
    await msg.answer('для редактирования ответа кнопок нажмите на кнопку ниже', reply_markup=builder.as_markup())


@router.callback_query(F.data.regexp(r"button_edit_\w+"))
async def button_edit_handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        name = callback.data.split("_")[2]
    except:
        return await callback.message.answer(
            f"Кнопка не найдена"
        )

    await state.update_data({'button_name': name})
    await callback.message.answer('Отправьте текст для ответа кнопки')
    await state.set_state(Tech.get_button_text)
    await callback.answer()


@router.message(Tech.get_button_text)
async def send_message_handler(msg: types.Message, state: FSMContext, session):
    state_data = await state.get_data()
    setting = session.get(Setting, 1)

    photo = None
    text = msg.text

    if msg.photo:
        photo = msg.photo[-1].file_id
        text = msg.caption

    if not setting:
        session.add(Setting())
        session.commit()
        setting = session.get(Setting, 1)
    print(photo)
    setattr(setting, state_data['button_name'], text)
    setattr(setting, state_data['button_name'] + "_photo", photo)
    session.commit()

    await msg.answer('Ответ кнопки изменен')
    await state.update_data({})
    await state.clear()


@router.callback_query(F.data.regexp(r"block_\d+"))
async def block_handler(callback: types.CallbackQuery, session):
    try:
        chat_id = int(callback.data.split("_")[1])
    except:
        return await callback.message.answer(
            f"Пользователь не найден"
        )

    chat = session.query(Chat).filter_by(chat_id=chat_id).first()
    chat.block = True
    session.commit

    await send_message(chat_id, 'Вы заблокированы')
    await callback.message.answer('Пользователь заблокирован')


@router.callback_query(F.data.regexp(r"answer_\d+"))
async def get_support_message_handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        data = callback.data.split("_")
        chat_id = int(data[1])
    except:
        return await callback.message.answer(
            f"Пользователь не найден"
        )

    await state.update_data({'chat_id': chat_id})
    await callback.message.answer('Отправьте сообщение пользователю. Это может быть любой текст, картинка, документ')
    await state.set_state(Tech.get_support_message)
    await callback.answer()


@router.message(Tech.get_support_message)
async def send_message_handler(msg: types.Message, state: FSMContext):
    state_data = await state.get_data()
    text = msg.text
    photo = None
    if msg.photo:
        photo = msg.photo[-1]
    document = msg.document
    if photo or document:
        text = msg.caption

    await send_message(state_data['chat_id'], text, photo, document)
    await msg.answer('Сообщение отправлено, для нового сообщения снова нажмите на кнопку')
    await state.update_data({})
    await state.clear()


async def send_message(chat_id, text, photo=None, document=None):
    try:
        bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

        if photo:
            await bot.send_photo(chat_id, photo.file_id, caption=text)
        elif document:
            await bot.send_document(chat_id, document.file_id, caption=text)
        else:
            await bot.send_message(chat_id, text)

        s = await bot.get_session()

        await s.close()
    except:
        pass
