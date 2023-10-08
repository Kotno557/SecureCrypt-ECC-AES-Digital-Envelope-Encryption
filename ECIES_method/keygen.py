"""
    10911240 楊大為 資工三乙 資安第一次個人作業-1 keygen.py
    使用時請使用 venv 進行  e.g. ./venv/Scripts/python keygen.py david
    目的：產生 Alice 的金鑰對
    輸入：python keygen.py alice
    輸出：公鑰檔案：alice.pub；私鑰檔案：alice.pri
"""

from ecies.utils import generate_key
from argparse import ArgumentParser


if __name__ == '__main__':

    # set parser
    parser = ArgumentParser()
    parser.add_argument('name', help='generate a ECC public/private key for {name}')

    # parse name and create an ECC crypto
    name = parser.parse_args().name
    key = generate_key()

    # generate public key file
    f = open(f'{name}.pub', 'wb')
    f.write(key.public_key.format(True))
    f.close()

    # generate private key file
    f = open(f'{name}.pri', 'wb')
    f.write(key.secret)
    f.close()
