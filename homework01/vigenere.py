def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    for i in range(len(plaintext)):
        j = i % len(keyword)
        f = ord(plaintext[i])
        if 64 < f < 91:
            upp = 1
        else:
            upp = 0
        if upp == 1:
            f = f + ord(keyword[j]) - 65
        else:
            f = f + ord(keyword[j]) - 97
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


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    for i in range(len(ciphertext)):
        j = i % len(keyword)
        f = ord(ciphertext[i])
        if 64 < f < 91:
            upp = 1
        else:
            upp = 0
        if upp == 1:
            f = f - ord(keyword[j]) + 65
        else:
            f = f - ord(keyword[j]) + 97
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
