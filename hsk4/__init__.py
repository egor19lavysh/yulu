from hsk4.listening.handlers import router as listening_router
from hsk4.reading.handlers import router as reading_router
from hsk4.writing.handlers import router as writing_router
from hsk4.intro import router

routers = [router, listening_router, reading_router, writing_router]