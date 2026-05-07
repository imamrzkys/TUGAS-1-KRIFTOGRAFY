"""
Playfair Cipher
Aturan grid 5×5 (I dan J digabung).
- Enkripsi: same row → geser kanan, same col → geser bawah, rectangle → tukar kolom
- Dekripsi: same row → geser kiri,  same col → geser atas,  rectangle → tukar kolom
"""


def _build_matrix(keyword: str) -> list[list[str]]:
    """
    Bangun matriks 5×5 Playfair dari keyword.
    J diganti I. Duplikasi dihilangkan. Sisa diisi alphabet.
    """
    kw = keyword.upper().replace('J', 'I')
    seen = set()
    matrix_flat = []
    for ch in kw:
        if ch.isalpha() and ch not in seen:
            matrix_flat.append(ch)
            seen.add(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            matrix_flat.append(ch)
            seen.add(ch)
    return [matrix_flat[r * 5:(r + 1) * 5] for r in range(5)]


def _pos(matrix: list[list[str]], ch: str) -> tuple[int, int]:
    """Cari posisi (baris, kolom) karakter di matriks."""
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == ch:
                return r, c
    raise ValueError(f"Karakter '{ch}' tidak ditemukan di matriks Playfair.")


def _make_pairs(clean: str) -> list[tuple[str, str]]:
    """
    Buat pasangan dua huruf dengan aturan:
    - Jika dua huruf sama dalam satu pasangan, sisipkan 'X'
    - Jika sisa ganjil di akhir, tambah 'X'
    """
    pairs = []
    i = 0
    while i < len(clean):
        a = clean[i]
        if i + 1 >= len(clean):
            pairs.append((a, 'X'))
            i += 1
        elif clean[i + 1] == a:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, clean[i + 1]))
            i += 2
    return pairs


def process_playfair(text: str, keyword: str, mode: str) -> dict:
    """
    Proses enkripsi atau dekripsi Playfair Cipher.
    
    Args:
        text    : Teks input
        keyword : Kata kunci untuk membangun matriks 5×5
        mode    : 'encrypt' atau 'decrypt'
    
    Returns:
        dict dengan result, formula, matrix, calc_steps
    """
    matrix = _build_matrix(keyword)

    # Preprocess teks: uppercase, huruf saja, J→I
    clean = "".join(
        ch.upper().replace('J', 'I') for ch in text if ch.isalpha()
    )

    pairs = _make_pairs(clean)

    result_chars = []
    calc_steps = []

    for (a, b) in pairs:
        ra, ca = _pos(matrix, a)
        rb, cb = _pos(matrix, b)

        if ra == rb:
            # Same Row: geser kanan (encrypt) / kiri (decrypt)
            rule = "Same Row"
            if mode == 'encrypt':
                na = matrix[ra][(ca + 1) % 5]
                nb = matrix[rb][(cb + 1) % 5]
            else:
                na = matrix[ra][(ca - 1) % 5]
                nb = matrix[rb][(cb - 1) % 5]
        elif ca == cb:
            # Same Column: geser bawah (encrypt) / atas (decrypt)
            rule = "Same Column"
            if mode == 'encrypt':
                na = matrix[(ra + 1) % 5][ca]
                nb = matrix[(rb + 1) % 5][cb]
            else:
                na = matrix[(ra - 1) % 5][ca]
                nb = matrix[(rb - 1) % 5][cb]
        else:
            # Rectangle: tukar kolom
            rule = "Rectangle"
            na = matrix[ra][cb]
            nb = matrix[rb][ca]

        result_chars.append(na)
        result_chars.append(nb)
        calc_steps.append({
            "pair": f"{a}{b}",
            "pos1": f"({ra},{ca})",
            "pos2": f"({rb},{cb})",
            "rule": rule,
            "result": f"{na}{nb}",
        })

    formula = (
        "Encrypt: same row→kanan | same col→bawah | rectangle→tukar kolom"
        if mode == 'encrypt'
        else "Decrypt: same row→kiri  | same col→atas   | rectangle→tukar kolom"
    )

    return {
        "result": "".join(result_chars),
        "formula": formula,
        "matrix": matrix,
        "calc_steps": calc_steps,
    }
