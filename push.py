import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import sqlite3
import telegram
from datetime import datetime
import asyncio
import pytz
import sys

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

token = os.environ.get('TOKEN')
chat_id = os.environ.get('CHAT_ID')
db = os.getenv('DATABASE')

audio_id = sys.argv[1]
audio_label = sys.argv[2]


patient = json.load(open("data/patients.json"))[1]
message = f"Name: {patient['name']}, Room: { patient['room'] }, Reason: {audio_label}"


eastern = pytz.timezone('US/Eastern')
adapt_datetime = lambda ts: ts.astimezone(eastern).strftime('%Y-%m-%d %H:%M:%S')
convert_datetime = lambda ts_str: datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S').astimezone(pytz.utc)

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)


async def send(msg, chat_id, token):
    bot = telegram.Bot(token=token)
    message = await bot.send_message(chat_id=chat_id, text=msg)
    timestamp = datetime.now()

    with sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO patients (patient_name, room_number, audio_id, audio_label, send_timestamp, message_id) VALUES (?, ?, ?, ?)''',
                  (patient['name'], patient['room'], audio_id, audio_label, timestamp, message.message_id))
        conn.commit()

    return message.message_id

async def check_replies(bot, message_id, chat_id):
    last_update_id = None

    while True:
        offset = last_update_id + 1 if last_update_id is not None else None
        updates = await bot.get_updates(offset=offset, timeout=10)

        for update in updates:
            last_update_id = update.update_id

            if update.message and update.message.reply_to_message and update.message.reply_to_message.message_id == message_id:
                reply = update.message
                user = reply.from_user
                reply_timestamp = reply.date

                user_mapping = json.load(open('data/doctors.json'))
                get_name = lambda user_id: user_mapping.get(user_id, "John Doe")


                with sqlite3.connect(db) as conn:
                    c = conn.cursor()
                    c.execute("UPDATE patients SET reply_timestamp = ?, attending_person_name = ? WHERE message_id = ?", (reply_timestamp, get_name(user.username), message_id))
                    conn.commit()
                print(f"User {user.username} replied to the message at {reply_timestamp}. Reply: {reply.text}")
                exit()

        await asyncio.sleep(1)

async def main():
    bot = telegram.Bot(token=token)
    message_id = await send(message, chat_id, token)
    await check_replies(bot, message_id, chat_id)

asyncio.run(main())