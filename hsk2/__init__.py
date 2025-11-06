from hsk2.intro import router
from hsk2.words import router as words_router
from hsk2.listening.handlers import router as listening_router
from hsk2.reading.handlers import router as reading_router
from hsk2.full_test import router as full_test_router

routers = [router, words_router, listening_router, reading_router, full_test_router]