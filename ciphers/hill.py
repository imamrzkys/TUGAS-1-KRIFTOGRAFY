"""
Hill Cipher
Enkripsi : C = K × P (mod 26)
Dekripsi : P = K⁻¹ × C (mod 26)
Syarat   : det(K) ≠ 0  DAN  gcd(det(K) mod 26, 26) = 1

Implementasi manual tanpa numpy agar edukatif.
Mendukung matriks kunci 2×2 dan 3×3.
"""

import math


# ---- Operasi Matriks ----

def _determinant(m):
    """Hitung determinan matriks n×n (ekspansi kofaktor, rekursif)."""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0
    for col in range(n):
        minor = [[m[r][c] for c in range(n) if c != col]
                 for r in range(1, n)]
        det += ((-1) ** col) * m[0][col] * _determinant(minor)
    return det


def _mod_inverse(a, m):
    """Invers modular a mod m menggunakan brute-force. Kembalikan -1 jika tidak ada."""
    a = a % m
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return -1


def _matrix_inverse_mod(m, mod=26):
    """
    Hitung K⁻¹ mod 26.
    Untuk 2×2:  K⁻¹ = det⁻¹ × [[d,-b],[-c,a]]
    Untuk 3×3:  K⁻¹ = det⁻¹ × adj(K)
    Semua elemen dimod 26 dan dijaga positif.
    """
    det = _determinant(m)
    det_mod = det % mod
    det_inv = _mod_inverse(det_mod, mod)

    if det_inv == -1:
        raise ValueError(
            f"Matriks tidak dapat diinvers modulo 26 "
            f"(det mod 26 = {det_mod}, tidak coprime dengan 26)."
        )

    n = len(m)

    if n == 2:
        # Formula klasik 2×2 inverse
        a, b = m[0][0], m[0][1]
        c, d = m[1][0], m[1][1]
        raw = [[d, -b], [-c, a]]
        return [[(det_inv * raw[r][col]) % mod for col in range(2)]
                for r in range(2)]

    # n == 3 (atau umum): gunakan matriks kofaktor → transpose → kalikan det_inv
    cofactors = []
    for r in range(n):
        row_cof = []
        for c in range(n):
            minor = [[m[rr][cc] for cc in range(n) if cc != c]
                     for rr in range(n) if rr != r]
            sign = (-1) ** (r + c)
            row_cof.append(sign * _determinant(minor))
        cofactors.append(row_cof)

    # Adjugat = transpose kofaktor
    adj = [[cofactors[c][r] for c in range(n)] for r in range(n)]

    # K⁻¹ = det_inv × adj  (mod 26), pastikan positif
    return [[(det_inv * adj[r][c]) % mod for c in range(n)]
            for r in range(n)]


def _matvec_mod(m, v, mod=26):
    """Kalikan matriks m dengan vektor v, modulo mod."""
    return [sum(m[r][c] * v[c] for c in range(len(v))) % mod
            for r in range(len(m))]


# ---- Fungsi Utama ----

def process_hill(text, key_matrix, mode):
    """
    Proses enkripsi atau dekripsi Hill Cipher.

    Args:
        text       : Teks input (non-huruf diabaikan)
        key_matrix : Matriks kunci n×n (list of list int)
        mode       : 'encrypt' atau 'decrypt'

    Returns:
        dict dengan result, formula, steps, key_matrix, inv_matrix, det, det_mod, n

    Raises:
        ValueError jika matriks tidak valid
    """
    n = len(key_matrix)

    # --- Validasi matriks ---
    det = _determinant(key_matrix)
    det_mod = det % 26
    if det_mod == 0:
        raise ValueError(
            f"Determinant matriks = {det} → det mod 26 = 0. "
            "Matriks tidak valid untuk Hill Cipher."
        )
    if math.gcd(det_mod, 26) != 1:
        raise ValueError(
            f"Determinant mod 26 = {det_mod}, tidak coprime dengan 26. "
            "Pilih matriks kunci yang berbeda."
        )

    inv_matrix = _matrix_inverse_mod(key_matrix)

    # --- Preprocess teks: hanya huruf, uppercase, padding 'X' ---
    clean = [c.upper() for c in text if c.isalpha()]
    while len(clean) % n != 0:
        clean.append('X')

    working = key_matrix if mode == 'encrypt' else inv_matrix
    formula = (
        "C = K × P  (mod 26)"
        if mode == 'encrypt'
        else "P = K⁻¹ × C  (mod 26)"
    )

    result_chars = []
    steps = []

    for i in range(0, len(clean), n):
        block = clean[i:i + n]
        vec = [ord(c) - ord('A') for c in block]

        # Hitung perkalian matriks × vektor (sebelum mod, untuk ditampilkan)
        mult_raw = [sum(working[r][c] * vec[c] for c in range(n))
                    for r in range(n)]
        mod_res = [v % 26 for v in mult_raw]
        res_chars = [chr(v + ord('A')) for v in mod_res]

        result_chars.extend(res_chars)
        steps.append({
            "block":    "".join(block),
            "vector":   vec,
            "mult_res": mult_raw,
            "mod_res":  mod_res,
            "res_chars": "".join(res_chars),
        })

    return {
        "result":     "".join(result_chars),
        "formula":    formula,
        "steps":      steps,
        "key_matrix": key_matrix,
        "inv_matrix": inv_matrix,
        "det":        det,
        "det_mod":    det_mod,
        "n":          n,
    }
