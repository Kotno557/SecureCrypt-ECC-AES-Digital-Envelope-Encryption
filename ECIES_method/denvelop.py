"""
    10911240 楊大為 資工三乙 資安第一次個人作業-3 denvelop.py
    使用時請使用 venv 進行  e.g. ./venv/Scripts/python denvelop.py alice.pri data.enc
    目的：解開信封檔 envelop.dat，並使用內藏的 random key 使用 AES-CBC 解密 data.enc。
    輸入：python denvelop.py alice.pri data.enc
    輸出：解密檔：data.decode
"""

from argparse import ArgumentParser, FileType
from ecies import decrypt
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


if __name__ == '__main__':

    # set parser and arguments
    parser = ArgumentParser()
    parser.add_argument('envelop', help='decrypt target envelop', type=FileType('rb'))
    parser.add_argument('code_data', help='decrypt target data', type=FileType('rb'))
    parser.add_argument('pri_key', help='the key', type=FileType('rb'))
    args = parser.parse_args()

    iv = args.code_data.read(16)
    cipheredData = args.code_data.read()
    envelop = args.envelop.read()
    pri_key = args.pri_key.read()

    # ecies decrypt develop use pri_key
    aes_key = decrypt(pri_key, envelop)

    # aes decrypt code_data use aes_key
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    originalData = unpad(cipher.decrypt(cipheredData), AES.block_size)
    with open('data.decode', "wb") as f:
        f.write(originalData)
