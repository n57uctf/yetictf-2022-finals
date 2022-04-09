from pydantic import BaseModel
from typing import List, Optional, Any


class UserCredentials(BaseModel):
    login: str
    password: str

class AuthToken(BaseModel):
    jwt: str

class UserApiKey(BaseModel):
    apikey: str

class Response(BaseModel):
    success: bool
    data: Optional[Any]

class User(BaseModel):
    id: Optional[int]
    login: str
    password_hash: str
    api_key: str

class DataBase(BaseModel):
    id: Optional[int]
    db_name: str
    owner: int
    table_count: int
    create_date: str
    description: str

class DataBaseColumn(BaseModel):
    columnName: str
    varType: str

class DataBaseTable(BaseModel):
    tableName: str
    columns: List[DataBaseColumn]

class DataBaseFront(BaseModel):
    name: str
    description: str
    tables: List[DataBaseTable]

class ApiResponse(BaseModel):
    success: bool
    data: Any

class Cell(BaseModel):
    column_name: str
    value: str

class Row(BaseModel):
    row: List[Cell]

class Table(BaseModel):
    table: List[Row]

class TableSchema(Row):
    table_name: str

class DBSchema(BaseModel):
    db_name: str
    tables: List[TableSchema]