"""
Affine Cipher
Rumus Enkripsi : C = (a*P + b) mod 26
Rumus Dekripsi : P = a^(-1) * (C - b) mod 26
Syarat        : gcd(a, 26) = 1  (agar a punya invers modulo 26)
"""

import math


def _mod_inverse(a: int, m: int) -> int:
    """
    Cari invers modular a mod m menggunakan brute-force.
    Mengembalikan -1 jika tidak ada.
    """
    a = a % m
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return -1


def process_affine(text: str, a: int, b: int, mode: str) -> dict:
    """
    Proses enkripsi atau dekripsi Affine Cipher.
    
    Args:
        text : Teks input
        a    : Koefisien pengali  (harus coprime dengan 26)
        b    : Koefisien pergeser
        mode : 'encrypt' atau 'decrypt'
    
    Returns:
        dict dengan result, formula, steps, a_inv
    
    Raises:
        ValueError jika a tidak coprime dengan 26
    """
    if math.gcd(a, 26) != 1:
        valid = [x for x in range(1, 26) if math.gcd(x, 26) == 1]
        raise ValueError(
            f"Nilai a={a} tidak valid. Harus coprime dengan 26 (gcd(a,26)=1). "
            f"Nilai yang valid: {valid}"
        )

    a_inv = _mod_inverse(a, 26)

    formula = (
        f"C = ({a}·P + {b}) mod 26"
        if mode == 'encrypt'
        else f"P = {a_inv}·(C − {b}) mod 26  [karena {a}⁻¹ mod 26 = {a_inv}]"
    )

    result = []
    steps = []

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p = ord(char) - base

            if mode == 'encrypt':
                c = (a * p + b) % 26
                new_char = chr(base + c)
                steps.append(
                    f"{char} ({p}) → {new_char} ({c}) | ({a}×{p}+{b}) mod 26 = {c}"
                )
            else:
                c = (a_inv * (p - b)) % 26
                new_char = chr(base + c)
                steps.append(
                    f"{char} ({p}) → {new_char} ({c}) | {a_inv}×({p}−{b}) mod 26 = {c}"
                )

            result.append(new_char)
        else:
            result.append(char)
            steps.append(f"'{char}' → '{char}' (dipertahankan)")

    return {
        "result": "".join(result),
        "formula": formula,
        "steps": steps,
        "a_inv": a_inv,
    }
