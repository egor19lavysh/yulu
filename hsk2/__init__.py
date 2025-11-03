from hsk2.intro import router
from hsk2.words import router as words_router
from hsk2.listening.handlers import router as listening_router
from hsk2.reading.handlers import router as reading_router

routers = [router, words_router, listening_router, reading_router]