Your target company tried to transfer a secret html document to another node, but you was able to catch the data.  Your task to find out what is the secret. You know they used a really old crypto solution, so you confidently say you will be able to decrypt.

The encrypter code is the following:

from Crypto.Util.Padding import pad

BLOCK_SIZE = 8
key = b'???'
f = open("secret.html", "rb")
plaintext = pad(f.read(),BLOCK_SIZE)
message = b''

key_it = 0
for c in plaintext:
    message += bytes([c ^ key[key_it]])
    key_it = (key_it + 1) % BLOCK_SIZE

import base64
print(base64.b64encode(message))

The catched informations is the following:

b'DmMhH3YTbjF3Yg0kWCsJaw4qET1ZZ1sAXCVYclApFV84fg01VCMJaw42DCRZIgkyVyEXNUEzC05GKxE8UHk9XR0qADFReT1dUC0BKQtNPV1CfDE4UGdUDlYnRTlGZxA1QgAVG1hxbRhgMSITXw1RRhx+SiALTT1dHSAKNEx5PV0dKhE9WXk1Yw=='