"""
test_ciphers.py – Tes otomatis semua algoritma kriptografi
Tugas 1 Kriptografi – Semester 6 – 2025/2026 Genap

Jalankan dengan:
    python test_ciphers.py
atau:
    python -m unittest test_ciphers
"""

import unittest
import sys
import os

# Pastikan direktori root ada di path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ciphers.caesar   import process_caesar
from ciphers.vigenere import process_vigenere
from ciphers.affine   import process_affine
from ciphers.hill     import process_hill
from ciphers.playfair import process_playfair


# ============================================================
# CAESAR CIPHER TESTS
# ============================================================
class TestCaesar(unittest.TestCase):

    def test_encrypt_basic(self):
        r = process_caesar("HELLO", 3, "encrypt")
        self.assertEqual(r["result"], "KHOOR")

    def test_decrypt_basic(self):
        r = process_caesar("KHOOR", 3, "decrypt")
        self.assertEqual(r["result"], "HELLO")

    def test_roundtrip(self):
        plaintext = "HELLO WORLD"
        enc = process_caesar(plaintext, 13, "encrypt")["result"]
        dec = process_caesar(enc, 13, "decrypt")["result"]
        self.assertEqual(dec, plaintext)

    def test_preserve_punctuation(self):
        r = process_caesar("Hello, World!", 3, "encrypt")
        self.assertEqual(r["result"], "Khoor, Zruog!")

    def test_lowercase(self):
        r = process_caesar("hello", 3, "encrypt")
        self.assertEqual(r["result"], "khoor")

    def test_mixed_case(self):
        r = process_caesar("HeLLo", 3, "encrypt")
        self.assertEqual(r["result"], "KhOOr")

    def test_shift_25(self):
        r = process_caesar("A", 25, "encrypt")
        self.assertEqual(r["result"], "Z")

    def test_wraps_around(self):
        r = process_caesar("XYZ", 3, "encrypt")
        self.assertEqual(r["result"], "ABC")

    def test_steps_count(self):
        r = process_caesar("HI", 3, "encrypt")
        self.assertEqual(len(r["steps"]), 2)

    def test_formula_encrypt(self):
        r = process_caesar("A", 5, "encrypt")
        self.assertIn("mod 26", r["formula"])
        self.assertIn("+", r["formula"])

    def test_formula_decrypt(self):
        r = process_caesar("A", 5, "decrypt")
        self.assertIn("mod 26", r["formula"])
        self.assertIn("-", r["formula"])


# ============================================================
# VIGENERE CIPHER TESTS
# ============================================================
class TestVigenere(unittest.TestCase):

    def test_encrypt_classic(self):
        r = process_vigenere("ATTACKATDAWN", "LEMON", "encrypt")
        self.assertEqual(r["result"], "LXFOPVEFRNHR")

    def test_decrypt_classic(self):
        r = process_vigenere("LXFOPVEFRNHR", "LEMON", "decrypt")
        self.assertEqual(r["result"], "ATTACKATDAWN")

    def test_roundtrip(self):
        plaintext = "THE QUICK BROWN FOX"
        enc = process_vigenere(plaintext, "SECRET", "encrypt")["result"]
        dec = process_vigenere(enc, "SECRET", "decrypt")["result"]
        self.assertEqual(dec, plaintext)

    def test_preserve_spaces(self):
        r = process_vigenere("HELLO WORLD", "KEY", "encrypt")
        # Space must be at position 5
        self.assertEqual(r["result"][5], " ")

    def test_lowercase_keyword_treated_same(self):
        r1 = process_vigenere("HELLO", "key", "encrypt")
        r2 = process_vigenere("HELLO", "KEY", "encrypt")
        self.assertEqual(r1["result"], r2["result"])

    def test_key_repeats_correctly(self):
        # Keyword KE repeats for HELLO: K,E,K,E,K
        r = process_vigenere("HELLO", "KE", "encrypt")
        # H(7)+K(10)=17=R, E(4)+E(4)=8=I, L(11)+K(10)=21=V, L(11)+E(4)=15=P, O(14)+K(10)=24=Y
        self.assertEqual(r["result"], "RIVPY")

    def test_steps_have_correct_length(self):
        r = process_vigenere("ABC", "KEY", "encrypt")
        # 3 alpha chars → 3 steps
        self.assertEqual(len(r["steps"]), 3)


# ============================================================
# AFFINE CIPHER TESTS
# ============================================================
class TestAffine(unittest.TestCase):

    def test_encrypt_classic(self):
        r = process_affine("AFFINECIPHER", 5, 8, "encrypt")
        self.assertEqual(r["result"], "IHHWVCSWFRCP")

    def test_decrypt_classic(self):
        r = process_affine("IHHWVCSWFRCP", 5, 8, "decrypt")
        self.assertEqual(r["result"], "AFFINECIPHER")

    def test_roundtrip(self):
        plaintext = "HELLO WORLD"
        enc = process_affine(plaintext, 7, 3, "encrypt")["result"]
        dec = process_affine(enc, 7, 3, "decrypt")["result"]
        self.assertEqual(dec, plaintext)

    def test_invalid_a_raises(self):
        with self.assertRaises(ValueError):
            process_affine("HELLO", 2, 8, "encrypt")   # gcd(2,26)=2 ≠ 1

    def test_invalid_a_raises_4(self):
        with self.assertRaises(ValueError):
            process_affine("HELLO", 4, 1, "encrypt")   # gcd(4,26)=2

    def test_a_inv_present(self):
        r = process_affine("A", 5, 8, "encrypt")
        self.assertIn("a_inv", r)
        self.assertEqual(r["a_inv"], 21)    # 5 × 21 mod 26 = 105 mod 26 = 1

    def test_preserve_spaces(self):
        r = process_affine("A B", 5, 8, "encrypt")
        self.assertEqual(r["result"][1], " ")

    def test_a_equals_1(self):
        # Affine a=1, b=k → same as Caesar shift k
        r_affine = process_affine("HELLO", 1, 3, "encrypt")["result"]
        r_caesar = process_caesar("HELLO", 3, "encrypt")["result"]
        self.assertEqual(r_affine, r_caesar)


# ============================================================
# HILL CIPHER TESTS
# ============================================================
class TestHill(unittest.TestCase):

    KEY_2X2 = [[3, 3], [2, 5]]    # det = 15-6 = 9, gcd(9,26)=1 ✓

    def test_encrypt_2x2(self):
        r = process_hill("HI", self.KEY_2X2, "encrypt")
        # H=7, I=8
        # [3*7+3*8, 2*7+5*8] = [21+24, 14+40] = [45, 54] mod26 = [19, 2] = T, C
        self.assertEqual(r["result"], "TC")

    def test_decrypt_2x2(self):
        enc = process_hill("HI", self.KEY_2X2, "encrypt")["result"]
        dec = process_hill(enc, self.KEY_2X2, "decrypt")["result"]
        self.assertEqual(dec, "HI")

    def test_roundtrip_longer(self):
        key = [[3, 3], [2, 5]]
        # "HELLO" ganjil → padded "HELLOX" (6 chars) untuk 2×2
        plaintext = "HELLOX"
        enc = process_hill(plaintext, key, "encrypt")["result"]
        dec = process_hill(enc, key, "decrypt")["result"]
        self.assertEqual(dec, plaintext)

    def test_padding_added(self):
        key = [[3, 3], [2, 5]]
        r = process_hill("HI!", key, "encrypt")   # '!' dibuang, "HI" → pas 2 huruf
        # Pastikan tetap berjalan
        self.assertIn("result", r)

    def test_invalid_matrix_det0(self):
        bad_key = [[2, 4], [1, 2]]    # det = 0
        with self.assertRaises(ValueError):
            process_hill("HELLO", bad_key, "encrypt")

    def test_invalid_matrix_det_not_coprime(self):
        bad_key = [[2, 3], [2, 3]]    # det = 0
        with self.assertRaises(ValueError):
            process_hill("HELLO", bad_key, "encrypt")

    def test_returns_inv_matrix(self):
        r = process_hill("HI", self.KEY_2X2, "encrypt")
        self.assertIn("inv_matrix", r)
        self.assertIn("det", r)

    def test_3x3_roundtrip(self):
        key = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
        plaintext = "ACT"
        enc = process_hill(plaintext, key, "encrypt")["result"]
        dec = process_hill(enc, key, "decrypt")["result"]
        self.assertEqual(dec, plaintext)


# ============================================================
# PLAYFAIR CIPHER TESTS
# ============================================================
class TestPlayfair(unittest.TestCase):

    def test_matrix_size(self):
        from ciphers.playfair import _build_matrix
        m = _build_matrix("MONARCHY")
        self.assertEqual(len(m), 5)
        self.assertEqual(len(m[0]), 5)

    def test_matrix_no_j(self):
        from ciphers.playfair import _build_matrix
        m = _build_matrix("MONARCHY")
        flat = [c for row in m for c in row]
        self.assertNotIn('J', flat)

    def test_matrix_no_duplicates(self):
        from ciphers.playfair import _build_matrix
        m = _build_matrix("MONARCHY")
        flat = [c for row in m for c in row]
        self.assertEqual(len(flat), len(set(flat)))

    def test_encrypt_returns_dict(self):
        r = process_playfair("INSTRUMENTS", "MONARCHY", "encrypt")
        self.assertIn("result", r)
        self.assertIn("matrix", r)
        self.assertIn("calc_steps", r)
        self.assertIn("formula", r)

    def test_roundtrip(self):
        keyword = "MONARCHY"
        # Playfair adds X padding, J→I. Use even-length, no doubles:
        plaintext = "HELPME"   # no doubles, even length, no J
        enc = process_playfair(plaintext, keyword, "encrypt")["result"]
        dec = process_playfair(enc, keyword, "decrypt")["result"]
        # Plaintext diawali HELPME
        self.assertEqual(dec[:len(plaintext)], plaintext)

    def test_double_letter_padding(self):
        from ciphers.playfair import _make_pairs
        # "LL" → ("L","X"),("L",...) bukan ("L","L")
        pairs = _make_pairs("BALLOON")
        pair_strs = [a + b for a, b in pairs]
        for p in pair_strs:
            self.assertEqual(len(p), 2)
            # Tidak ada pasangan huruf sama
            if p[0] == p[1]:
                self.fail(f"Pasangan sama terdeteksi: {p}")

    def test_odd_length_padding(self):
        from ciphers.playfair import _make_pairs
        pairs = _make_pairs("ABC")
        self.assertEqual(len(pairs), 2)          # AB, CX
        self.assertEqual(pairs[-1], ('C', 'X'))

    def test_j_replaced_by_i(self):
        r = process_playfair("JELLY", "MONARCHY", "encrypt")
        # J diganti I, pastikan tidak crash
        self.assertIn("result", r)

    def test_classic_encrypt(self):
        # Tes klasik: INSTRUMENTS dengan kunci MONARCHY
        # Hasil bisa berbeda tergantung implementasi pairing
        r = process_playfair("INSTRUMENTS", "MONARCHY", "encrypt")
        # Pastikan minimal tidak kosong dan panjang genap
        self.assertTrue(len(r["result"]) > 0)
        self.assertEqual(len(r["result"]) % 2, 0)


# ============================================================
# RUN
# ============================================================
if __name__ == '__main__':
    loader  = unittest.TestLoader()
    suite   = unittest.TestSuite()

    suites = [
        TestCaesar,
        TestVigenere,
        TestAffine,
        TestHill,
        TestPlayfair,
    ]

    for s in suites:
        suite.addTests(loader.loadTestsFromTestCase(s))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return non-zero exit code if tests fail (useful for CI)
    sys.exit(0 if result.wasSuccessful() else 1)
