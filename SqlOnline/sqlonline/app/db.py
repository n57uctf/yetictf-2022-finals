from datetime import datetime

import sqlite3
import re
from typing import List
from threading import Lock

from app.models import User, DataBase
from app.exceptions import AppException, NotAllowedCharacterException


class AppDB(object):
    def __init__(self, path: str) -> None:
        self.connector = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.connector.cursor()
        self.create_all()
        self.lock = Lock()
        self.allowed_characters = r'[^a-zA-Z0-9.]'

    def is_allowed_string(self, string):
        characher_regex = re.compile(self.allowed_characters)
        string = characher_regex.search(string)
        return not bool(string)

    def create_all(self):
        query = """
        CREATE TABLE IF NOT EXISTS Users (
	        id integer PRIMARY KEY AUTOINCREMENT,
	        login text UNIQUE,
	        password_hash text,
	        api_key text
        );
        """
        self.cursor.execute(query)
        query = """
        CREATE TABLE IF NOT EXISTS DataBases (
	        id integer PRIMARY KEY AUTOINCREMENT,
	        db_name text,
	        owner integer,
	        table_count integer,
	        create_date integer,
            description text,
            FOREIGN KEY(owner) REFERENCES Users(id)
        );
        """
        self.cursor.execute(query)
        self.connector.commit()

    def create_user(self, user: User):
        with self.lock:
            if not self.is_allowed_string(user.login):
                raise NotAllowedCharacterException('Not allowed character in login')
            query = """INSERT INTO Users(login,password_hash,api_key) VALUES(?,?,?)"""
            self.cursor.execute(query, (user.login, user.password_hash, user.api_key))
            self.connector.commit()


    def create_user_db(self, database: DataBase):
        with self.lock:
            if not self.is_allowed_string(database.db_name):
                raise NotAllowedCharacterException('Not allowed character in db name')
            query = """INSERT INTO DataBases(db_name,owner,table_count,create_date,description) VALUES(?,?,?,?,?)"""
            self.cursor.execute(query, (database.db_name, database.owner, database.table_count, database.create_date, database.description,))
            self.connector.commit()


    def select_user(self, id=None, login=None, api_key=None):
        with self.lock:    
            if login:
                query = """
                    SELECT * FROM Users WHERE login=?
                """
                self.cursor.execute(query, (login,))
                result = self.cursor.fetchone()
            else:
                raise AppException("Incorrect param")
            return User(
                id=result[0],
                login=result[1],
                password_hash=result[2],
                api_key=result[3]
            )

    def select_db_creation_log(self, seconds: int) -> List:
        with self.lock:
            query = """select login, db_name from (select * from DataBases left join users on users.id=DataBases.owner where DataBases.create_date>?)"""
            self.cursor.execute(query,(int(datetime.now().timestamp()) - seconds,))
            result = self.cursor.fetchall()
            return [f"{str(datetime.now())}: User {tup[0]} created databse {tup[1]}" for tup in result]

    def select_user_api_key(self, login: str) -> str:
        with self.lock:
            query = """SELECT api_key FROM Users WHERE login=?"""
            self.cursor.execute(query, (login,))
            result = self.cursor.fetchone()
            return result[0]
    
    def select_user_dbs(self, login: str = None, api_key: str = None) -> List[DataBase]:
        with self.lock:
            if api_key:
                query = """SELECT * FROM DataBases WHERE owner=(SELECT id FROM Users WHERE api_key=?)"""
                self.cursor.execute(query, (api_key,))
            elif login:
                query = """SELECT * FROM DataBases WHERE owner=(SELECT id FROM Users WHERE login=?)"""
                self.cursor.execute(query, (login,))
            else:
                raise AppException("No arguments")
            result = self.cursor.fetchall()
            return [DataBase(
                id=data[0],
                db_name=data[1],
                owner=data[2],
                table_count=data[3],
                create_date=str(datetime.fromtimestamp(data[4])),
                description=data[5],
            ) for data in result]

    def select_login_by_api_key(self, login):
        with self.lock:
            query = "SELECT login FROM Users WHERE api_key=?"
            self.cursor.execute(query, (login,))
            result = self.cursor.fetchone()
            return result[0]