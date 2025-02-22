from nats.js.client import JetStreamContext
from datetime import datetime
from uuid import uuid4


async def delay_send_message(
    js: JetStreamContext,
    chat_id: int,
    message_id: int,
    subject: str,
    delay: int = 0,
) -> None:
    headers = {
        "ID": str(uuid4()),
        "Tg-Delayed-Chat-ID": str(chat_id),
        "Tg-Delayed-Msg-ID": str(message_id),
        "Tg-Delayed-Msg-Timestamp": str(datetime.now().timestamp()),
        "Tg-Delayed-Msg-Delay": str(delay),
    }
    await js.publish(subject=subject, headers=headers)
