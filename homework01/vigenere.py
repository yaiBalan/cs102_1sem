ALPHABET = 26


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for position in range(len(plaintext)):
        if not plaintext[position].isalpha():
            ciphertext += plaintext[position]
        else:
            if not plaintext[position].isupper():
                move = ord(keyword[position % len(keyword)]) - ord("a")
                ciphertext += str(
                    chr(((ord(plaintext[position]) + move - ord("a")) % ALPHABET + ord("a")))
                )
            else:
                move = ord(keyword[position % len(keyword)]) - ord("A")
                ciphertext += str(
                    chr(((ord(plaintext[position]) + move - ord("A")) % ALPHABET + ord("A")))
                )
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for position in range(len(ciphertext)):
        if not ciphertext[position].isalpha():
            plaintext += ciphertext[position]
        else:
            if not ciphertext[position].isupper():
                move = ord(keyword[position % len(keyword)]) - ord("a")
                plaintext += chr(
                    (ord(ciphertext[position]) - move - (ord("a") - ALPHABET)) % ALPHABET + ord("a")
                )
            else:
                move = ord(keyword[position % len(keyword)]) - ord("A")
                plaintext += chr(
                    (ord(ciphertext[position]) - move - (ord("A") - ALPHABET)) % ALPHABET + ord("A")
                )
    return plaintext
