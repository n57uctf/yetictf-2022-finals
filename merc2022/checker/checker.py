#!/usr/bin/env python3
import requests, re, sys
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
from requests_toolbelt.multipart.encoder import MultipartEncoder
from checklib import *
from random import randrange
from pathlib import Path

BASE_DIR = Path(__file__).absolute().resolve().parent

class CheckMachine:
    @property

    def url(self):
        return f'http://{self.host}:{self.port}'

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def register(self, name, passwd):
        sess = get_initialized_session()
        resp = sess.post(f'{self.url}/registration.php', data={"name": name,"passwd": passwd,"passwd_confirm": passwd,"register":""})
        check_response(resp, 'Could not register')

        return sess

    def login(self, name, passwd):
        sess = get_initialized_session()

        resp = sess.post(f'{self.url}/login.php', data={'name': name, 'passwd': passwd, 'login':""})
        check_response(resp, 'Could not login')

        return sess

    def cabinet(self, sess):
        resp = sess.get(f'{self.url}/cabinet.php')
        check_response(resp, "Can't get cabinet page")

        if re.findall(r'Your Merchant ID\: \<strong\>',resp.text):
            return(resp.text.split('Your Merchant ID: <strong>')[1].split('</strong>')[0])
        else:
            cquit(Status.MUMBLE, "Can't get a Merc ID")

    def advert(self, sess):
        resp = sess.get(f'{self.url}/advert.php?')
        check_response(resp, "Can't get advert")

        if re.findall(r'invest\.php\?merc_id=',resp.text):
            return 'ok'
        else:
            cquit(Status.MUMBLE, "Can't get a referal")

    def chat(self, sess, merc_id, name):
        message = f'note to {name}'
        sess.post(f'{self.url}/chat.php', data={'sender_id':merc_id,'receiver_id':merc_id,'message':message,'chat':''})
        resp = sess.get(f'{self.url}/chat.php')
        check_response(resp, "Can't send message")

        if re.findall(r'{}'.format(message),resp.text):
            return 'ok'
        else:
            cquit(Status.MUMBLE, "Didn't receive message")

    def parsel(self,sess,note):
        resp = sess.get(f'{self.url}/request.php')
        if re.findall(r'<select name="name"', resp.text):
            name = resp.text.split('<select name="name"')[1].split('</select>')[0].split('<option>')[-1].split('</option>')[0]
        else:
            cquit(Status.CORRUPT, 'Couldn\'t get drivers')
        dest = 'Germiston'
        disp = 'Johannesburg'

        resp = sess.post(f'{self.url}/request.php', data={'dispatch':disp,'destination':dest,'note':note,'name':name,'request':''})
        check_response(resp, "Can't get delivery page")

        resp = sess.get(f'{self.url}/cabinet.php')
        if re.findall(r'{}'.format(note),resp.text):
            return 'ok'
        else:
            return 'corrupt'

    def parsel_check(self,sess,note):

        resp = sess.get(f'{self.url}/cabinet.php')
        if re.findall(r'{}'.format(note),resp.text):
            return 'ok'
        else:
            return 'corrupt'

    def license(self, flag):

        img = PngImageFile(BASE_DIR / 'random.png')
        meta = PngInfo()
        meta.add_text("Comment", flag)
        img.save(BASE_DIR / 'license.png',pnginfo=meta)

    def driver(self, name, vehicle, bio, flag):

        self.license(flag)

        num = randrange(5)

        values = {
                'name':name,
                'vehicle':vehicle,
                'about':bio,
                'status':'0',
                'driver':'',
                 }
        files = {
                'avatar': (f'{num}.png', open(BASE_DIR / f'{num}.png','rb'), 'image/png'),
                'license': ('license.png', open(BASE_DIR / 'license.png','rb'), 'image/png')
                }

        sess = get_initialized_session()

        resp = sess.post(f'{self.url}/driver.php', data=values, files=files)
        check_response(resp, "Can't create driver")

        time.sleep(3)
        
        resp = sess.get(f'{self.url}/application.php')
        check_response(resp, "Can't get profile")

        if re.findall(r'<td><img src="image\.php\?license"', resp.text):
            driver_id = resp.text.split('<td><img src="image.php?license"')[1].split('<td>')[1].split('</td>')[0]
        else:
            cquit(Status.MUMBLE, "Can't find Driver ID")

        resp = sess.get(f'{self.url}/image.php?license')
        check_response(resp, "Can't get license")

        open(BASE_DIR / 'response.png','wb').write(resp.content)

        image_path = '/checkers/merc2022/response.png'

        if Image.open(image_path).info['Comment'] == flag:
            return driver_id
        else:
            return 'corrupt'

    def driver_profile(self,driver_id,flag):

        sess = get_initialized_session()

        resp = sess.post(f'{self.url}/driver.php',data={'driver_id':driver_id,'application':''})
        check_response(resp, "Can't get driver's profile")

        resp = sess.get(f'{self.url}/image.php?license')
        check_response(resp, "Can't get license")

        open(BASE_DIR / 'response2.png','wb').write(resp.content)

        if Image.open(BASE_DIR / 'response2.png').info['Comment'] == flag:
            return 'ok'
        else:
            return 'corrupt'

def check(host,port):

    chk = CheckMachine(host,port)

    name = rnd_username()
    passwd = rnd_password()

    chk.register(name,passwd)

    sess = chk.login(name,passwd)

    merc_id = chk.cabinet(sess)

    chk.advert(sess)
    chk.chat(sess,merc_id,name)

    cquit(Status.OK, "OK", f'{name}:{passwd}')

def put1(host,port,flag):

    chk = CheckMachine(host,port)

    name = rnd_username()
    passwd = rnd_password()

    chk.register(name,passwd)

    sess = chk.login(name,passwd)

    result = chk.parsel(sess,flag)

    if result == 'ok':
        cquit(Status.OK, f"{name}",f'{name}:{passwd}')
    else:
        cquit(Status.CORRUPT, 'Couldn\'t request delivery')

def put2(host,port,flag):

    chk = CheckMachine(host,port)

    name = rnd_username()
    vehicle = rnd_username()
    bio = rnd_username()

    result = chk.driver(name, vehicle, bio, flag)

    if result != 'corrupt':
        cquit(Status.OK, f"{name}",f'{name}:{result}')
    else:
        cquit(Status.CORRUPT, 'Couldn\'t create driver')

def get1(host,port,flag,flag_id):

    chk = CheckMachine(host,port)

    name,passwd = flag_id.strip().split(':')

    sess = chk.login(name,passwd)

    result = chk.parsel_check(sess,flag)

    if result == 'ok':
        cquit(Status.OK, "OK")
    else:
        cquit(Status.CORRUPT, 'Couldn\'t get delivery message')

def get2(host,port,flag,flag_id):

    chk = CheckMachine(host,port)

    name,driver_id = flag_id.strip().split(':')

    result = chk.driver_profile(driver_id,flag)

    if result == 'ok':
        cquit(Status.OK, "OK")
    else:
        cquit(Status.CORRUPT, 'Couldn\'t get license')

if __name__ == '__main__':

    action, *args = sys.argv[1:]

    port = '6666'

    try:
        if action == 'check':

            host, = args
            check(host, port)

        elif action == 'put':
    
            host, flag_id, flag, vuln_number = args

            if vuln_number == '1':
                put1(host, port, flag)
            else:
                put2(host, port, flag)

        elif action == 'get':
            
            host, flag_id, flag, vuln_number = args

            if vuln_number == '1':
                get1(host, port, flag, flag_id)
            else:
                get2(host, port, flag, flag_id)

        else:
            cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)

        cquit(Status.ERROR)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))
