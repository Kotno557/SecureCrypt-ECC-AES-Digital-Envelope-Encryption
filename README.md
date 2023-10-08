# SecureCrypt-ECC-AES-Digital-Envelope-Encryption

使用 ECC ECDH 加密方式:

※ 橢圓曲線選用brainpoolP160r1，基點設為G，以下計算都使用橢圓曲線的數學原理

※ Alice 公鑰為一座標，儲存格式為”{X座標},{Y座標}”，私鑰為一整數，儲存格式為”{整數}”

1. keygen.py 產生一隨機整數 a 作為 Alice 的私鑰，計算公鑰 A = a * G，依照上方提示儲存金鑰格式。
2. envelop.py 產生一隨機整數 b 做為一隨機私鑰，計算共享金鑰 S = b * G (根據 共享金鑰 S = a * b * G)，因為共享金鑰長度不符合AES的金鑰標準，所以這邊用 SHA256 將共享金鑰 Hash 至可於AES加密的長度，並用此金鑰加密data.exe(一個有關伊隆·馬斯克的BBC新聞)，輸出加密後的密文data.enc與 b的公鑰B (B = b * G) envelop.dat。
3. denvelop.py 使用Alice的私鑰與信封中的公鑰B解出共享金鑰S，因S = a * b * G，並使用此座標用 SHA256 Hash成 AES解密金鑰，解密data.enc。
