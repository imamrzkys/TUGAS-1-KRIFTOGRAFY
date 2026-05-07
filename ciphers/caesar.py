"""
Caesar Cipher
Rumus Enkripsi : C = (P + k) mod 26
Rumus Dekripsi : P = (C - k) mod 26
- Huruf besar/kecil diproses dengan benar
- Spasi dan tanda baca dipertahankan
"""

def process_caesar(text: str, shift: int, mode: str) -> dict:
    """
    Proses enkripsi atau dekripsi Caesar Cipher.
    
    Args:
        text  : Teks input
        shift : Nilai geser (1-25)
        mode  : 'encrypt' atau 'decrypt'
    
    Returns:
        dict dengan result, formula, steps
    """
    result = []
    steps = []

    # Tentukan arah geser berdasarkan mode
    k = shift if mode == 'encrypt' else -shift
    formula = (
        f"C = (P + {shift}) mod 26"
        if mode == 'encrypt'
        else f"P = (C - {shift}) mod 26"
    )

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p = ord(char) - base
            c = (p + k) % 26          # Python % selalu positif untuk hasil mod
            new_char = chr(base + c)

            result.append(new_char)
            steps.append(
                f"{char} ({p:2d}) → {new_char} ({c:2d}) | ({p} {'+' if k >= 0 else ''}{k}) mod 26 = {c}"
            )
        else:
            result.append(char)
            steps.append(f"'{char}' → '{char}' (dipertahankan)")

    return {
        "result": "".join(result),
        "formula": formula,
        "steps": steps,
    }
