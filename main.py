import uvicorn
from fastapi import FastAPI

from app.views import api
from app.database import Base, engine

app = FastAPI()


app.include_router(api)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    uvicorn.run('main:app', reload=True)
