import asyncio
import os
import datetime
import random
from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest

from config import setup as stp
from API.Database import Database
from API.Parser import *

client = TelegramClient(stp.session_name, stp.api_id, stp.api_hash)
db = Database(stp.database)


async def fill_user_id():
    users = db.get_users()
    print(users)
    for user in users:
        phone_number = user[0]
        try:
            result = await client(ImportContactsRequest([InputPhoneContact(
                client_id=1,  # любой ид
                phone=phone_number,
                first_name="аккаунт номер",
                last_name=str(user[3]),
            )]))
            user_info = result.users[0]
            print(phone_number, ' - ',user_info.id)
            db.add_user(user[0], user_info.id)
            db.set_active(phone_number, 1)
        except:
            print(phone_number, ' - 0')
            db.set_active(phone_number, 0)

async def work_with_contact(command,
                            file=str,
                            key="number",
                            channel="",
                            message=str,
                            start=0,
                            count=db.get_count(),
                            delay=0,
                            random_mode_ = True,
                            only_active_mode_ = True):
    log_info = ""

    if message == 'default':
        with open(stp.messages_file) as f:
            messages = f.read().split("---")

    users = []
    if file.endswith(".db"):
        print('only_active_mode_ ==',  only_active_mode_)
        users = db.get_users(start, start + count) if not only_active_mode_ else db.get_active_users(start, start + count)

    elif file.endswith(".csv"):
        users = get_number_list(file, key)

    else:
        log_info = f"{file} is incorrect file format. should be .csv or .db"

    for user in users:
        phone_number = user[0] if (file.endswith(".db")) else user
        user_id = user[1] if (file.endswith(".db")) else 0
        delay = random.randint(int(delay//2), int(delay*1.5)) if random_mode_ else delay

        if command == 'invite':
            try:
                await client(functions.channels.InviteToChannelRequest(channel=channel, users=[phone_number]))
                log_info = f"[{datetime.datetime.now()}]- <{user_id}({phone_number})> add to chanel"
                if delay > 0:
                    await asyncio.sleep(delay)
            except:
                log_info = f"[{datetime.datetime.now()}]- <{user_id}({phone_number})> not added to channel or does not exist"

        if command == 'spam':
            message = random.choice(messages)
            try:
                await client.send_message(user[0], message)
                log_info = f"[{datetime.datetime.now()}]- user <{user_id}({phone_number})> got a message: \"{message}\""
                if file.endswith(".db"):
                    db.set_active(phone_number, True)
                if delay > 0:
                    await asyncio.sleep(delay)
            except:
                log_info = f"[{datetime.datetime.now()}]- user <{user_id}({phone_number})> didn't receive message or doesn't exist"
                if file.endswith(".db"):
                    db.set_active(phone_number, False)

        print(log_info)
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(parent_dir, 'log.txt'), 'a') as log_file:
            log_file.write(log_info + "\n")




#функции уже в целом не актуальны.
async def invite(file=str,
                 key="number",
                 channel="",
                 start=0,
                 count=db.get_count(),
                 delay=0,
                 random_mode_ = True,
                 only_active_mode_ = True):

    if file.endswith(".db"):
        users = db.get_users(start, start + count) if not only_active_mode_ else db.get_active_users(start, start + count)

    elif file.endswith(".csv"):
        users = get_number_list(file, key)

    for user in users:
        phone_number = user[0] if (file.endswith(".db")) else user
        delay = random.randint(int(delay//2), int(delay*1.5)) if random_mode_ else delay
        try:
            log_info = f"[{datetime.datetime.now()}]- {phone_number} add to chanel"
            await client(functions.channels.InviteToChannelRequest(channel=channel, users=[phone_number]))
            if delay > 0:
                await asyncio.sleep(delay)
        except:
            log_info = f"[{datetime.datetime.now()}]- {phone_number} not added to channel or does not exist"

        print(log_info)
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(parent_dir, 'log.txt'), 'a') as log_file:
            log_file.write(log_info + "\n")


async def spam(file=str,
               key="number",
               message=str,
               start=0,
               count=db.get_count(),
               delay=0,
               random_mode_=True,
               only_active_mode_=True):

    if message == 'default':
        with open(stp.messages_file) as f:
            messages = f.read().split("---")
    else:
        messages = [message]
    if file.endswith(".db"):
        users = db.get_users(start, start + count) if not only_active_mode_ else db.get_active_users(start, start + count)
        for user in users:
            delay = random.randint(int(delay // 2), int(delay * 1.5)) if random_mode_ else delay
            message = random.choice(messages)
            try:
                await client.send_message(user[0], message)
                log_info = f"[{datetime.datetime.now()}]- user <{user[1]}({user[0]})> got a message: \"{message}\""
                db.set_active(user[0], True)
                if delay > 0:
                    await asyncio.sleep(delay)
            except:
                log_info = f"[{datetime.datetime.now()}]- user <{user[1]}({user[0]})> didn't receive message or doesn't exist"
                db.set_active(user[0], False)
            # следующие 4 строчки предназанчены для логирования. в будующем выведу в отдульную функцию
            print(log_info)
            parent_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(parent_dir, 'log.txt'), 'a') as log_file:
                log_file.write(log_info + "\n")

    elif file.endswith(".csv"):
        numbers = get_number_list(file, key)
        for number in numbers:
            message = random.choice(messages)
            try:
                await client.send_message(number, message)
                # следующие четыре строчки предназанчены для логирования. в будующем выведу в отдульную функцию
                log_info = f"[{datetime.datetime.now()}]- ({number}) got a message: \"{message}\""
                if delay > 0:
                    await asyncio.sleep(delay)
            except:
                log_info = f"[{datetime.datetime.now()}]- ({number}) didn't receive message or doesn't exist"
                db.set_active(number[0], False)
            print(log_info)
            parent_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(parent_dir, 'log.txt'), 'a') as log_file:
                log_file.write(log_info + "\n")
    else:
        print("incorrect file format, should be '.csv' or 'db'")
