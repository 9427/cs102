def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("")
    ''
    """
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


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    shift = -3
    upp = 0
    for i in range(len(ciphertext)):
        f = ord(ciphertext[i])
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
        plaintext += chr(f)
    return plaintext
