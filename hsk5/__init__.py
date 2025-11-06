from .intro import router
from .words import router as words_router
from hsk5.listening.handlers import router as listening_router
from hsk5.writing.handlers import router as writing_router
from hsk5.reading.handlers import router as reading_router
from hsk5.full_test import router as full_test_router


routers = [router, words_router, listening_router, writing_router, reading_router, full_test_router]
