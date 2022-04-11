import sqlite3
import re
import os
from threading import Lock

from app.models import DataBaseFront, Cell, Row, TableSchema, DBSchema
from app.exceptions import NotAllowedCharacterException, NotAllowedDatatypeException, DatabaseAlreadyExistException, AppException


class DBManager(object):
    def __init__(self):
        self.allowed_characters = r'[^a-zA-Z0-9.]'
        self.allowed_datatypes = ("TEXT","BLOB","INTEGER","REAL",)
        self.db_storage_path = "./users_dbs/"
        self.lock = Lock()

    def is_allowed_datatype(self, string):
        return string in self.allowed_datatypes

    def is_allowed_string(self, string):
        characher_regex = re.compile(self.allowed_characters)
        string = characher_regex.search(string)
        return not bool(string)

    def get_user_db_files(self, login, db_names):
        db_files = sorted(os.listdir(path=self.db_storage_path))
        user_db_files = []
        for db_file in db_files:
            for db_name in db_names:
                if db_file.endswith(login + db_name + ".db"):
                    user_db_files.append(db_file)
                    break
        return user_db_files

    def create_user_db(self, schema: DataBaseFront, login: str):
        with self.lock:
            if not self.is_allowed_string(schema.name):
                raise NotAllowedCharacterException(f"Invalid database name '{schema.name}'")
            db_file_name = login + schema.name + ".db"
            if db_file_name in self.get_user_db_files(login, db_file_name):
                raise DatabaseAlreadyExistException(f"Database '{schema.name}' already exist")
            connector = sqlite3.connect(self.db_storage_path + db_file_name)
            for table in schema.tables:
                columns = []
                for column in table.columns:
                    if not self.is_allowed_string(column.columnName):
                        raise NotAllowedCharacterException(f"Invalid column name '{column.columnName}'")    
                    elif not self.is_allowed_datatype(column.varType):
                        raise NotAllowedDatatypeException(f"Invalid datatype '{column.varType}'")
                    else:
                        columns.append(f"{column.columnName} {column.varType}")
                if not self.is_allowed_string(table.tableName):
                    raise NotAllowedCharacterException(f"Invalid table name '{table.tableName}'")
                else:
                    query = f"CREATE TABLE IF NOT EXISTS {table.tableName}({','.join(columns)});"
                    connector.cursor().execute(query)
            connector.close()

    def get_user_db_schema(self, login, db_names):
        user_db_file_names = self.get_user_db_files(login, db_names)
        return [self.__user_db_schema(login, db_file_name) for db_file_name in user_db_file_names]

    def insert_row(self, login, db_name, table_name, row: Row):
        with self.lock:
            if not self.is_allowed_string(table_name) or not self.is_allowed_string(db_name):
                raise NotAllowedCharacterException(f"Incorrect character in '{table_name}' or '{db_name}'")
            connector = sqlite3.connect(self.db_storage_path + self.get_user_db_files(login, [db_name])[0])
            cursor = connector.cursor()
            query = f"SELECT type FROM pragma_table_info(?)"
            cursor.execute(query, (table_name,))
            row_data_types = [_[0] for _ in cursor.fetchall()]
            row_to_insert = [cell.value for cell in row.row]
            if len(row_to_insert) != len(row_data_types):
                raise AppException("Too many cells in row")
            retype = {"TEXT": str,"BLOB":str,"INTEGER":int,"REAL":float}
            converted_row_to_insert = [retype[data_type.upper()](value) for data_type, value in zip(row_data_types, row_to_insert)]
            query = f"INSERT INTO {table_name} VALUES ({','.join('?' * len(row_data_types))})"
            cursor.execute(query, tuple(converted_row_to_insert))
            connector.commit()
            connector.close()

    def select_row(self, login, db_name, table_name, column=None, value=None):
        with self.lock:
            is_where_query = False
            if not self.is_allowed_string(db_name) or not self.is_allowed_string(table_name):
                raise NotAllowedCharacterException(f"Incorrect character in '{table_name}' or '{db_name}'")
            if column and value:
                is_where_query = True
                if not self.is_allowed_string(column) or not self.is_allowed_string(value):
                    raise NotAllowedCharacterException(f"Incorrect character in '{column}' or '{value}'")
            connector = sqlite3.connect(self.db_storage_path + self.get_user_db_files(login, [db_name])[0])
            cursor = connector.cursor()
            result = None
            
            if is_where_query:
                query = f"SELECT * FROM {table_name} WHERE {column}=?"
                cursor.execute(query, (value,))
                result = cursor.fetchall()
            else:
                query = f"SELECT * FROM {table_name}"
                cursor.execute(query)
                result = cursor.fetchall()
            connector.close()
            return result

    def __user_db_schema(self, login, user_db_file_name):
        with self.lock:
            connector = sqlite3.connect(self.db_storage_path + user_db_file_name)
            cursor = connector.cursor()
            query = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
            cursor.execute(query)
            tables = [index[0] for index in cursor.fetchall()]
            db_schema = DBSchema(
                db_name=user_db_file_name[len(login):-3],
                tables=[]
            )
            for table in tables:
                query = f"SELECT name, type FROM pragma_table_info(?)"
                cursor.execute(query, (table,))
                table_schema = cursor.fetchall()
                row = TableSchema(
                    table_name=table,
                    row=[]
                )
                for cell in table_schema:
                    row.row.append(
                        Cell(
                            column_name=cell[0],
                            value=cell[1]
                        )
                    )
                db_schema.tables.append(row)
            connector.close()
            return db_schema

