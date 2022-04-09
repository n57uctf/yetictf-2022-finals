#!/usr/bin/env python3

import sys
import requests
import enum
import typing
import random
import json
import string
import re
import json_tools

PORT = 8000
names = ('Michael', 'Christopher', 'Jessica', 'Matthew', 'Ashley', 'Jennifer', 'Joshua', 'Amanda', 'Daniel', 'David', 'James', 'Robert', 'John', 'Joseph', 'Andrew', 'Ryan', 'Brandon', 'Jason', 'Justin', 'Sarah', 'William', 'Jonathan', 'Stephanie', 'Brian', 'Nicole', 'Nicholas', 'Anthony', 'Heather', 'Eric', 'Elizabeth', 'Adam', 'Megan', 'Melissa', 'Kevin', 'Steven', 'Thomas', 'Timothy', 'Christina', 'Kyle', 'Rachel', 'Laura', 'Lauren', 'Amber', 'Brittany', 'Danielle', 'Richard', 'Kimberly', 'Jeffrey', 'Amy', 'Crystal', 'Michelle', 'Tiffany', 'Jeremy', 'Benjamin', 'Mark', 'Emily', 'Aaron', 'Charles', 'Rebecca', 'Jacob', 'Stephen', 'Patrick', 'Sean', 'Erin', 'Zachary', 'Jamie', 'Kelly', 'Samantha', 'Nathan', 'Sara', 'Dustin', 'Paul', 'Angela', 'Tyler', 'Scott', 'Katherine', 'Andrea', 'Gregory', 'Erica', 'Mary', 'Travis', 'Lisa', 'Kenneth', 'Bryan', 'Lindsey', 'Kristen', 'Jose', 'Alexander', 'Jesse', 'Katie', 'Lindsay', 'Shannon', 'Vanessa', 'Courtney', 'Christine', 'Alicia', 'Cody', 'Allison', 'Bradley')
db_names = ('main', 'application', '1c', 'test', 'api', 'database', 'info', 'particle', 'deep', 'fox', 'trench', 'jacket', 'chance', 'privilege', 'intention', 'emergency', 'mail', 'dawn', 'indication', 'distributor', 'chip', 'witness', 'norm', 'period', 'boom', 'mushroom', 'real', 'cheek', 'parameter',)
descriptions = ('test', 'sql training', 'my database', 'just fo fun',)
table_names = ('users','cars','maps','products','sales','films', 'dumb','private','public','people','clients',)
column_names = ('mail','id','number','price','color','password','description','date','message','model','year','value', 'previousValue', 'valuep', 'keyvalue', 'sqlite3bindvalue', 'sqlite3value', 'sqlite3valuedouble', 'sqlite3valueint', 'sqlite3valueint64', 'sqlite3valuetype', 'sqlite3valuenumerictype', 'sqlite3resultvalue', 'returnValue', 'hourValue', 'minuteValue', 'secondValue', 'yearValue', 'monthValue')

def get_random_name():
    ran = len(names)
    name = names[random.randint(0, ran - 1)]
    return name + str(random.randint(10000, 99999))

def get_random_word():
    try:
        r = requests.get("")
        if r.status_code != 200:
            return random.choice(column_names) + " " + random.choice(db_names)
    except:
        return random.choice(column_names) + " " + random.choice(db_names)
    words = r.text.splitlines()
    return random.choice(words)

def get_password():
    password = []
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    random.shuffle(characters)
    for i in range(20):
        password.append(random.choice(characters))
    random.shuffle(password)
    return "".join(password)

def get_json(response, validate_response=True):
    try:
        data = json.loads(response.text)
    except:
        cquit(Status.MUMBLE, f'JSON validation error on url: {response.url}',f'JSON validation error on url: {response.url}, content: {response.text}')
    if not validate_response:
        return data
    try:
        if data["success"] == True:
            return data
        else:
            cquit(Status.MUMBLE, f'Response status not success on url: {response.url}',f'Response status not success on url: {response.url}, content: {response.text}')
    except:
        cquit(Status.MUMBLE, f'Unknown response status ("success" field in response not found), url: {response.url}',f'Unknown response status ("success" field in response not found), url: {response.url}, content: {response.text}')

def check_status_code(response):
    if response.status_code != 200:
        cquit(Status.MUMBLE, f'Code {response.status_code} on url: {response.url}')
    return True

class Status(enum.Enum):
    OK = 101
    CORRUPT = 102
    MUMBLE = 103
    DOWN = 104
    ERROR = 110

    def __bool__(self):
        return self.value == Status.OK


def cquit(status: Status, public: str='', private: typing.Optional[str] = None):
    if private is None:
        private = public

    print(public, file=sys.stdout)
    print(private, file=sys.stderr)
    assert (type(status) == Status)
    sys.exit(status.value)


def check(host):
    # APP check
    # Connect 

    r = requests.get(f'http://{host}:{PORT}/')
    check_status_code(r)

    creds = {"login":get_random_name(),"password":get_password()}

    # Register

    r = requests.post(f'http://{host}:{PORT}/register', json=creds)
    check_status_code(r)
    data = get_json(r)

    # Login
    
    r = requests.post(f'http://{host}:{PORT}/login', json=creds)
    check_status_code(r)
    data = get_json(r)

    try:
        token = data["data"]["jwt"]
    except:
        cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
    
    auth_header = {'Authorization': f'Bearer {token}'}

    # Getting api key

    r = requests.get(f'http://{host}:{PORT}/api_key', headers=auth_header)
    check_status_code(r)
    data = get_json(r)

    try:
        api_key = data["data"]["apikey"]
    except:
        cquit(Status.MUMBLE, f'Can not get api key: {r.url}',f'Can not get api key: {r.url}, content: {r.text}')

    schema = {
        "name":random.choice(db_names),
        "description":random.choice(descriptions),
        "tables":[
            {
                "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                "columns":[
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    },
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    }
                ]
            },
            {
                "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                "columns":[
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"INTEGER"
                    },
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    },
                    {
                    "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                    "varType":"TEXT"
                    }
                ]
            }
        ]
    }

    # Creating new database

    r = requests.post(f'http://{host}:{PORT}/new_db', headers=auth_header, json=schema)
    check_status_code(r)
    data = get_json(r)

    # Checking last log

    r = requests.get(f'http://{host}:{PORT}/last_log', params={'seconds': 10})
    check_status_code(r)
    data = get_json(r)

    log_found = False
    try:
        for log in data['data']:
            if re.search(creds['login'], log) and re.search(schema['name'], log):
                log_found = True
    except:
        cquit(Status.MUMBLE, f'Open log not working (JSON exception): {r.url}',f'Open log not working (JSON exception): {r.url}, content: {r.text}, expected login: {creds["login"]}, expected db name: {schema["name"]}')

    if not log_found:
        cquit(Status.MUMBLE, f'Open log not working: {r.url}',f'Open log not working: {r.url}, content: {r.text}, expected login: {creds["login"]}, expected db name: {schema["name"]}')

    # Getting info about user's databases

    r = requests.get(f'http://{host}:{PORT}/dbs', headers=auth_header)
    check_status_code(r)
    data = get_json(r)
    try:
        if data['data'][0]['db_name'] != schema['name']:
            cquit(Status.MUMBLE, f'Database name changed: {r.url}',f'Database name changed: {r.url}, content: {r.text}, expected name: {schema["name"]}, recived name: {data["data"][0]["db_name"]}')
        if data['data'][0]['description'] != schema['description']:
            cquit(Status.MUMBLE, f'Database description changed: {r.url}',f'Database description changed: {r.url}, content: {r.text}, expected description: {schema["description"]}, recived description: {data["data"][0]["description"]}')
    except:
        cquit(Status.MUMBLE, f'Can not get databases (JSON exception): {r.url}',f'Can not get databases (JSON exception): {r.url}, content: {r.text}')

    # API check
    # Getting chema

    r = requests.get(f'http://{host}:{PORT}/api/v1/dbs', params={'key': api_key})
    check_status_code(r)
    data = get_json(r)

    try:
        tables = []
        is_db_was_found = False
        for db_schema in data['data']:
            if db_schema['db_name'] == schema['name']:
                is_db_was_found = True
                tables = db_schema['tables']
    except:
        cquit(Status.MUMBLE, f'Database not found in db schema (JSON exception): {r.url}',f'Database not found in db schema (JSON exception): {r.url}, content: {r.text}')

    if not is_db_was_found:
        cquit(Status.MUMBLE, f'Database not found in db schema: {r.url}',f'Database not found in db schema: {r.url}, content: {r.text}')

    try:
        expected_tables = []
        for table in schema['tables']:
            expected_cols = []
            for col in table['columns']:
                expected_cols.append({'column_name': col['columnName'], 'value': col['varType']})
            expected_tables.append({'row': expected_cols, 'table_name': table['tableName']})
    except:
        cquit(Status.MUMBLE, f'Database schema error: {r.url}',f'Database schema error (error while parsing JSON (cheker maybe crash)): {r.url}, content: {r.text}')

    try:
        result = json_tools.diff(tables, expected_tables)
    except:
        cquit(Status.MUMBLE, f'Database schema error: {r.url}',f'Database schema error (error while compare JSON (json_tool.diff not working)): {r.url}, content: {r.text}')

    if result:
        cquit(Status.MUMBLE, f'Received and expected schema do not match: {r.url}',f'Received and expected schema do not match: {r.url}, content: {r.text}, excpected: {expected_tables}, recived: {tables}, diff: {result}')
    
    # Placing data
    
    data_to_place = {
        "row": [
        
        ]
    }

    t_count = len(schema['tables'])
    selected_table = random.randint(0, t_count - 1)
    

    for col in schema['tables'][selected_table]['columns']:
        if col['varType'] == 'TEXT' or col['varType'] == 'BLOB':    
            data_to_place['row'].append({'column_name': col['columnName'], 'value': get_random_word()})
        else:
            data_to_place['row'].append({'column_name': col['columnName'], 'value': str(random.randint(0, 999999))})

    r = requests.post(f'http://{host}:{PORT}/api/v1/', params={
            'key': api_key, 
            'db': schema['name'],
            'table': schema['tables'][selected_table]['tableName']
        }, json=data_to_place)
    check_status_code(r)
    data = get_json(r)

    # Getting data from db

    r = requests.get(f'http://{host}:{PORT}/api/v1/', params={
            'key': api_key, 
            'db': schema['name'],
            'table': schema['tables'][selected_table]['tableName']
        })
    check_status_code(r)
    data = get_json(r)

    try:
        for row in data_to_place['row']:
            if row['value'] in str(data['data'][0]):
                pass
            else:
                cquit(Status.MUMBLE, f'Can not get data from database {r.url}',f'Recived data from database doesn\'t mach with placed data: {r.url}, content: {r.text}, excpected: {data_to_place}, recived: {data}')
    except:
        cquit(Status.MUMBLE, f'Can not get data from database (JSON exception): {r.url}',f'Can not get data from database (JSON exception): {r.url}, content: {r.text}, excpected: {data_to_place}, recived: {data}')
    
    cquit(Status.OK, f'OK')

def put(host, flag_id, flag, vuln_number):
    if int(vuln_number) == 1:  # first vuln
        # Placing flag to database description

        r = requests.get(f'http://{host}:{PORT}/')
        check_status_code(r)

        creds = {"login":get_random_name(),"password":get_password()}

        # Register

        r = requests.post(f'http://{host}:{PORT}/register', json=creds)
        check_status_code(r)
        data = get_json(r)

        # Login
    
        r = requests.post(f'http://{host}:{PORT}/login', json=creds)
        check_status_code(r)
        data = get_json(r)

        try:
            token = data["data"]["jwt"]
        except:
            cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
        
        auth_header = {'Authorization': f'Bearer {token}'}

        schema = {
            "name":random.choice(db_names),
            "description": flag,
            "tables":[
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                },
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"INTEGER"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                }
            ]
        }

        # Placing flag

        r = requests.post(f'http://{host}:{PORT}/new_db', headers=auth_header, json=schema)
        check_status_code(r)
        data = get_json(r)

        flag_id = str(creds).replace("\'", "\"")

        cquit(Status.OK, "OK", f'{flag_id}')

    elif int(vuln_number) in (2, 3, 4):  # second vuln
        # Placing flag in database data
        
        r = requests.get(f'http://{host}:{PORT}/')
        check_status_code(r)

        creds = {"login":get_random_name(),"password":get_password()}

        # Register

        r = requests.post(f'http://{host}:{PORT}/register', json=creds)
        check_status_code(r)
        data = get_json(r)

        # Login
    
        r = requests.post(f'http://{host}:{PORT}/login', json=creds)
        check_status_code(r)
        data = get_json(r)

        try:
            token = data["data"]["jwt"]
        except:
            cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
        
        auth_header = {'Authorization': f'Bearer {token}'}

        # Getting api key

        r = requests.get(f'http://{host}:{PORT}/api_key', headers=auth_header)
        check_status_code(r)
        data = get_json(r)

        try:
            api_key = data["data"]["apikey"]
        except:
            cquit(Status.MUMBLE, f'Can not get api key: {r.url}',f'Can not get api key: {r.url}, content: {r.text}')

        schema = {
            "name":random.choice(db_names),
            "description": random.choice(descriptions),
            "tables":[
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                },
                {
                    "tableName":random.choice(table_names) + str(random.randint(100, 999)),
                    "columns":[
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"INTEGER"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        },
                        {
                        "columnName":random.choice(column_names) + str(random.randint(100, 999)),
                        "varType":"TEXT"
                        }
                    ]
                }
            ]
        }

        # Creating database

        r = requests.post(f'http://{host}:{PORT}/new_db', headers=auth_header, json=schema)
        check_status_code(r)
        data = get_json(r)

        # Placing flag 

        data_to_place = {
            "row": [
            
            ]
        }

        t_count = len(schema['tables'])
        selected_table = random.randint(0, t_count - 1)
        

        for col in schema['tables'][selected_table]['columns']:
            if col['varType'] == 'TEXT' or col['varType'] == 'BLOB':    
                data_to_place['row'].append({'column_name': col['columnName'], 'value': flag})
            else:
                data_to_place['row'].append({'column_name': col['columnName'], 'value': str(random.randint(0, 999999))})

        r = requests.post(f'http://{host}:{PORT}/api/v1/', params={
                'key': api_key, 
                'db': schema['name'],
                'table': schema['tables'][selected_table]['tableName']
            }, json=data_to_place)
        check_status_code(r)
        data = get_json(r)

        cquit(Status.OK, "OK", f'{api_key}')

def get(host, flag_id, flag, vuln_number):

    if int(vuln_number) == 1:  # first vuln

        # Getting flag from database description

        creds = json.loads(flag_id)

        # Login

        r = requests.post(f'http://{host}:{PORT}/login', json=creds)
        check_status_code(r)
        data = get_json(r)

        try:
            token = data["data"]["jwt"]
        except:
            cquit(Status.MUMBLE, f'Can not get auth token: {r.url}',f'Can not get auth token: {r.url}, content: {r.text}')
        
        auth_header = {'Authorization': f'Bearer {token}'}

        # Getting db description and flag

        r = requests.get(f'http://{host}:{PORT}/dbs', headers=auth_header)
        check_status_code(r)
        data = get_json(r)

        if flag not in str(data):
            cquit(Status.CORRUPT, f'Couldn\'t find flag in database info')

        cquit(Status.OK, f'OK')

    elif int(vuln_number) in (2, 3, 4):  # second vuln

        # Getting flag from database data

        api_key = flag_id

        # Getting chema

        r = requests.get(f'http://{host}:{PORT}/api/v1/dbs', params={'key': api_key})
        check_status_code(r)
        data = get_json(r)
        
        dbs_data = ""

        for db in data['data']:
            for table in db['tables']:
                r = requests.get(f'http://{host}:{PORT}/api/v1/', params={
                        'key': api_key, 
                        'db': db['db_name'],
                        'table': table['table_name']
                    })
                check_status_code(r)
                get_json(r)
                dbs_data += r.text

        if flag not in dbs_data:
            cquit(Status.CORRUPT, f'Couldn\'t find flag in database')

        cquit(Status.OK, f'OK')

if __name__ == '__main__':
    action, *args = sys.argv[1:]

    try:
        if action == 'check':
            host, = args
            check(host)

        elif action =='put':
            host, flag_id, flag, vuln_number = args
            put(host, flag_id, flag, vuln_number)

        elif action == 'get':
            host, flag_id, flag, vuln_number = args
            get(host, flag_id, flag, vuln_number)
        else:
            cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)

        cquit(Status.ERROR)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))