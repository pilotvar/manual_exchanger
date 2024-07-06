from aiogram.fsm.state import StatesGroup, State


class AddSupport(StatesGroup):
    get_data = State()


class AddAdmin(StatesGroup):
    get_data = State()


class AddCard(StatesGroup):
    get_data = State()


class SendPayment(StatesGroup):
    get_amount = State()
    get_number = State()


class AddBot(StatesGroup):
    get_data = State()


class AddBotTech(StatesGroup):
    get_data = State()


class SendSuccessWithdrawal(StatesGroup):
    get_data = State()


class Tech(StatesGroup):
    get_data = State()
    get_button_text = State()
    get_img = State()
    get_support_message = State()
    send_messages = State()


class Exchange(StatesGroup):
    get_amount = State()


class Withdrawal(StatesGroup):
    get_amount = State()
    get_wallet = State()


class Client(StatesGroup):
    get_number = State()
    get_comission = State()