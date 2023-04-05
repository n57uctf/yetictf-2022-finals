from fastapi import FastAPI, Request, Form, APIRouter, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from config import SQLALCHEMY_DATABASE_URL
import crud
import schemas
import databases

active_login = None

class UnicornException(Exception):
    def __init__(self, content: str, code_status: int):
        self.content = content
        self.status = code_status

app = FastAPI()

app.mount('/shape/static/css', StaticFiles(directory="/usr/src/app/shape/static/css"), name="styles")
app.mount('/shape/static/js', StaticFiles(directory="/usr/src/app/shape/static/js"), name="js")
app.mount('/shape/static/imgs', StaticFiles(directory="/usr/src/app/shape/static/imgs"), name="im")
temp = Jinja2Templates(directory="/usr/src/app/shape/")

user_router = APIRouter(
    prefix="/api/user",
    tags=["user"],
    responses={404: {"description": " Not found :("}},
)

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """ Обработчик ошибок типа UnicornException """
    return temp.TemplateResponse("info.html", {"request": request,
                                               "status": exc.status,
                                               "message": f"Oops! {exc.content}",
                                               })

database = databases.Database(SQLALCHEMY_DATABASE_URL)

@app.get("/")
async def mainPage(request: Request):
    if active_login:
        return temp.TemplateResponse("index.html", {"request": request, "isAutorized":active_login})
    else:
        return temp.TemplateResponse("index.html", {"request": request})

@user_router.get("/sign-up")
async def signUpGet(request: Request):
    return temp.TemplateResponse("signup.html", {"request": request})

@user_router.post("/sign-up")
async def signUp(request: Request, login: str = Form(...), passwrd: str = Form(...)):
    
    if_already_registered = await crud.already_registered(database, login)
    
    if if_already_registered:
        return await unicorn_exception_handler(request,
            UnicornException("This user already registered, him pass: "+str(if_already_registered), 400))
    else:
        instance = schemas.UserCreate(login=login, password=passwrd)
        result = await crud.create_user(database, instance)
        return temp.TemplateResponse("tmp.html", {"request": request, "user_data": result})

@user_router.get("/sign-in")
async def signInGet(request: Request):
    return temp.TemplateResponse("signin.html", {"request": request})

@user_router.post("/sign-in")
async def signIn(request: Request, login: str = Form(...), password: str = Form(...)):
    global active_login
    cuser = schemas.UserCreate(login=login, password=password)
    if_active = await crud.check_current_user(database, cuser)

    if isinstance(if_active, dict):
        return await unicorn_exception_handler(request, UnicornException("No such user", 404))

    if not if_active:
        active_login = login
        await crud.activate_user(database, cuser)
    
    active_login = login
    return await mainPage(request)

def deactivateLogin():
    global active_login
    active_login = None

@user_router.get("/log-out", response_model=schemas.UserBase, response_model_exclude_unset=True)
async def logOut(request: Request):
    if not active_login:
        return await unicorn_exception_handler(request, UnicornException("Exit error", 400))

    response = await crud.deactivate_user(database, active_login)
    deactivateLogin()
    print(jsonable_encoder(response))
    return RedirectResponse("/")

@user_router.get("/sign-in/messages")
async def getMessenges(request: Request):
    print(active_login)
    incoming_messages = await crud.all_incoming_messages(database, active_login)

    if isinstance(incoming_messages, str):
        return temp.TemplateResponse("messages.html", {"request": request, "isAutorized":active_login, 
                                     "length":0})
    elif not incoming_messages:
        return await unicorn_exception_handler(request, UnicornException("You are not authorized!", 400))
    else:
        return temp.TemplateResponse("messages.html", {"request": request, "isAutorized":active_login, 
                                                    "messages": incoming_messages, "length": len(incoming_messages)})


@user_router.post("/sign-in/messages", response_model=schemas.SendedBase, response_model_exclude_unset=True)
async def sendMessage(request: Request, recipientName: str = Form(...), message: str = Form(...)):
    returned = await crud.send_message(database, active_login, recipientName, message)
    if not returned:
        return await unicorn_exception_handler(request, UnicornException("No such recipient or sender", 404))
    else:
        return returned

@user_router.get("/sign-in/messages/all-users")
async def getAllUsers(request: Request):
    print(active_login)
    all_users = await crud.all_users_db(database, active_login)

    if not all_users:
        return await unicorn_exception_handler(request, UnicornException("You are not authorized!", 400))

    return temp.TemplateResponse("index.html", {"request": request, "isAutorized":active_login, 
                                                "users": all_users, "length": len(all_users)})

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(user_router)
