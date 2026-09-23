import numpy as np
from sympy import Matrix

MOD = 26
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def prepare_text(text, n):
    text = ''.join(c.upper() for c in text if c.isalpha())

    while len(text) % n != 0:
        text += 'X'

    return text


def encrypt_hill(plaintext, key):
    n = key.shape[0]
    plaintext = prepare_text(plaintext, n)

    ciphertext = ""

    for i in range(0, len(plaintext), n):
        block = plaintext[i:i+n]

        # Convert letters to numbers
        vector = np.array([
            [ord(c) - 65] for c in block
        ])

        # C = K × P mod 26
        result = (key @ vector) % 26

        for value in result.flatten():
            ciphertext += chr(int(value) + 65)

    return ciphertext


def decrypt_hill(ciphertext, key):
    n = key.shape[0]

    # Find inverse of key modulo 26
    try:
        inverse_key = np.array(
            Matrix(key.tolist()).inv_mod(26)
        ).astype(int)
    except Exception:
        return "ERROR: Key matrix is not invertible modulo 26."

    plaintext = ""

    for i in range(0, len(ciphertext), n):
        block = ciphertext[i:i+n]

        vector = np.array([
            [ord(c) - 65] for c in block
        ])

        # P = K^-1 × C mod 26
        result = (inverse_key @ vector) % 26

        for value in result.flatten():
            plaintext += chr(int(value) + 65)

    return plaintext


# ==========================================
# MAIN PROGRAM
# ==========================================

print("=== Hill Cipher Tool ===")

# 3 × 3 key matrix
K = np.array([
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
])

message = input("Enter plaintext: ")

print("\nKey Matrix:")
print(K)

print("\nPlaintext:", message)

encrypted = encrypt_hill(message, K)
print("[+] Encrypted Text:", encrypted)

decrypted = decrypt_hill(encrypted, K)
print("[+] Decrypted Text:", decrypted)