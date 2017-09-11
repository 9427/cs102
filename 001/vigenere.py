def encrypt_vigenere(plaintext, keyword):
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
