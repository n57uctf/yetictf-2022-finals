#!/usr/bin/env python3

import sys
import random
import string
import re
import time

from pwnlib.tubes.remote import remote

PORT = 7777

OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110

def verdict(code, public="", private=""):
    if public:
        print(public)
    if private:
        print(private, file=sys.stderr)
    print('Exit with code {}'.format(code), file=sys.stderr)
    exit(code)

def connect(host):
    try:
        r = remote(host, PORT)
        return r
    except Exception as e:
        verdict(DOWN, "Connection error")

def get_cmds():
    return random.sample(range(1, 3), 2)

def get_rand_str():
    n = random.randint(10, 20)
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k = n))
    return str(rand)

def sign_up(r, need_exit):
    try:
        login = str.encode(get_rand_str())
        pas = str.encode(get_rand_str())
        email = str.encode(get_rand_str() + "@gmail.com")

        r.sendline(b"2")
        r.recvuntil(b"Login: ")
        r.sendline(login)

        r.recvuntil(b"Password: ")
        r.sendline(pas)

        r.recvuntil(b"Email: ")
        r.sendline(email)

        r.recvuntil(b"> ")

        if need_exit:
            r.sendline(b"5")
            r.recvuntil(b"> ")

        return login, pas, email

    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Sign up failed")

def sign_in(r, login, pas):
    try:
        r.sendline(b"1")
        r.recvuntil(b"Login: ")
        r.sendline(login)

        r.recvuntil(b"Password: ")
        r.sendline(pas)

        r.recvuntil(b"> ")

    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Sign in failed")

def forgot_password(r, login):
    try:
        r.sendline(b"3")
        r.recvuntil(b"Login: ")
        r.sendline(login)

        r.recvuntil(b"Code: ")

        code = str(random.randint(1000, 9999))

        r.sendline(str.encode(code))

        r.recvuntil(b"Code: ")
        r.sendline(b"0")

        r.recvuntil(b"> ")

    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Forgot password failed")

def blackjack_get_number(s):
    array = re.findall(r'[0-9]+', s)
    return int(array[0])

def check_game_blackjack(r, game_count):
    for i in range(0, game_count):
        try:
            r.sendline(b"1")
            r.recvuntil(b"> ")
            r.sendline(b"1")

            count = 0

            while(count != 10):
                answer = str(r.recvuntil(b"> "))
                if "win" in answer:
                    break

                if "Sum of cards now:" in answer:
                    s = re.findall(r'Sum of cards now: [0-9]+', answer)
                    if blackjack_get_number(s[0]) <= 17:
                        r.sendline(b"n")
                    else:
                        r.sendline(b"y")

                else:
                    verdict(MUMBLE, "Blackjack logic error")

                count += 1

            if count == 10:
                verdict(MUMBLE, "Endless loop in blackjack O_o")

        except Exception as ex:
            r.close()
            verdict(MUMBLE, "Check blackjack failed")

def check_game_poker(r):
    try:
        r.sendline(b"1")
        r.recvuntil(b"> ")
        r.sendline(b"2")

        r.recvuntil(b"> ")
        r.sendline(b"b")
        r.recvuntil(b"> ")

        wager = str(random.randint(100, 500))
        r.sendline(str.encode(wager))

        answer = str(r.recvuntil(b"> "))
        if "Example" in answer:
            r.sendline(b"0")
            r.recvuntil(b"> ")
            r.recvuntil(b"> ")

            r.sendline(b"f")
            r.recvuntil(b"> ")
            return

        r.sendline(b"f")

        r.recvuntil(b"> ")

    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Check poker failed")

def check_games(r):
    game_num = random.randint(0, 1)
    game_count = random.randint(1, 3)

    if game_num:
        check_game_poker(r)
        check_game_blackjack(r, game_count)
    else:
        check_game_blackjack(r, game_count)
        check_game_poker(r)

def check_show_commands(r, login, email):
    try:
        r.sendline(b"3")

        answer = str(r.recvuntil(b"> "))

        if (login not in answer) or (email not in answer):
            verdict(MUMBLE, "Show profile failed")

        r.sendline(b"4")

        answer = str(r.recvuntil(b"> "))

        if login not in answer:
            verdict(MUMBLE, "Show players failed")

    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Check show commands failed")

def set_purse(r, flag):
    try:
        r.sendline(b"2")
        r.recvuntil(b"purse: ")
        r.sendline(flag)

        r.recvuntil(b"> ")

    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Set purse failed")

def check_purse(r, flag):
    try:
        r.sendline(b"3")
        answer = str(r.recvuntil(b"> "))
        if flag not in answer:
            verdict(MUMBLE, "Get flag failed")

    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Check purse failed")

def leave(r):
    try:
        r.sendline(b"5")
        r.recvuntil(b"> ")
        r.sendline(b"4")
    except Exception as ex:
        r.close()
        verdict(MUMBLE, "Leave failed")
