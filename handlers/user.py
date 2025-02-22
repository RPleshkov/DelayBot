from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fsm.states import FSMSendMessage

router = Router()


@router.message(CommandStart())
async def cmd_start_process(msg: Message):
    await msg.answer(
        text="Привет! Воспользуйся командой /send для демонстрации отложенных сообщений"
    )


@router.message(Command("send"))
async def cmd_send_process(msg: Message, state: FSMContext):
    await msg.answer(
        text="Пришли сообщение для отложенной отправки.",
    )
    await state.set_state(FSMSendMessage.SEND)


@router.message(StateFilter(FSMSendMessage.SEND), F.text)
async def get_message(msg: Message, state: FSMContext):
    pass
