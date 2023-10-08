"""
    10911240 楊大為 資工三乙 資安第一次個人作業-1 keygen.py
    使用時請使用 venv 進行
    目的：產生 Alice 的金鑰對
    輸入：python keygen.py alice
    輸出：公鑰檔案：alice.pub；私鑰檔案：alice.pri
"""
from argparse import ArgumentParser

from tinyec import registry, ec
import secrets


if __name__ == '__main__':

    # set parser
    parser = ArgumentParser()
    parser.add_argument('name', help='generate a ECC public/private key for {name}')

    # parse name
    name = parser.parse_args().name

    # create keypair
    curve = registry.get_curve('brainpoolP160r1')
    alicePrivKey = secrets.randbelow(curve.field.n)
    alicePubKey= alicePrivKey  * curve.g
    print("Alice public key:", alicePubKey)
    print("Alice PrivKey key:", alicePrivKey)
    
    # generate public key file
    f = open(f'{name}.pub', 'w',encoding='utf-8')
    f.write(str(alicePubKey.x))
    f.write(',')
    f.write(str(alicePubKey.y))
    f.close()

    # generate private key file
    f = open(f'{name}.pri', 'w',encoding='utf-8')
    f.write(str(alicePrivKey))
    f.close()
    
    test = ec.Point(curve, alicePubKey.x , alicePubKey.y)
