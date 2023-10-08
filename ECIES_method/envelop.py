"""
    10911240 楊大為 資工三乙 資安第一次個人作業-2 envelop.py
    使用時請使用 venv 進行  e.g. ./venv/Scripts/python envelop.py
    目的：產生信封檔 envelop.dat，並使用內藏的 random key 使用 AES-CBC 加密 data.txt (預先建立好的明文文字檔，請任意貼入一則至少 100 字的新聞稿)。
    輸入：python envelop.py alice.pub data.txt
    輸出：信封檔 envelop.dat；加密檔：data.enc
"""

from argparse import ArgumentParser, FileType
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from ecies import encrypt


def aes_encrypt(key, data):

    # change data to binary
    data = data.encode('utf-8')

    # 以金鑰搭配 CBC 模式建立 cipher 物件
    cipher = AES.new(key, AES.MODE_CBC)

    # 將輸入資料加上 padding 後進行加密
    ciphered_data = cipher.encrypt(pad(data, AES.block_size))

    # 將初始向量與密文寫入檔案
    with open('data.enc', "wb") as f:
        f.write(cipher.iv)
        f.write(ciphered_data)


def ecies_encrypt(receiver_public_key, key):

    # encrypt key with receiver_public_key then generate envelop.dat
    with open('envelop.dat', "wb") as f:
        f.write(encrypt(receiver_public_key, key))


if __name__ == '__main__':

    # set parser and keys
    parser = ArgumentParser()
    parser.add_argument('pubFile', help='generate a envelop from public key {pubFile}', type=FileType('rb'))
    parser.add_argument('data', help='generate a envelop for {data}', type=FileType('r', encoding='utf-8'))
    args = parser.parse_args()

    # generate a random AES key
    aes_key = get_random_bytes(32)

    # do aes encrypt
    aes_encrypt(aes_key, args.data.read())

    # do ecies encrypt
    ecies_encrypt(args.pubFile.read(), aes_key)
