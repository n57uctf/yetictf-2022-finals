import requests
import argparse
import json


parser = argparse.ArgumentParser()

# Зарегистрировать пользователя с лгином = (login + db_name)[:-2]
# Создать базу данных с названием = (db_name)[-2:]
# Взять свой api ключ
# Дампнуть данные из созданной бд 

# 2022-04-05 19:46:06.508037: User qwerty created databse db1

def main():
    parser.add_argument('--host', type=str, required=True, help='Remote host (ip:port)')
    parser.add_argument('--login', type=str, required=True, help='User login')
    parser.add_argument('--db', type=str, required=True, help='DB name to connect to')
    args = parser.parse_args()
    
    new_login = args.login[:-1]
    new_db_name = args.login[-1] + args.db

    creds = {"login": new_login, "password": "123"}
    r = requests.post("http://" + args.host + "/register")

    
    #r = requests.get("http://" + args.host + "/api/v1/dbs", params={"key": apikey})
    #json_response = json.loads(r.text)
    #print(json_response)


if __name__ == "__main__":
    main()