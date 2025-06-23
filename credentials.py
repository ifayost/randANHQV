import base64
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass



def save_credentials(filename='./credentials'):
    print('\n Amazon Prime credentials\n')
    username = input(' - Username: ').encode()
    prime_pass = getpass(' - Password: ').encode()
    
    password = getpass('\nProtect credentials with password: ').encode()

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_000_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = f.encrypt(username + b'\n' + prime_pass)
    with open(filename, 'wb') as f:
        f.write(salt + b'\n' + token)
    return password

def read_credentials(password=None, filename='./credentials'):
    with open(filename, 'rb') as f:
        salt, token = f.read().split(b'\n')
    
    done = False
    while not done:
        try:
            if password is None:
                password = getpass('Enter password: ').encode()

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=1_000_000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            f = Fernet(key)
            username, password = f.decrypt(token).decode().split('\n')
            done = True
        except InvalidToken:
            print('[!] Wrong password, try again.')
            password = None
            
    return username, password


if __name__ == '__main__':
    save_credentials()
