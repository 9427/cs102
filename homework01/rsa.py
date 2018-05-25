import random


def is_prime(n):
    """
    Tests to see if a number is prime.

    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(4)
    False
    >>> is_prime(5)
    True
    >>> is_prime(6)
    False
    >>> is_prime(25)
    False
    >>> is_prime(8)
    False
    >>> is_prime(49)
    False
    >>> is_prime(1111)
    False
    """
    if (n == 2) or (n == 3):
        return True
    elif (n < 5) or (n % 2 == 0) or (n % 3 == 0):
        return False
    i = 5
    f = 0
    while i <= sqrt(n):
        if n % i == 0:
            return False
        if f == 0:
            i += 2
            f = 1
        else:
            i += 4
            f = 0
    return True


def sqrt(n):
    i = 1
    while i * i < n:
        i += 1
    return i


def gcd(a, b):
    """
    Euclid's algorithm for determining the greatest common divisor.

    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a


def multiplicative_inverse(e, phi):
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.

    >>> multiplicative_inverse(7, 40)
    23
    """
    i = 0
    a = [[0, 0, 0, 0, 0]]
    if e > phi:
        a[0][0] = e
        a[0][1] = phi
    else:
        a[0][0] = phi
        a[0][1] = e
    a[0][2] = a[0][0] // a[0][1]
    while a[i][1] > 1:
        a.append([0, 0, 0, 0, 0])
        i += 1
        a[i][0] = a[i-1][1]
        a[i][1] = a[i-1][0] % a[i-1][1]
        a[i][2] = a[i][0] // a[i][1]
    a[i][3] = 0
    a[i][4] = 1
    while i > 0:
        i -= 1
        a[i][3] = a[i+1][4]
        a[i][4] = a[i+1][3] - (a[i+1][4] * a[i][2])
    return a[0][4] % a[0][0]


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
