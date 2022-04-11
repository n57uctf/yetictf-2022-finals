from datetime import datetime

from fastapi import HTTPException, Header, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse

from app import app, app_db
from app.models import DataBase, UserCredentials, AuthToken, User, Response, UserApiKey, DataBaseFront
from app.auth import get_auth_token, hash_sha256, generate_api_key, verify_hash, verify_auth_token
from app.logger import Log4j
from app.db_manager import DBManager


def auth_required(authorization: str = Header("Authorization")):
    if not authorization:
        raise HTTPException(status_code=401)
    try:
        jwt_payload = verify_auth_token(authorization.split()[1])
    except Exception as e:
        raise HTTPException(status_code=401)        
    return jwt_payload

@app.post('/login')
def login(creds: UserCredentials):
    try:
        user = app_db.select_user(login=creds.login)
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
        )
    if verify_hash(user.password_hash, creds.password):
        return Response(
            success=True,
            data=AuthToken(
                jwt=get_auth_token(user.login)
            )
        )    
    return Response(
        success=False,
    )

@app.post('/register')
def register(creds: UserCredentials):
    user = User(
        login=creds.login,
        password_hash=hash_sha256(creds.password),
        api_key=generate_api_key(creds.login, creds.password)
    )
    try:
        app_db.create_user(user)
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
            data=str(e)
        )
    return Response(
        success=True
    )

@app.get('/last_log')
def get_new_dbs(seconds: int):
    try:
        new_dbs = app_db.select_db_creation_log(seconds)
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
            data=str(e)
        )
    return Response(
        success=True,
        data=new_dbs
    )
    

@app.get('/api_key')
def get_api_key(dependency: dict = Depends(auth_required)):
    try:
        api_key = app_db.select_user_api_key(dependency.get("login"))
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
            data=str(e)
        )
    return Response(
        success=True,
        data=UserApiKey(
            apikey=api_key
        )
    )


@app.get('/dbs')
def get_user_dbs(dependency: dict = Depends(auth_required)):
    try:
        dbs = app_db.select_user_dbs(dependency.get("login"))
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
            data=str(e)
        )
    return Response(
        success=True,
        data=dbs
    )


@app.post('/new_db')
def create_new_user_db(user_db: DataBaseFront, dependency: dict = Depends(auth_required)):
    try:
        user = app_db.select_user(login=dependency.get("login"))
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
            data=str(e)
        )
    db_mgr = DBManager()
    try:
        db_mgr.create_user_db(user_db, user.login)
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
            data=str(e)
        )
    try:
        app_db.create_user_db(
            DataBase(
                db_name=user_db.name,
                owner=user.id,
                table_count=len(user_db.tables),
                create_date=int(datetime.now().timestamp()),
                description=user_db.description,
            )
        )
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        return Response(
            success=False,
            data=str(e)
        )
    return Response(
        success=True
    )

@app.get('/')
def get_app_angular():
    with open('static/index.html', 'r') as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)

@app.get('/pub_key', response_class=PlainTextResponse) #Endpoint for auth itegration with other services
def get_public_key():
    try:
        with open('jwtRS256.key.pub', 'r') as pub_key_file:
            pub_key = pub_key_file.read()
    except Exception as e:
        Log4j.error(str(type(e)) + ": " + str(e))
        raise HTTPException(status_code=404)
    return pub_key
