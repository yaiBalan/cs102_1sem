import string
import typing as tp

ALPHABET = 26


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for symbol_pos in range(len(plaintext)):
        if not plaintext[symbol_pos].isalpha():
            ciphertext += str(plaintext[symbol_pos])
        else:
            if not plaintext[symbol_pos].isupper():
                ciphertext += str(
                    chr((ord(plaintext[symbol_pos]) - ord("a") + shift) % ALPHABET + ord("a"))
                )
            else:
                ciphertext += str(
                    chr((ord(plaintext[symbol_pos]) - ord("A") + shift) % ALPHABET + ord("A"))
                )
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for symbol_pos in range(len(ciphertext)):
        if not ciphertext[symbol_pos].isalpha():
            plaintext += str(ciphertext[symbol_pos])
            continue
        else:
            if not ciphertext[symbol_pos].isupper():
                plaintext += str(
                    chr((ord(ciphertext[symbol_pos]) - ord("a") - shift) % ALPHABET + ord("a"))
                )
            else:
                plaintext += str(
                    chr((ord(ciphertext[symbol_pos]) - ord("A") - shift) % ALPHABET + ord("A"))
                )
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    alphabet_len = len(string.ascii_lowercase)
    matches = 0
    for i in range(0, alphabet_len):
        try_plain = set(decrypt_caesar(ciphertext, i).split(" "))
        if len(try_plain & dictionary) >= matches:
            matches = len(try_plain & dictionary)
            best_shift = i
    return best_shift
