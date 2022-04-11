from fastapi import HTTPException

from app.models import ApiResponse, Row
from app import api, app_db
from app.db_manager import DBManager
from app.logger import Log4j


@api.get("/dbs")
def get_dbs(key: str):
    db_mang = DBManager()
    user_dbs_names = [db.db_name for db in app_db.select_user_dbs(api_key=key)]
    try:
        login = app_db.select_login_by_api_key(key)
    except Exception as e:
        return ApiResponse(
            success=False,
            data=str(e)
        )
    if not login:
        return ApiResponse(
            success=False
        )
    return ApiResponse(
        success=True,
        data=db_mang.get_user_db_schema(login, user_dbs_names)
    )

@api.get("/", response_model=ApiResponse)
def select_data(key: str, db: str, table: str, column: str = None, value: str = None):
    db_mang = DBManager()
    user_dbs_names = [db.db_name for db in app_db.select_user_dbs(api_key=key)]
    if db not in user_dbs_names:
        raise HTTPException(status_code=401)
    try:
        login = app_db.select_login_by_api_key(key)
    except Exception as e:
        return ApiResponse(
            success=False,
            data=str(e)
        )
    try:
        result = db_mang.select_row(login, db, table, column, value)
    except Exception as e:
        return ApiResponse(
            success=False,
            data=str(e)
        )
    return ApiResponse(
        success=True,
        data=result
    )

@api.post("/", response_model=ApiResponse)
def insert_data(key: str, db: str, table: str, data: Row):
    db_mang = DBManager()
    user_dbs_names = [db.db_name for db in app_db.select_user_dbs(api_key=key)]
    if db not in user_dbs_names:
        raise HTTPException(status_code=401)
    login = app_db.select_login_by_api_key(key)
    try:
        result = db_mang.insert_row(login, db, table, data)
    except Exception as e:
        return ApiResponse(
            success=False,
            data=str(type(e)) + ": " + str(e)
        )
    return ApiResponse(
        success=True
    )

@api.delete("/")
def delete_data():
    return ApiResponse(
        success=False,
        data="Method deprecated"
    )