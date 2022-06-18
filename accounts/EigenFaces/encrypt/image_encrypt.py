import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def make_fernet(pwd=b"password"):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=390000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(pwd))
    return Fernet(key)


def encrypt(filepath, pwd=b"password", f=None):
    if f is None:
        f = make_fernet(pwd)

    with open(filepath, "rb") as image:
        b = image.read()
     
    data = f.encrypt(b)

    dot_idx = filepath.index(".")
    wo_type = filepath[:dot_idx]
    write_file = wo_type + "_enc.txt"

    with open(write_file, "wb") as eimage:
        eimage.write(data)

    return f, write_file


def decrypt(filepath, pwd=b"password", f=None, image=True):
    if f is None:
        f = make_fernet(pwd)

    with open(filepath, "rb") as image:
        b = image.read()
     
    data = f.decrypt(b)

    dot_idx = filepath.index(".")
    wo_enc_and_type = filepath[:dot_idx -4]

    write_file = wo_enc_and_type + ".jpg" if image else wo_enc_and_type + ".txt"

    with open(write_file, "wb") as dimage:
        dimage.write(data)

    return f, write_file


# test code
path = "pic.jpg"
pwd = b"stephen > krzysztof"
(f, enc_path) = encrypt(path, pwd)
decrypt(enc_path, pwd, f)
