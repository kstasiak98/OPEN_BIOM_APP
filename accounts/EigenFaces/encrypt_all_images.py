from image_encrypt import encrypt
import os

PASSWORD = 'Test'

folders = os.listdir('Images')
for f in folders:
    images = os.listdir(f'Images/{f}')
    for i in images:
        if not i.endswith('_enc.txt'):
            encrypt(f'Images/{f}/{i}', PASSWORD)
            os.remove(f'Images/{f}/{i}')
