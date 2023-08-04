from api.zapi import get_chats, send_link, save_contacts, get_groups
from models.request import MensagemLinkRequest
from endpoints.mensagens import enviar_link
from endpoints.Import_grupo import get_grupos_by_instanceId
import json



# id = 5
# instanceId = '3BD0D4D493AA20F71F43021F9CCA646D'
# token = '317DE0D63122EFD7BCAFF7EF'
# phone = "5586988675485"

# message = "test https://conectapiaui.com.br/blog/coluna-vip/personalidades-exibem-looks-exuberantes-no-baile-do-laellyo-mesquita-em-teresina-486.html"
# image = "https://conectapiaui.com.br/media/image_bank/2023/7/thumbs/looks-espetaculares.jpg.1200x0_q95_crop.webp"
# linkUrl = "https://conectapiaui.com.br/blog/coluna-vip/personalidades-exibem-looks-exuberantes-no-baile-do-laellyo-mesquita-em-teresina-486.html"
# title = "teste"
# linkDescription = "Teresina ficou pequena na noite desta terça-feira (11/07)"
# linkType = "LARGE"
# delayMessage = 1

# body = MensagemLinkRequest ( phone=phone,
#                             message=message, 
#                             image=image,
#         linkUrl=linkUrl, 
#         title=title, 
#         linkDescription=linkDescription,
#         linkType=linkType,
#         delayMessage=delayMessage)


# envio = enviar_link(id, body)
# print(envio)


# data = send_link(instanceId, token, message, phone, image, linkUrl, title, linkDescription, linkType, delayMessage)


# get_grupos_by_instanceId(5)