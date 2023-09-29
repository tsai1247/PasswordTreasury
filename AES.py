from Crypto.Cipher import AES as OAES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import json
from base64 import b64encode, b64decode
import time
import logging
import i18n
from os import getenv
from typing import Union

logging.basicConfig(level=logging.INFO)

class AESEncrypted:
    def __init__(self, ciphertext: bytes = None, iv: bytes = None, jsonInput: str = None):
        if ciphertext is None or iv is None:
            jsonInput = json.loads(jsonInput)
            self._ciphertext = jsonInput['ciphertext']
            self._iv = jsonInput['iv']
        else:
            self._ciphertext = b64encode(ciphertext).decode('utf-8')
            self._iv = b64encode(iv).decode('utf-8')

    @property
    def ciphertext(self):
        return b64decode(self._ciphertext.encode('utf-8'))
    
    @property
    def iv(self):
        return b64decode(self._iv.encode('utf-8'))
    
    def get(self):
        return json.dumps({
            'ciphertext': self._ciphertext,
            'iv': self._iv
        })


class AES():
    def __init__(self, password, salt=None) -> None:
        self.setKey(password, salt)
        pass

    def setKey(self, password, salt=None):
        if password is None:
            self.key = get_random_bytes(32)
        else:
            if salt is None:
                salt = getenv('salt')
                if salt is None:
                    salt = get_random_bytes(32)
                    logging.info(f'新的salt為 {b64encode(salt).decode("utf-8")}')
                else:
                    salt = b64decode(salt.encode('utf-8'))

            self.key = PBKDF2(password, salt, dkLen=32)

        return self.key
    
    def encrypt(self, data: str) -> AESEncrypted:
        # 輸出的加密檔案名稱
        outputFile = 'encrypted.bin'

        # 要加密的資料（必須為 bytes）
        data = data.encode()

        # 以金鑰搭配 CBC 模式建立 cipher 物件
        cipher = OAES.new(self.key, OAES.MODE_CBC)

        # 將輸入資料加上 padding 後進行加密
        cipheredData = cipher.encrypt(pad(data, OAES.block_size))

        return AESEncrypted(cipheredData, cipher.iv)
    
    def decrypt(self, data: Union[AESEncrypted, str]):
        try:
            if type(data) is str:
                data = AESEncrypted(jsonInput=data)

            # 以金鑰搭配 CBC 模式與初始向量建立 cipher 物件
            cipher = OAES.new(self.key, OAES.MODE_CBC, iv=data.iv)

            # 解密後進行 unpadding
            originalData = unpad(cipher.decrypt(data.ciphertext), OAES.block_size)

            # 輸出解密後的資料
            return originalData.decode()
        except:
            return "************"

