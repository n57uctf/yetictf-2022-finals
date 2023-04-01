# CREATE READ UPDATE DELETE
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
import databases, string
from models.users_and_messages import users_table as users
from models.users_and_messages import messages_table as messages
import schemas
from random import choice
from algorithm.cipher import cipher
from datetime import datetime

# smth for password-hashing

instance1, instance2 = cipher(), cipher()

def get_random_string(length=12):
    return "".join(choice(string.ascii_letters) for _ in range(length))

def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    
    instance1.setOptions(salt, password)
    enc = instance1.encrypt(password)
    return enc

async def get_hash_by_user(db: databases.Database, login: str):
    query = users.select().where(
        users.c.login == login
    )
    result = await db.fetch_one(query)
    return result["password"]

def validate_password(password: str, hashed_password: str) -> bool:
    """ Проверяет, что хеш пароля совпадает с хешем из БД """
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed

async def create_user(db: databases.Database, user: schemas.UserCreate):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hash = hash_password(user.password, salt)
    pswrd = f"{salt}${hash}"

    dt=datetime.now()
    
    query = users.insert().values(
        login=user.login, password=pswrd, date=dt, is_active = False
    )
    user_id = await db.execute(query)

    return {"id": user_id,"login": user.login, "password": pswrd, "date": dt}

# smth for auth

async def get_current_user(db: databases.Database, login: str):
    query = users.select().where(users.c.login == login)
    return await db.fetch_one(query)

async def check_current_user(db: databases.Database, user: schemas.UserCreate):
    try:
        query = users.select().where(
            users.c.login == user.login
        )
        response = jsonable_encoder(await db.fetch_one(query))

        if not validate_password(user.password, response["password"]):
            raise Exception

        return response["is_active"]
    except Exception:
        return {"Error": "No such user!"}

async def deactivate_user(db: databases.Database, user: str):
    user_data = await get_current_user(db, user)
    uid = jsonable_encoder(user_data)["id"]

    dctvt = users.update().where(
        and_(
            users.c.id == uid,
            users.c.login == user, 
    )).values(is_active = False)

    await db.execute(dctvt)
    response = await get_current_user(db, user)
    return response

async def activate_user(db: databases.Database, user: schemas.UserCreate):
    
    user_data = await get_current_user(db, user.login)
    uid = jsonable_encoder(user_data)["id"]

    actvt = users.update().where(
        and_(
            users.c.id == uid,
            users.c.login == user.login, 
    )).values(is_active = True)

    await db.execute(actvt)

async def already_registered(db: databases.Database, login: str):
    try:
        query = users.select().where(
            users.c.login == login
        )
        response = await db.fetch_one(query)
        return jsonable_encoder(response)
    except Exception:
        return False

# smth for chatting

async def checkRecipientOrSender(db: databases.Database, name: str):
    try:
        user_data = await get_current_user(db, name)
        json_uid = jsonable_encoder(user_data)
        uid = json_uid["id"]
    except Exception:
        return False
    else:
        return uid


async def send_message(db: databases.Database, senderName: str, recipientName: str, message: str):
    instance = cipher()
    suid, ruid = await checkRecipientOrSender(db, senderName), await checkRecipientOrSender(db, recipientName)
    
    if not suid or not ruid:
        return False

    m_data = datetime.now()
    instance.setOptions(senderName, recipientName)
    
    super_encrypted_message = instance.encrypt(message)

    query = messages.insert().values(date=m_data, SenderName=senderName, RecipientName=recipientName,
                                        Messege=super_encrypted_message, user_id=suid)
    message_id = await db.execute(query)
    
    return {"id":message_id, "senderName":senderName, "recipientName":recipientName, 
            "message":super_encrypted_message, "date":m_data, "user_id": suid}


async def all_users_db(db: databases.Database, login: str):
    uid = await checkRecipientOrSender(db, login)

    if not uid: return False

    query = users.select().where(
        users.c.id != uid
    )
    db_result = await db.fetch_all(query)

    result = jsonable_encoder(db_result)
    return result


def decode_all_messages(result: list):
    m1 = cipher()

    for item in result:
        for k,v in item.items():
            if k == "Messege":
                m1.setOptions(item["SenderName"], item["RecipientName"])
                item[k] = m1.decrypt(v)
            else:
                continue
    return result


async def all_incoming_messages(db: databases.Database, login: str):
    uid = await checkRecipientOrSender(db, login)

    if not uid: return False
    
    query = messages.join(users).select().where(
        and_
        (
            messages.c.SenderName != login,
            messages.c.RecipientName == login,
        )
    )

    db_res = await db.fetch_all(query)

    result = jsonable_encoder(db_res)

    if result == []:
        return "No messages yet!"

    result = decode_all_messages(result)

    return result


