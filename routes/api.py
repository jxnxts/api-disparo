from fastapi import APIRouter
from endpoints import Instance, webhook, Contatos, Grupos, Import_grupo, whatsapp, queue, mensagens

router = APIRouter()
router.include_router(Instance.router)
router.include_router(Contatos.router)
router.include_router(Grupos.router)
router.include_router(Import_grupo.router)
router.include_router(mensagens.router)
router.include_router(whatsapp.router)
router.include_router(webhook.router)
router.include_router(queue.router)
