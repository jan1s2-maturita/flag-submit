from typing import Annotated
from fastapi import FastAPI, HTTPException, Header
from .models.db_connect import Database
from .config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT, PUBLIC_KEY_PATH
db = Database(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS, db_name=DB_NAME)
from jwt import decode
from pydantic import BaseModel

app = FastAPI()

class Data(BaseModel):
    flag: str
@app.post("/submit/{flag_id}")
async def submit(flag_id: int, data: Data, x_token: Annotated[str, Header()]):
    payload = None
    try:
        with open(PUBLIC_KEY_PATH, 'r') as f:
            public_key = f.read()
            payload = decode(x_token, public_key, algorithms=['RS256'])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    if db.submit_user_flag(payload["id"], flag_id, data.flag):
        return {"success": True}
    else:
        raise HTTPException(status_code=400, detail="Invalid flag")

@app.get("/health")
async def health():
    return {"status": "up"}
