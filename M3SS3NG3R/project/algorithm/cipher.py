import hashlib

class cipher(object):
	"""docstring for cipher"""
	def __init__(self):
		super(cipher, self).__init__()
		self.key = ''

	def setOptions(self, SenderName, RecipientName):
		hash = hashlib.sha256()
		for i in range(ord(SenderName[0])):
			hash.update(bytes(SenderName, 'utf-8'))
			hash.update(bytes(RecipientName, 'utf-8'))
		self.key = hash.hexdigest()


	def encrypt(self, message):
		if type(message) == str:
			return self.bleza(message, 0) if self.key!='' else '' 
		if type(message) == bytes:
			message = str(message)[2:-1]
			return self.bleza(message, 0) if self.key!='' else '' 
		return ''

	def decrypt(self, message):
		if type(message) == str:
			return self.bleza(message, 1) if self.key!='' else '' 
		if type(message) == bytes:
			message = str(message)[2:-1]
			return self.bleza(message, 1) if self.key!='' else '' 
		return ''

	def bleza(self, message, flag):
		k = 0
		encrypt_messege = ''
		for item in message:
			encrypt_messege += chr((ord(item)+ord(self.key[k%len(self.key)])*((-1)if flag else(1)))%55295)  
			k += 1
		return encrypt_messege