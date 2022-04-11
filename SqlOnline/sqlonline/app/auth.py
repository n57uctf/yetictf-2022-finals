import jwt
import hashlib
import requests

from app.exceptions import AppException
from app.logger import Log4j


def get_auth_token(login: str):
    try:
        with open("jwtRS256.key", "r") as private_key_file:
            private_key = private_key_file.read()
            return jwt.encode(
                {"login": login}, 
                private_key,
                algorithm="RS256",
                headers={"jku": "http://127.0.0.1:8000/pub_key"}
            )
    except Exception as e:
        raise AppException("Private key file not found")

def hash_sha256(data: str):
    return hashlib.sha256(data.encode()).hexdigest()

def verify_hash(hash_string: str, data: str):
    return hashlib.sha256(data.encode()).hexdigest() == hash_string

def generate_api_key(login: str, password: str):
    return hash_sha256(login + password * (len(login) >> len(password)))

def verify_auth_token(token: str):
    try:
        headers = jwt.get_unverified_header(token)
        jku = headers["jku"]
        r = requests.get(jku)
        public_key = r.text
        return jwt.decode(token, public_key, algorithms=["RS256", "RS384", "RS512", "HS256", "HS384", "HS512"])
    except Exception as e:
        Log4j.error(f"JWT exception: {str(type(e))}: {str(e)}")
        raise AppException("Public key file not found")
