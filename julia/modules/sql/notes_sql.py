#    MissJuliaRobot (A Telegram Bot Project)
#    Copyright (C) 2019-2021 Julia (https://t.me/MissJulia_Robot)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, in version 3 of the License.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see < https://www.gnu.org/licenses/agpl-3.0.en.html/ >.


from sqlalchemy import Column, UnicodeText, String
from julia.modules.sql import BASE, SESSION


class NOTES(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)

    def __init__(
        self,
        chat_id,
        keyword,
        reply,
    ):
        self.chat_id = chat_id
        self.keyword = keyword
        self.reply = reply


NOTES.__table__.create(checkfirst=True)


def get_notes(chat_id, keyword):
    try:
        return SESSION.query(NOTES).get((str(chat_id), keyword))
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_all_notes(chat_id):
    try:
        return SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id)).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_note(chat_id, keyword, reply):
    adder = SESSION.query(NOTES).get((str(chat_id), keyword))
    if adder:
        adder.reply = reply
    else:
        adder = NOTES(chat_id, keyword, reply)
        adder = NOTES(
            chat_id,
            keyword,
            reply,
        )
    SESSION.add(adder)
    SESSION.commit()


def remove_note(chat_id, keyword):
    saved_note = SESSION.query(NOTES).get((str(chat_id), keyword))
    if saved_note:
        SESSION.delete(saved_note)
        SESSION.commit()


def remove_all_notes(chat_id):
    saved_note = SESSION.query(NOTES).filter(NOTES.chat_id == str(chat_id))
    if saved_note:
        saved_note.delete()
        SESSION.commit()
