from .intro import router
from .words import router as words_router
from hsk5.listening.handlers import router as listening_router
from hsk5.writing.handlers import router as writing_router
from hsk5.reading.handlers import router as reading_router


routers = [router, words_router, listening_router, writing_router, reading_router]
