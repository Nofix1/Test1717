import asyncio
from io import BytesIO
import regex as re
from aiohttp import ClientSession, FormData
from telethon import TelegramClient, events, types
from telethon.tl import functions
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from config import *
from telebytes import *

# https://t.me/lovec_checkov

client = TelegramClient(session='session', api_id=int(api_id), api_hash=api_hash, system_version="4.16.30-vxSOSYNXA ")

code_regex = re.compile(r"t\.me/(CryptoBot|send|tonRocketBot|CryptoTestnetBot|wallet|xrocket|xJetSwapBot)\?start=(CQ[A-Za-z0-9]{10}|C-[A-Za-z0-9]{10}|t_[A-Za-z0-9]{15}|mci_[A-Za-z0-9]{15}|c_[a-z0-9]{24})", re.IGNORECASE)
url_regex = re.compile(r"https:\/\/t\.me\/\+([\w-]{12,})")
public_regex = re.compile(r"https:\/\/t\.me\/(\w{4,})")

replace_chars = ''' @#&+()*"'…;,!№•—–·±<{>}†★‡„“”«»‚‘’‹›¡¿‽~`|√π÷×§∆\\°^%©®™✓₤$₼€₸₾₶฿₳₥₦₫₿¤₲₩₮¥₽₻₷₱₧£₨¢₠₣₢₺₵₡₹₴₯₰₪'''
translation = str.maketrans('', '', replace_chars)

crypto_black_list = [1622808649, 1559501630, 1985737506, 5014831088, 5794061503]

global is_off
is_off = False
checks_count = 0
checks = []
wallet = []
channels = []
captches = []

async def ocr_space(file: bytes):
    data = FormData()
    data.add_field('isOverlayRequired', 'false')
    data.add_field('apikey', ocr_api_key)
    data.add_field('language', 'eng')
    data.add_field('scale', 'true')
    data.add_field('OCREngine', '2')
    data.add_field('file', file, filename='image.png', content_type='image/png')
    async with ClientSession() as c:
        async with c.post('https://api.ocr.space/parse/image',
            data=data
        ) as r:
            result = await r.json()
    try:
        return result.get('ParsedResults')[0].get('ParsedText').replace(" ", "")
    except:
        return 

async def pay_out():
    global is_off
    while True:
        is_off = True
        await client.send_message('CryptoBot', message=f'/wallet')
        await asyncio.sleep(0.5)
        message = (await client.get_messages('CryptoBot', limit=1))[0]
        text = message.message
        lines = text.split('\n\n')
        for line in lines:
            if ':' in line:
                if 'Доступно' in line:
                    data = line.split('\n')[2].split('Доступно: ')[1].split(' (')[0].split(' ')
                    summ = data[0]
                    curency = data[1]
                else:
                    data = line.split(': ')[1].split(' (')[0].split(' ')
                    summ = data[0]
                    curency = data[1]
                try:
                    if summ == '0':
                        continue
                    result = (await client.inline_query('send', f'{summ} {curency}'))[0]
                    if 'Создать чек' in result.title: 
                        await result.click(avto_vivod_tag)
                except:
                    pass
        await client.send_message('wallet', message=f'/wallet')
        await asyncio.sleep(0.5)
        message = (await client.get_messages('wallet', limit=1))[0]
        text = message.message
        lines = text.split('\n')
        for line in lines:
            if ':' in line and '≈' in line:
                summ = line.split(': ')[1].split(' ≈')[0].split(' ')[0]
                try:
                    result = (await client.inline_query('wallet', f'{summ}'))[0]
                    if 'Создать чек' in result.title:
                        await result.click(avto_vivod_tag)
                except:
                    pass
        await client.send_message('xrocket', message=f'/wallet')
        await asyncio.sleep(0.5)
        for _ in range(3):
            message = (await client.get_messages('xrocket', limit=1))[0]
            text = message.message
            lines = text.split('\n')
            for line in lines:
                if ':' in line and 'удерживается' not in line:
                    data = line.split(': ')[1].split(' (')[0].split(' ')
                    summ = data[0]
                    curency = data[1]
                    try:
                        if summ == '0':
                            continue
                        result = (await client.inline_query('xrocket', f'{summ} {curency}'))[0]
                        if 'Чек на' in result.title: 
                            await result.click(avto_vivod_tag)
                    except:
                        pass
            if message.reply_markup.rows[0].buttons[0].text != '›':
                if len(message.reply_markup.rows[0].buttons) == 1:
                    break
                else:
                    if message.reply_markup.rows[0].buttons[1].text != '›':
                        break
            await message.click(text='›')
        print(f'[$] Автовывод > Ваши средства отправлены на основной аккаунт!')
        await client.send_message(channel, message=f'<b>💲 Ваши средства успешно отправлены на основной аккаунт!</b>', parse_mode='HTML') 
        is_off = False
        await asyncio.sleep(22320)

@client.on(events.NewMessage(chats=[1985737506], pattern="⚠️ Вы не можете активировать этот чек, так как вы не являетесь подписчиком канала"))
async def handle_new_message(event):
    code = None
    if event.message.reply_markup is None or is_off is True:
        return
    for row in event.message.reply_markup.rows:
        for button in row.buttons:
            if isinstance(button, types.KeyboardButtonUrl):
                check = code_regex.search(button.url)
                if check:
                    code = check.group(2)
                    continue
                channel = url_regex.search(button.url)
                public_channel = public_regex.search(button.url)
                try:
                    if channel:
                        await client(ImportChatInviteRequest(channel.group(1)))
                    if public_channel:
                        await client(JoinChannelRequest(public_channel.group(1)))
                except:
                    pass
    if code not in wallet:
        await client.send_message('wallet', message=f'/start {code}')
        wallet.append(code)

@client.on(events.NewMessage(chats=[1559501630], pattern="Чтобы"))
async def handle_new_message(event):
    if event.message.reply_markup is None or is_off is True:
        return
    for row in event.message.reply_markup.rows:
        for button in row.buttons:
            if isinstance(button, types.KeyboardButtonUrl):
                channel = url_regex.search(button.url)
                if channel:
                    try:
                        await client(ImportChatInviteRequest(channel.group(1)))
                    except:
                        pass
    try:
        await event.message.click(data=b'check-subscribe')
    except:
        pass

@client.on(events.NewMessage(chats=[5014831088], pattern="Для активации чека"))
async def handle_new_message(event):
    if event.message.reply_markup is None or is_off is True:
        return
    for row in event.message.reply_markup.rows:
        for button in row.buttons:
            if isinstance(button, types.KeyboardButtonUrl):
                channel = url_regex.search(button.url)
                public_channel = public_regex.search(button.url)
                try:
                    if channel:
                        await client(ImportChatInviteRequest(channel.group(1)))
                    if public_channel:
                        await client(JoinChannelRequest(public_channel.group(1)))
                except:
                    pass
    try:
        await event.message.click(data=b'Check')
    except:
        pass

@client.on(events.NewMessage(chats=[5794061503]))
async def handle_new_message(event):
    if event.message.reply_markup is None:
        return
    for row in event.message.reply_markup.rows:
        for button in row.buttons:
            if isinstance(button, types.KeyboardButtonCallback):
                if (button.data.decode()).startswith(('showCheque_', 'activateCheque_')):
                    await event.message.click(data=button.data)
                continue
            if isinstance(button, types.KeyboardButtonUrl):
                channel = url_regex.search(button.url)
                public_channel = public_regex.search(button.url)
                try:
                    if channel:
                        await client(ImportChatInviteRequest(channel.group(1)))
                    if public_channel:
                        await client(JoinChannelRequest(public_channel.group(1)))
                except:
                    pass

async def filter(event):
    for word in ['Вы получили', 'Вы обналичили чек на сумму:', '✅ Вы получили:', '💰 Вы получили']:
        if word in event.message.text:
            return True
    return False

@client.on(events.MessageEdited(chats=crypto_black_list, func=filter))
@client.on(events.NewMessage(chats=crypto_black_list, func=filter))
async def handle_new_message(event):
    try:
        bot = (await client.get_entity(event.message.peer_id.user_id)).usernames[0].username
    except:
        bot = (await client.get_entity(event.message.peer_id.user_id)).username
    summ = event.raw_text.split('\n')[0].replace('Вы получили ', '').replace('✅ Вы получили: ', '').replace('💰 Вы получили ', '').replace('Вы обналичили чек на сумму: ', '')
    global checks_count
    checks_count += 1
    await client.send_message(channel, message=f'✅ Активирован чек на сумму <b>{summ}</b>\nБот: <b>@{bot}</b>\nВсего чеков после запуска активировано: <b>{checks_count}</b>', parse_mode='HTML') 

@client.on(events.MessageEdited(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
@client.on(events.NewMessage(outgoing=False, chats=crypto_black_list, blacklist_chats=True))
async def handle_new_message(event):
    if is_off is True:
        return
    try:
        message_text = event.message.text.translate(translation)
    except:
        return
    codes = code_regex.findall(message_text)
    if codes:
        for bot_name, code in codes:
            if code not in checks:
                await client.send_message(bot_name, message=f'/start {code}')
                checks.append(code)
    if event.message.reply_markup is None:
        return
    for row in event.message.reply_markup.rows:
        for button in row.buttons:
            if isinstance(button, types.KeyboardButtonUrl):
                match = code_regex.search(button.url)
                if match:
                    if match.group(2) not in checks:
                        await client.send_message(match.group(1), message=f'/start {match.group(2)}')
                        checks.append(match.group(2))
                            
async def anti_cap():
    @client.on(events.NewMessage(chats=[1559501630, 1622808649], func=lambda e: e.photo))
    async def handle_photo_message(event):
        photo = await event.download_media(bytes)
        recognized_text = await ocr_space(file=photo)
        if recognized_text and recognized_text not in captches:
            global is_off
            is_off = True
            code = (await client.get_messages(event.message.peer_id.user_id, limit=1))[0].message
            if '/start' not in code:
                code = None
            await client.send_message(event.message.peer_id.user_id, message=recognized_text)
            await asyncio.sleep(0.5)
            message = (await client.get_messages(event.message.peer_id.user_id, limit=1))[0].message
            if 'Incorrect answer.' in message or 'Неверный ответ.' in message:
                await client.send_message(channel, message=f'<b>❌ Не удалось разгадать каптчу, решите ее сами.</b>', parse_mode='HTML') 
                print(f'[!] Ошибка антикаптчи > Не удалось разгадать каптчу, решите ее сами.')
                captches.append(recognized_text)
            else:
                print(f'[$] Антикаптча > Каптча успешно решена!')
                await client.send_message(channel, message=f'<b>🖼️ Каптча успешно решена!</b>', parse_mode='HTML') 
            is_off = False
            if code is not None:
                await client.send_message(event.message.peer_id.user_id, message=code)
        if not recognized_text:
            await client.send_message(channel, message=f'<b>❌ Не удалось разгадать каптчу, решите ее сами.</b>', parse_mode='HTML') 
            print(f'[!] Ошибка антикаптчи > API не вернуло ответа. Пройдите каптчу самостоятельно.')
    print(f'[$] Антикаптча подключена!')

async def main():
    try:
        await client.start()
        try:
            await client(JoinChannelRequest('lovec_checkov'))
        except:
            pass
        if avto_vivod is True and avto_vivod_tag != '':
            try:
                message = await client.send_message(avto_vivod_tag, message='1')
                await client.delete_messages(avto_vivod_tag, message_ids=[message.id])
                asyncio.create_task(pay_out())
                print(f'[$] Автовывод подключен!')
            except:
                print(f'[!] Ошибка автовывода > Не удалось отправить тестовое сообщение на тег для автовывода. Автовывод отключен.')
        elif avto_vivod is True and avto_vivod_tag == '':
            print(f'[!] Ошибка автовывода > Вы не указали тег для автовывода.')
        if anti_captcha == True:
            await anti_cap()
        print(f'[$] Ловец чеков успешно запущен!')
        print(f'[+] Наш канал с обновлениями: https://t.me/lovec_checkov')
        print(f'[+] Разработчик: @absolutely_enough')
        await client.run_until_disconnected()
    except Exception as e:
        print(f'[!] Ошибка коннекта > {e}')

asyncio.run(main())