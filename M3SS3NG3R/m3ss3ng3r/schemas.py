from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime

class UserCreate(BaseModel):
    """ Проверяет sign-up запрос """
    login: str
    password: str

    @validator('login')
    def logging_check(cls, v):
        if len(v) == 1:
            raise ValueError('Login lenght must be more then 1! Fixed it.')
        return v

class UserBase(UserCreate):
    """ Формирует тело ответа с деталями пользователя """
    id: int
    date: datetime = datetime.now()
    is_active: Optional[bool] = False


class SendedBase(BaseModel):
    id: int
    senderName: str
    recipientName: str
    message: str
    date: datetime = datetime.now()
    user_id: str
