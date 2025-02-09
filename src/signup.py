import asyncpg
import uuid
import re

from fastapi import FastAPI, HTTPException
from typing import Dict

# ==============================================

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "CCCAT20_1 course from Rodrigo Branas!"}


@app.get("/account/{account_id}")
async def get_account(account_id: int):
    conn = await asyncpg.connect(dsn="postgres://postgres:123456@localhost:5432/app")
    result = await conn.fetch("SELECT * FROM ccca.account WHERE account_id = $1", account_id)
    await conn.close()
    
    if result:
        return dict(result[0])
    
    return dict("There was no result!")


@app.post("/signup")
async def signup():
    None

@app.post("/signup")
async def signup(req_body: Dict):
    account_id = str(uuid.uuid4())
    result = None

    existing_account = await get_account_from_db(req_body["email"])

    if not existing_account:
        if bool(re.match(r'[a-zA-Z]+\s[a-zA-Z]+', req_body["name"])):
            if bool(re.match(r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)", req_body["email"])):
                if bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$", req_body["password"])):
                    if len(req_body["cpf"]) == 11 and req_body["cpf"].isdigit():
                        if(req_body.get("isDriver")):
                            if bool(re.match(r"[A-Z]{3}[0-9]{4}", req_body["carPlate"])):
                                await insert_account_to_db(
                                    account_id,
                                    req_body["name"],
                                    req_body["email"],
                                    req_body["cpf"],
                                    req_body["carPlate"],
                                    bool(req_body.get("isPassenger", False)),
                                    bool(req_body["isDriver"]),
                                    req_body["password"]
                                )
                                result = {"accountId": account_id}
                            else:
                                result = -6
                        else:
                            await insert_account_to_db(
                                    account_id,
                                    req_body["name"],
                                    req_body["email"],
                                    req_body["cpf"],
                                    req_body["carPlate"],
                                    bool(req_body.get("isPassenger", False)),
                                    bool(req_body["isDriver"]),
                                    req_body["password"]
                                )
                            result = {"accountId": account_id}
                    else:
                        result = -1
                else:
                    result = -5
            else:
                result = -2
        else:
            result = -3
    else:
        result = -4

    if isinstance(result, int):
        raise HTTPException(status_code=422, detail={"message": result})
    else:
        return result


async def get_account_from_db(email: str):
    conn = await asyncpg.connect(dsn="postgres://postgres:123456@localhost:5432/app")
    result = await conn.fetch("SELECT * FROM ccca.account WHERE email = $1", email)
    await conn.close()
    return result


async def insert_account_to_db(account_id: str, name: str, email: str, cpf: str, car_plate: str, is_passenger: bool, is_driver: bool, password: str):
    conn = await asyncpg.connect(dsn="postgres://postgres:123456@localhost:5432/app")
    await conn.execute(
        "INSERT INTO ccca.account (account_id, name, email, cpf, car_plate, is_passenger, is_driver, password) "
        "VALUES ($1, $2, $3, $4, $5, $6, $7, $8)",
        account_id, name, email, cpf, car_plate, is_passenger, is_driver, password
    )
    await conn.close()