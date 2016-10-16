from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto import Random

class AESCipher(object):
    def __init__(self, key):
	if len(key) > 32:
            self.key = key[:32]
        else:
            self.key = key.ljust(32, '0')

    #function to encrypt all messages sent
    # returns iv+E(message)+MAC
    def encrypt(self, plain_text):

        iv = Random.new().read(AES.block_size)
        #generate new AES cipher in CBC mode
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        #generate new Mac
        mac = HMAC.new(self.key)
        #pad message to 16 byte blocks
        mod = len(plain_text)%16
        to_pad = 16-mod
        multiple = ((len(plain_text)-mod)/16)+1
        message = plain_text.ljust(multiple*16, '\0')

        #encrypt message
        cipher_text = cipher.encrypt(message)

        #calculate MAC
        mac.update(cipher_text)
        return iv + cipher_text + mac.hexdigest()

    #decrypt all messages
    #returns plaintext
    def decrypt(self, cipher_text):
        #get iv and mac from cipher text
        iv = cipher_text[:16]
        if len(iv) != 16:
            raise ValueError('IV not 16 bytes')
        sent_mac = cipher_text[-32:]

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        #decrypt message
        plain_text = cipher.decrypt(cipher_text[16:-32])

        #unpad message
        for i in range(len(plain_text)-1, 0, -1):
            if plain_text[i] != '\x00':
                plain_text = plain_text[:i+1]
                break

        #get MAC from sent cipher text
        calc_mac = HMAC.new(self.key)
        calc_mac.update(cipher_text[16:-32])

        #check newly calc MAC is same as sent MAC
        if sent_mac != calc_mac.hexdigest():
            raise ValueError('MAC is not the same.')

        return plain_text
