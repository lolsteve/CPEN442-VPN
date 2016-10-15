from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto import Random

class AESCipher(object):
    def __init__(self, key):
        if len(key) > 32:
            self.key = key[:32]
        else:
            self.key = key.ljust(32, '0')

    def encrypt(self, plain_text):
        print "lets encrypt the msg"
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        mac = HMAC.new(self.key)

        mod = len(plain_text)%16
        to_pad = 16-mod
        multiple = ((len(plain_text)-mod)/16)+1
        message = plain_text.ljust(multiple*16, '\0')
        cipher_text = cipher.encrypt(message)

        mac.update(cipher_text)

        return iv + cipher_text + mac.hexdigest()

    def decrypt(self, cipher_text):
        iv = cipher_text[:16]
        sent_mac = cipher_text[-32:]

        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(cipher_text[16:-32])

        for i in range(len(plain_text)-1, 0, -1):
            if plain_text[i] != '\x00':
                plain_text = plain_text[:i+1]
                break

        calc_mac = HMAC.new(self.key)
        calc_mac.update(cipher_text[16:-32])

        if sent_mac != calc_mac.hexdigest():
            raise ValueError('MAC is not the same. You are being listened too!')

        return plain_text
