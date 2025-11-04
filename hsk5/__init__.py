from .intro import router
from .words import router as words_router
from hsk5.listening.handlers import router as listening_router


routers = [router, words_router, listening_router]
