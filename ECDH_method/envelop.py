"""
    10911240 楊大為 資工三乙 資安第一次個人作業-2 envelop.py
    使用時請使用 venv 進行
    目的：產生信封檔 envelop.dat，並使用內藏的 random key 使用 AES-CBC 加密 data.txt (預先建立好的明文文字檔，請任意貼入一則至少 100 字的新聞稿)。
    輸入：python envelop.py alice.pub data.txt
    輸出：信封檔 envelop.dat；加密檔：data.enc
    https://cryptobook.nakov.com/asymmetric-key-ciphers/ecdh-key-exchange-examples
"""

from argparse import ArgumentParser, FileType
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad

from tinyec import registry, ec
import secrets

def aes_encrypt(key, data):

    # 以金鑰搭配 CBC 模式建立 cipher 物件
    cipher = AES.new(key, AES.MODE_CBC)

    # 將輸入資料加上 padding 後進行加密
    ciphered_data = cipher.encrypt(pad(data, AES.block_size))

    # 將初始向量與密文寫入檔案
    with open('data.enc', "wb") as f:
        f.write(cipher.iv)
        f.write(ciphered_data)



def parse_tuple(s):
    return tuple(map(int,s.split(',')))


if __name__ == '__main__':

    # set parser and keys
    parser = ArgumentParser()
    parser.add_argument('pubFile', help='generate a envelop from public key {pubFile}', type=FileType('r',encoding='utf-8'))
    parser.add_argument('data', help='generate a envelop for {data}', type=FileType('rb'))
    args = parser.parse_args()

    alicePubKeyVector = parse_tuple(args.pubFile.read())
    
    curve = registry.get_curve('brainpoolP160r1')
    alicePubKey = ec.Point(curve, alicePubKeyVector[0], alicePubKeyVector[1])

    # generate a random AES key
    randomPrivKey = secrets.randbelow(curve.field.n)
    randomPubKey = randomPrivKey * curve.g

    sharedKey = randomPrivKey * alicePubKey
    sharedKey = str(sharedKey.x) + ',' + str(sharedKey.y)
    sharedKey = str.encode(sharedKey)
    print('共享金鑰> ',sharedKey,type(sharedKey))
    h = SHA256.new(data=sharedKey)
    print('經過SHA-256雜湊過後的共享金鑰> ',h.digest(),type(h.digest()))

    # do aes encrypt
    aes_encrypt(h.digest(), args.data.read())

    # do ecdh encrypt
    with open('envelop.dat', "w", encoding='utf-8') as f:
        f.write(str(randomPubKey.x) + ',' + str(randomPubKey.y))

