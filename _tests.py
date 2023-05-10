from api.zapi import get_chats


instanceId = '3BD0EC25C42700F71FFC761E7FB83AB5'
token = 'D40F72612B483B4E4E1073DF'


data = get_chats(instanceId, token)

for messages in data:
    if messages.isGroup == True:
        print(messages.phone)