#!/usr/bin/env python3

import random
import sys

import api

import time

def get(*args):
    host, flag_id, flag = args[:3]
    login, pas, flag = flag_id.strip().split(":")

    r = api.connect(host)

    api.sign_in(r, str.encode(login), str.encode(pas))

    api.check_purse(r, flag)

    api.leave(r)

    r.close()

    api.verdict(api.OK)

def put(*args):
    host, flag_id, flag = args[:3]

    r = api.connect(host)

    login, pas, email = api.sign_up(r, False)

    api.set_purse(r, str.encode(flag))

    api.leave(r)

    r.close()

    login = login.decode("utf-8")
    pas = pas.decode("utf-8")

    flag_id = f"{login}:{pas}:{flag}"
    api.verdict(api.OK, private = flag_id)

def check(*args):
    host = args[0]

    r = api.connect(host)

    login, pas, email = api.sign_up(r, True)

    sign_in_cmd = random.randint(0, 1)

    if (sign_in_cmd):
        api.sign_in(r, login, pas)
    else:
        api.forgot_password(r, login)
        api.sign_in(r, login, pas)

    api.check_show_commands(r, login.decode("utf-8"), email.decode("utf-8"))

    api.check_games(r)

    api.leave(r)

    r.close()

    api.verdict(api.OK)

def error_arg(*args):
    api.verdict(api.CHECKER_ERROR, private = "Wrong command {}".format(sys.argv[1]))

def init(*args):
    api.verdict(OK)

def info(*args):
    api.verdict(OK, "vulns: 1")

COMMANDS = {
    'put': put,
    'check': check,
    'get': get,
    'info': info,
    'init': init
}

if __name__ == "__main__":
    try:
        COMMANDS.get(sys.argv[1])(*sys.argv[2:])
    except Exception as ex:
        api.verdict(api.CHECKER_ERROR, private="INTERNAL ERROR: {}".format(ex))
