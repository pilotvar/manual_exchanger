from sqlalchemy import select

from db import session
from models.chat import Chat


def get_chat_db(chat_id):
    return session.query(Chat).filter_by(chat_id=chat_id).first()


def update_chat(chat):
    chat_db = get_chat_db(chat.id)
    full_name = chat.first_name + " " + (chat.last_name or "")

    if chat_db is None:
        chat_db = Chat(
            chat_id=chat.id,
            user_name=chat.username,
            full_name=full_name,
        )
        session.add(chat_db)
        session.commit()
    else:
        if chat_db.user_name != chat.username or chat_db.full_name != full_name:
            chat_db.user_name = chat.username
            chat_db.full_name = full_name
            session.commit()

    session.refresh(chat_db)
    return chat_db
