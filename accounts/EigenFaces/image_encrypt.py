import base64
from os import urandom, listdir 
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


def keygen(pwd=b"password"):
    salt = urandom(16)
    pwd = pwd.encode(encoding = 'UTF-8')
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=390000,backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(pwd))
    with open("key.txt", "wb") as keywriter:
        keywriter.write(key)


def load_key():
    with open("key.txt", "rb") as keyreader:
        key = keyreader.read()
    return key


def encrypt(filepath, pwd=b"password"):
    if "key.txt" not in listdir():
        keygen(pwd)
    
    key = load_key()

    f = Fernet(key)

    with open(filepath, "rb") as image:
        b = image.read()
     
    data = f.encrypt(b)

    dot_idx = filepath.index(".")
    wo_type = filepath[:dot_idx]
    write_file = wo_type + "_enc.txt"

    with open(write_file, "wb") as eimage:
        eimage.write(data)

    return write_file


def decrypt(filepath, pwd=b"password", image=True):
    if "key.txt" not in listdir():
        keygen(pwd)
    
    key = load_key()

    f = Fernet(key)

    with open(filepath, "rb") as image:
        b = image.read()
     
    data = f.decrypt(b)

    dot_idx = filepath.index(".")
    wo_enc_and_type = filepath[:dot_idx -4]

    write_file = wo_enc_and_type + ".jpg" if image else wo_enc_and_type + ".txt"

    with open(write_file, "wb") as dimage:
        dimage.write(data)

    return write_file


if __name__ == "__main__":
    # test code
    path = "pic.jpg"
    pwd = b"stephen > krzysztof"
    output = encrypt(path, pwd)
    print(output)
    dec_path = decrypt(output, pwd)
    print(dec_path)
