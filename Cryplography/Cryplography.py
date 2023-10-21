from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hmac
import argparse
import random
import sys
import os

# Pre-defined ID encryption passwords
id_passwords = {
    1: b'key1',
    2: b'key2',
    3: b'key3',
    4: b'key4',
    5: b'key5'
}

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )
    return kdf.derive(password)

# Encrypt function
def encrypt_file(input_path, output_path, password):
    id_number = random.choice(list(id_passwords.keys()))
    id_password = id_passwords[id_number]

    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()

    with open(input_path, "rb") as f_input:
        plaintext = f_input.read()

    plaintext_with_id = f"{id_number}\n".encode("utf-8") + plaintext  # Separate with newline
    ciphertext = encryptor.update(plaintext_with_id) + encryptor.finalize()

    with open(output_path, "wb") as f_output:
        f_output.write(salt + iv + ciphertext)

# Decrypt function
def decrypt_file(input_path, output_path, password):
    try:
        with open(input_path, "rb") as f_input:
            data = f_input.read()
            salt = data[:16]
            iv = data[16:32]
            ciphertext = data[32:]

        key = generate_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
        decryptor = cipher.decryptor()

        decrypted_with_id = decryptor.update(ciphertext) + decryptor.finalize()

        id_delimiter_pos = decrypted_with_id.find(b"\n")
        id_bytes = decrypted_with_id[:id_delimiter_pos]
        id_number = int(id_bytes)
        decrypted_text = decrypted_with_id[id_delimiter_pos + 1:]  # Skip the delimiter

        with open(output_path, "wb") as f_output:
            f_output.write(decrypted_text)
        print(f"Decryption successful.")

    except:
        print("An error occurred during decryption. Please check your input or password.")
        
def main():
    if len(sys.argv) < 4 or len(sys.argv) % 2 != 0:
        print("Usage: python your_script.py <encrypt/decrypt> <input1> <output1> <input2> <output2> ...")
        return

    action = sys.argv[1]
    
    if action == "encrypt":
        password = input("Enter encryption password: ").encode("utf-8")
    elif action == "decrypt":
        password = input("Enter decryption password: ").encode("utf-8")

    for i in range(2, len(sys.argv), 2):
        input_file = sys.argv[i]
        output_file = sys.argv[i + 1]

        if action == "encrypt":
            encrypt_file(input_file, output_file, password)
            print(f"Encryption successful for '{input_file}'.")

        elif action == "decrypt":
            decrypt_file(input_file, output_file, password)

if __name__ == "__main__":
    main()


