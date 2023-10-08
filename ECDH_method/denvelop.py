"""
    10911240 楊大為 資工三乙 資安第一次個人作業-3 denvelop.py
    使用時請使用 venv 進行 
    目的：解開信封檔 envelop.dat，並使用內藏的 random key 使用 AES-CBC 解密 data.enc。
    輸入：python denvelop.py alice.pri data.enc
    輸出：解密檔：data.decode
"""

from argparse import ArgumentParser, FileType
from tinyec import registry, ec
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad

def parse_tuple(s):
    return tuple(map(int,s.split(',')))

if __name__ == '__main__':

    # set parser and arguments
    parser = ArgumentParser()
    parser.add_argument('envelop', help='decrypt target envelop', type=FileType('r'))
    parser.add_argument('code_data', help='decrypt target data', type=FileType('rb'))
    parser.add_argument('pri_key', help='the key', type=FileType('rb'))
    args = parser.parse_args()

    curve = registry.get_curve('brainpoolP160r1')
    iv = args.code_data.read(16)
    cipheredData = args.code_data.read()
    pri_key = int(args.pri_key.read())
    envelopPubKeyVector = parse_tuple(args.envelop.read())
    envelopPoint = ec.Point(curve, envelopPubKeyVector[0], envelopPubKeyVector[1])


    # ECC decrypt develop use pri_key
    sharedKey = pri_key * envelopPoint
    sharedKey = str(sharedKey.x) + ',' + str(sharedKey.y)
    sharedKey = str.encode(sharedKey)
    print('共享金鑰> ',sharedKey,type(sharedKey))
    h = SHA256.new(data=sharedKey)
    print('經過SHA-256雜湊過後的共享金鑰> ',h.digest(),type(h.digest()))


    # aes decrypt code_data use aes_key
    cipher = AES.new(h.digest(), AES.MODE_CBC, iv=iv)
    originalData = unpad(cipher.decrypt(cipheredData), AES.block_size)
    with open('data.decode', "wb") as f:
        f.write(originalData)

