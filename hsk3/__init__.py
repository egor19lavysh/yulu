from hsk3.reading.handlers import router as reading_router
from hsk3.writing.handlers import router as writing_router
from hsk3.listening.handlers import router as listening_router
from .full_test import router as full_test_router
from .words import router as words_router
from hsk3.intro import router

routers = [router, reading_router, writing_router, listening_router, full_test_router, words_router]
