from telethon import TelegramClient
import json
import os
import asyncio
from rich.console import Console; con = Console()

with open('session.json') as f:
    SessionJSON = json.load(f)
api_id = SessionJSON['app_id']
api_hash = SessionJSON['app_hash']
client = TelegramClient('TelegramConsole', api_id, api_hash)

os.system('clear')

async def GetChats():
    # Getting information about yourself
    me = await client.get_me()
    #print(me.stringify())

    con.print(f'''
[green]████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     [/]    
[green]╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     [/]    
[green]   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     [/]    
[green]   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     [/]    
[green]   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗[/]    
[green]   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝[/]    
            [cyan]████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗[/]   
            [cyan]╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║[/]   
            [cyan]   ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║[/]   
            [cyan]   ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║[/]   
            [cyan]   ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║[/]   
            [cyan]   ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝[/]   
[magenta]{me.username}   |   +{me.phone}
    ''')

    ChatsList = []; i = 0
    async for dialog in client.iter_dialogs():
        i = i + 1
        ChatsList.append(
            {
                'ID': i,
                'DialogID': dialog.id,
                'DialogName': dialog.name
            }
        )
    
    return ChatsList



async def gather_messages(ChatID: int):
    chat = []
    messages = client.iter_messages(ChatID)
    async for message in reversed(messages):
        sender = await message.get_sender()
        try: username = sender.username
        except: username = None
        try: FirstName = sender.first_name
        except: FirstName = None
        try: LastName = sender.last_name
        except: LastName = None
        print(message)
        #con.print(str(type(message)), style='red')
        chat.append(
            {
                'type': str(type(message)),
                'ID': message.id,
                'username': username,
                'FirstName': FirstName,
                'LastName': LastName,
                'date': message.date,
                'text': message.text,
                'pinned': message.pinned
            }
        )
    return chat 



async def ShowChat(ChatID: int):
    messages = await gather_messages(ChatID=ChatID)
    for message in messages:
        MessageType = message['type']
        MessageID = message['ID']
        MessageUsername = message['username']
        MessageFirstName = message['FirstName']
        MessageLastName = message['LastName']
        MessageDate = message['date']
        MessageText = message['text'] 
        MessagePinned = message['pinned']

        if MessageType == "<class 'telethon.tl.patched.Message'>":
            MsgInfo = f'[{MessageID}][{MessageDate}]'
            if MessageUsername != None: MsgInfo = MsgInfo + f'[cyan](@{MessageUsername})[/]'
            if MessageFirstName != None: MsgInfo = MsgInfo + f'[yellow]{MessageFirstName}[/]'
            if MessageLastName != None: MsgInfo = MsgInfo + f' [yellow]{MessageLastName}[/]'
            if MessagePinned == True: MsgInfo = MsgInfo + f': [green]{MessageText}[/]' 
            else: MsgInfo = MsgInfo + f': {MessageText}'
            con.print(MsgInfo)
        elif MessageType == "<class 'telethon.tl.patched.MessageService'>":
            pass

    SendMsg = input('Введите сообщение: ')
    if SendMsg == '': os.system('clear'); await ShowChat(ChatID=ChatID)
    elif '>d' in SendMsg: 
        data = SendMsg.split(' ')
        await client.delete_messages(ChatID, int(data[1]))
        os.system('clear'); await ShowChat(ChatID=ChatID)

    elif '>e' in SendMsg:
        data = SendMsg.split(' ')
        await client.edit_message(ChatID, int(data[1]), SendMsg.replace('>e', '').replace(data[1], ''))
        os.system('clear'); await ShowChat(ChatID=ChatID)

    elif SendMsg == '>pin':
        MsgID = con.input('[black on white]Введите ID сообщения[/][deep_pink4 on white]([red1 on white][>b][/] - Отмена)[/]: ')
        if MsgID == '>b': os.system('clear'); await ShowChat(ChatID=ChatID)
        else:
            notify_input = con.input('Уведомить о закреплении сообщения? [[green]Y[/]/[red]N[/]]: ')
            if notify_input == '>b': os.system('clear'); await ShowChat(ChatID=ChatID)
            elif notify_input == 'Y' or notify_input == 'y' or notify_input == '': notify = True
            elif notify_input == 'N' or notify_input == 'n': notify = False

            pm_oneside_input = con.input('Закрепить у всех? [[green]Y[/]/[red]N[/]]: ')
            if notify_input == '>b': os.system('clear'); await ShowChat(ChatID=ChatID)
            elif pm_oneside_input == 'Y' or pm_oneside_input == 'y' or pm_oneside_input == '': pm_oneside = False
            elif pm_oneside_input == 'N' or pm_oneside_input == 'n': pm_oneside = True

            await client.pin_message(ChatID, int(MsgID), notify=notify, pm_oneside=pm_oneside)
            os.system('clear'); await ShowChat(ChatID=ChatID)


    elif SendMsg == '>unpin': 
        MsgID = con.input('Введите ID сообщения([>b] - Отмена): ')
        if MsgID == '>b': os.system('clear'); await ShowChat(ChatID=ChatID)
        else:
            await client.unpin_message(ChatID, int(MsgID))
            os.system('clear'); await ShowChat(ChatID=ChatID)


    

    elif SendMsg == '>b': os.system('clear'); await ShowChats()
    elif '>pic' in SendMsg: pass
    else:
        await client.send_message(ChatID, SendMsg)
        os.system('clear'); await ShowChat(ChatID=ChatID)

async def ShowChats():
    async with client:
        ChatsList = await GetChats()
        for chat in ChatsList:
            ID = chat['ID']
            DialogName = chat['DialogName']
            con.print(f'[{ID}] - {DialogName}', style='yellow')
        con.print('\n[>e] - exit\n[>s] - serch')
        choose = input('>')

        if choose == '>e': exit
        
        else: 
            for i in ChatsList:
                if int(i['ID']) == int(choose):
                    ChatID = i['DialogID']
                    await ShowChat(ChatID=ChatID)

if __name__ == '__main__':
    asyncio.run(ShowChats())
