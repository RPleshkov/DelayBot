from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from nats.js import JetStreamContext
from fsm.states import FSMSendMessage
from services.delay_service.publisher import delay_send_message


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


@router.message(StateFilter(FSMSendMessage.SEND))
async def get_message(
    msg: Message,
    state: FSMContext,
    js: JetStreamContext,
    delay_subject: str,
):

    delay = 5

    await delay_send_message(
        js=js,
        chat_id=msg.chat.id,
        message_id=msg.message_id,
        subject=delay_subject,
        delay=delay,
    )

    await state.clear()
