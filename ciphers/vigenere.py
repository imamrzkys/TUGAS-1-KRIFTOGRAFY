"""
Vigenere Cipher
Rumus Enkripsi : C_i = (P_i + K_i) mod 26
Rumus Dekripsi : P_i = (C_i - K_i) mod 26
- Keyword diulang sepanjang plaintext (hanya untuk huruf)
- Spasi dan tanda baca dipertahankan
"""

def process_vigenere(text: str, keyword: str, mode: str) -> dict:
    """
    Proses enkripsi atau dekripsi Vigenere Cipher.
    
    Args:
        text    : Teks input
        keyword : Kata kunci (hanya huruf)
        mode    : 'encrypt' atau 'decrypt'
    
    Returns:
        dict dengan result, formula, steps
    """
    keyword = keyword.upper()
    k_len = len(keyword)
    k_idx = 0          # indeks keyword hanya maju saat char adalah huruf

    result = []
    steps = []

    formula = (
        "C_i = (P_i + K_i) mod 26"
        if mode == 'encrypt'
        else "P_i = (C_i - K_i) mod 26"
    )

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p = ord(char) - base
            k_char = keyword[k_idx % k_len]
            k = ord(k_char) - ord('A')

            if mode == 'encrypt':
                c = (p + k) % 26
                new_char = chr(base + c)
                steps.append(
                    f"{char} + {k_char} → {new_char} | ({p} + {k}) mod 26 = {c}"
                )
            else:
                c = (p - k) % 26   # Python % positif
                new_char = chr(base + c)
                steps.append(
                    f"{char} − {k_char} → {new_char} | ({p} − {k}) mod 26 = {c}"
                )

            result.append(new_char)
            k_idx += 1
        else:
            result.append(char)
            steps.append(f"'{char}' → '{char}' (dipertahankan)")

    return {
        "result": "".join(result),
        "formula": formula,
        "steps": steps,
    }
