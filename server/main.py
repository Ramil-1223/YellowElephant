import uvicorn
from fastapi import FastAPI
from core.create import create
from core.drop import drop
from core.list import ls
from core.backup import backup

app = FastAPI()

app.include_router(create)
app.include_router(drop)
app.include_router(ls)
app.include_router(backup)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9999)