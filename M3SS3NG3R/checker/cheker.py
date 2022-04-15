#!/usr/bin/env python3
import sys
import requests
import enum
import typing
import random

port = 8004

def random_line(l: int = -1):
	if l == -1:
		l = random.randint(8,20)
	s = ''
	for _ in range(l):
		t = random.randint(48,127)
		while chr(t) == '>' or chr(t) == '<':
			t = random.randint(48,127)
		s += chr(t)
	return s

class Status(enum.Enum):
	OK = 101
	CORRUPT = 102
	MUMBLE = 103
	DOWN = 104
	ERROR = 110

	def __bool__(self):
		return self.value == Status.OK

def cquit(status: Status, public: str='', private: typing.Optional[str] = None):
	print()
	if private is None:
		private = public

	print(public, file=sys.stdout)
	print(private, file=sys.stderr)
	assert (type(status) == Status)
	sys.exit(status.value)


def check(host):
	# check pages
	r = requests.get(f'http://{host}:{port}/')
	if r.status_code != 200:
		cquit(Status.DOWN, f'Code {r.status_code} on url {r.url}') 
	r = requests.get(f'http://{host}:{port}/api/user/sign-up')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on url {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on url {r.url}')

	#check sig-up
	log1 = random_line()
	pass1 = random_line()
	r = requests.post(f'http://{host}:{port}/api/user/sign-up', data = {'login':log1, 'passwrd':pass1})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on sig-up_1 {r.url}')

	log2 = random_line()
	pass2 = random_line()
	r = requests.post(f'http://{host}:{port}/api/user/sign-up', data = {'login':log2, 'passwrd':pass2})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on sig-up_2 {r.url}')

	#check sig-in
	r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log1, 'password':pass1})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on sig-in_1 {r.url}')

	# check pages
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages/all-users')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check logout_1 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check logout_1 {r.url}')
	
	#check logout
	r = requests.get(f'http://{host}:{port}/api/user/log-out')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on logout_1 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages/all-users')
	if r.text.find('<h1 class="text-center sign-wrap-4"><div class="sign_word"><span>400</span></div></h1>') == -1:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check logout_1 {r.url}')	

	#check send messege
	r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log1, 'password':pass1})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on sig-in_1 {r.url}')

	mes1 = random_line(30)
	r = requests.post(f'http://{host}:{port}/api/user/sign-in/messages', data = {'recipientName':log2, 'message':mes1})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on mes 1 to 2 {r.url}')

	r = requests.get(f'http://{host}:{port}/api/user/log-out')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on logout_1 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages/all-users')
	if r.text.find('<h1 class="text-center sign-wrap-4"><div class="sign_word"><span>400</span></div></h1>') == -1:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check logout_1 {r.url}')	

	r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log2, 'password':pass2})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on sig-in_2 {r.url}')

	mes2 = random_line(30)
	r = requests.post(f'http://{host}:{port}/api/user/sign-in/messages', data = {'recipientName':log1, 'message':mes2})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on mes 2 to 1 {r.url}')

	#check get messege
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check mes 1 to 2 {r.url}')
	#item = r.text.find(mes1[0:10])
	#print(r.text[item:item+50], mes1, sep='\n')
	res = r.text.find(mes1)
	if res == -1:
		cquit(Status.MUMBLE, f"Can't take mes 1")
	r = requests.get(f'http://{host}:{port}/api/user/log-out')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on logout_2 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages/all-users')
	if r.text.find('<h1 class="text-center sign-wrap-4"><div class="sign_word"><span>400</span></div></h1>') == -1:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check logout_1 {r.url}')	

	r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log1, 'password':pass1})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on sig-in_1 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check mes 1 to 2 {r.url}')
	res = r.text.find(mes2)
	#item = r.text.find(mes2[0:10])
	#print(r.text[item:item+50], mes2, sep='\n')
	if res == -1:
		cquit(Status.MUMBLE, f"Can't take mes 2")
	r = requests.get(f'http://{host}:{port}/api/user/log-out')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on logout_1 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages/all-users')
	if r.text.find('<h1 class="text-center sign-wrap-4"><div class="sign_word"><span>400</span></div></h1>') == -1:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check logout_1 {r.url}')		
	
	#check all users (with new user)
	r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log1, 'password':pass1})
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on sig-in_1 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages/all-users')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on {r.url}')

	res = r.text.find(log1)
	if res == -1:
		cquit(Status.MUMBLE, f"Can't take user1")
	res = r.text.find(log2)
	if res == -1:
		cquit(Status.MUMBLE, f"Can't take user1")

	r = requests.get(f'http://{host}:{port}/api/user/log-out')
	if r.status_code != 200:
		cquit(Status.MUMBLE, f'Code {r.status_code} on logout_1 {r.url}')
	r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages/all-users')
	if r.text.find('<h1 class="text-center sign-wrap-4"><div class="sign_word"><span>400</span></div></h1>') == -1:
		cquit(Status.MUMBLE, f'Code {r.status_code} on check logout_1 {r.url}')	

	cquit(Status.OK, 'OK')

def put(host, flag_id, flag, vuln_number):
	if vuln_number == 1:
		log1 = flag_id[0:10]
		pass1 = flag
		r = requests.post(f'http://{host}:{port}/api/user/sign-up', data = {'login':log1, 'passwrd':pass1})
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on sig-up_flag {r.url}')

		cquit(Status.OK, "OK")

	if vuln_number == 2:
		log1 = flag_id[0:10]
		pass1 = flag_id[10:20]
		r = requests.post(f'http://{host}:{port}/api/user/sign-up', data = {'login':log1, 'passwrd':pass1})
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on sig-up1_flag {r.url}')

		log2 = flag_id[20:30]
		pass2 = flag_id[30:40]
		r = requests.post(f'http://{host}:{port}/api/user/sign-up', data = {'login':log2, 'passwrd':pass2})
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on sig-up2_flag {r.url}')

		r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log1, 'password':pass1})
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on sig-in_1 {r.url}')
		
		r = requests.post(f'http://{host}:{port}/api/user/sign-in/messages', data = {'recipientName':log2, 'message':flag})
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on mes 1 to 2 {r.url}')

		r = requests.get(f'http://{host}:{port}/api/user/log-out')
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on logout_1 {r.url}')

		cquit(Status.OK, "OK")

def get(host, flag_id, flag, vuln_number):

	if vuln_number == 1:
		log1 = flag_id[0:10]
		pass1 = flag
		r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log1, 'password':pass1})
		if r.status_code != 200:
			cquit(Status.CORRUPT, f'Code {r.status_code} on sig-in1_flag {r.url}')
		else:
			r = requests.get(f'http://{host}:{port}/api/user/log-out')
			if r.status_code != 200:
				cquit(Status.MUMBLE, f'Code {r.status_code} on logout_1 {r.url}')
			cquit(Status.OK, f'OK')

	if vuln_number == 2:
		log2 = flag_id[20:30]
		pass2 = flag_id[30:40]
		r = requests.post(f'http://{host}:{port}/api/user/sign-in', data = {'login':log2, 'password':pass2})
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on sig-in2_flag {r.url}')

		r = requests.get(f'http://{host}:{port}/api/user/sign-in/messages')
		if r.status_code != 200:
			cquit(Status.MUMBLE, f'Code {r.status_code} on check mes 1 to 2 {r.url}')
		res = r.text.find(flag)
		if res == -1:
			cquit(Status.CORRUPT, f"Can't take mes 2")
			r = requests.get(f'http://{host}:{port}/api/user/log-out')
			if r.status_code != 200:
				cquit(Status.MUMBLE, f'Code {r.status_code} on logout_1 {r.url}')
		else:
			cquit(Status.OK, f'OK')



if __name__ == '__main__':
	action, *args = sys.argv[1:]
	#print(sys.argv[1:])
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