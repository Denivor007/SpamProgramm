import sys
import argparse

from API.Spamer import *


def create_parser_spam():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default=stp.database)
    parser.add_argument('-k', '--key', default='number')
    parser.add_argument('-d', '--delay', default='10')
    parser.add_argument('-m', '--message', default='default')
    parser.add_argument('-st', '--start', default='0')
    parser.add_argument('-rm', '--random_mode', default='1')
    parser.add_argument('-am', '--active_mode', default='1')
    parser.add_argument('-c', '--count', default=sys.maxsize)

    return parser


def create_parser_invite():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default=stp.database)
    parser.add_argument('-k', '--key', default='number')
    parser.add_argument('-d', '--delay', default='1')
    parser.add_argument('-ch', '--channel', default='')
    parser.add_argument('-st', '--start', default='0')
    parser.add_argument('-rm', '--random_mode', default='1')
    parser.add_argument('-am', '--active_mode', default='1')
    parser.add_argument('-c', '--count', default=sys.maxsize)

    return parser


def create_parser_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from_file', default='numbers.csv')
    parser.add_argument('-k', '--key', default='number')
    parser.add_argument('-st', '--start', default='0')
    parser.add_argument('-c', '--count', default=sys.maxsize)

    return parser


if __name__ == "__main__":
    command = sys.argv[1].lower()

    if command == 'help':
        help = sys.argv[2].lower()
        if help == "spam":
            message = "\n'-f' или '--file' задаёт файл, из которого будут браться номера для рассылки. по умлчанию это database из файла setup.py\n'-k' или '--key', если файл задан как csv то этот параметр определяет столбец, по которому беуться номера. по умолчанию \"number\" (в будущем значение по умолчанию будте браться из файла config.txt)"
            message += "\n'-d' или '--delay', задаёт задержку отправки сообщения, по умолчанию 10  (в будущем значение по умолчанию будте браться из файла config.txt)"
            message += "\n'-m' или '--message', сообщение для рассылки. по умолчанию данные из файла \"message.txt\"(в будущем значение по умолчанию будте браться из файла config.txt)"
            message += "\n'-st' или '--start', номер человека в файле, по умолчанию \"0\", т.е. первый (в будущем значение по умолчанию будте браться из файла config.txt)"
            message += "\n'-c' или '--count', количество номеров для обработки, по умолчанию это максимум."

            print(message)
        elif help == 'invite':
            message = "\n'-f' или '--file' задаёт файл, из которого будут браться номера для добавления в канал. по умочанию это database из файла setup.py"
            message += "\n'-k' или '--key', если файл задан как csv то этот параметр определяет столбец, по которому беруться номера. по умолчанию \"number\" (в будущем значение по умолчанию будте браться из файла config.txt)"
            message += "\n'-d' или '--delay', задаёт задержку отправки сообщения, по умолчанию 10  (в будущем значение по умолчанию будте браться из файла config.txt)"
            message += "\n'-ch' или '--channel' канал для подписки. значения по умолчанию нет"
            message += "\n'-st' или '--start', номер человека в файле, по умолчанию \"0\", т.е. первый (в будущем значение по умолчанию будте браться из файла config.txt)"
            message += "\n'-c' или '--count', количество номеров для обработки, по умолчанию это максимум."
            print(message)

    if command == 'fill':
        with client:
            client.loop.run_until_complete(fill_user_id())

    if command == 'parse':
        parser = create_parser_parse()
        namespace = parser.parse_args(sys.argv[2:])
        numbers = get_number_list(namespace.from_file, namespace.key)
        count = db.add_numbers(numbers)
        print(f"added {count} new records to the database")
        with client:
            client.loop.run_until_complete(fill_user_id())

    if command == 'invite':
        parser = create_parser_invite()
        namespace = parser.parse_args(sys.argv[2:])
        with client:
            kwargs = {"file": namespace.file,
                      "key": namespace.key,
                      "channel": namespace.channel,
                      "start": int(namespace.start),
                      "count": int(namespace.count),
                      "delay": int(namespace.delay),
                      "random_mode_": bool(int(namespace.random_mode)),
                      "only_active_mode_": bool(int(namespace.active_mode)),
                      }
            client.loop.run_until_complete(work_with_contact('invite', **kwargs))

    if command == 'spam':
        parser = create_parser_spam()
        namespace = parser.parse_args(sys.argv[2:])
        with client:
            kwargs = {"file": namespace.file,
                      "key": namespace.key,
                      "message": namespace.message,
                      "start": int(namespace.start),
                      "count": int(namespace.count),
                      "delay": int(namespace.delay),
                      "random_mode_": bool(int(namespace.random_mode)),
                      "only_active_mode_": bool(int(namespace.active_mode)),
                      }
            client.loop.run_until_complete(work_with_contact('spam',**kwargs))





#
# async def main():
#
#     # ...to your contacts
#     await client.send_message('+380990712878', 'Hello, friend!')
#     # ...or even to any username
#     await client.send_message('@A_depressant', 'Testing Telethon!')
#
#     # You can, of course, use markdown in your messages:
#     message = await client.send_message(
#         'me',
#         'This message has **bold**, `code`, __italics__ and '
#         'a [nice website](https://example.com)!',
#         link_preview=False
#     )
#
#     # You can reply to messages directly if you have a message object
#     await message.reply('Cool!')
#
    # You can print the message history of any chat: