def encrypt_caesar(plaintext):
    ciphertext = ''
    shift = 3
    upp = 0
    for i in range(len(plaintext)):
        f = ord(plaintext[i])
        if 64 < f < 91:
            upp = 1
        f += shift
        if f < 65:
            f += 26
        if upp == 1 and f > 90:
            f -= 26
        if upp == 0 and f < 97:
            f += 26
        if f > 122:
            f -= 26
        ciphertext += chr(f)
    return ciphertext


def decrypt_caesar(plaintext):
    ciphertext = ''
    shift = -3
    upp = 0
    for i in range(len(plaintext)):
        f = ord(plaintext[i])
        if 64 < f < 91:
            upp = 1
        f += shift
        if f < 65:
            f += 26
        if upp == 1 and f > 90:
            f -= 26
        if upp == 0 and f < 97:
            f += 26
        if f > 122:
            f -= 26
        ciphertext += chr(f)
    return ciphertext
