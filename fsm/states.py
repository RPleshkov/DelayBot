from aiogram.fsm.state import StatesGroup, State


class FSMSendMessage(StatesGroup):
    SEND = State()
