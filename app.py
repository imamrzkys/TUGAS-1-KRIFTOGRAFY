"""
Aplikasi Web Simulasi Kriptografi Klasik
Tugas 1 Kriptografi - Semester 6 - 2025/2026 Genap
"""

import os
import traceback
from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import datetime

from ciphers.caesar import process_caesar
from ciphers.vigenere import process_vigenere
from ciphers.affine import process_affine
from ciphers.hill import process_hill
from ciphers.playfair import process_playfair

# ---- App Setup ----
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "aurora-glass-kripto-dev-key-2025")

# ==================== ROUTES ====================

@app.route('/', methods=['GET'])
def index():
    """Halaman utama simulator."""
    return render_template('index.html',
                           algo=None, mode=None, text='',
                           result_data=None, request_form={})


@app.route('/process', methods=['POST'])
def process():
    """Proses enkripsi/dekripsi dan kembalikan hasil ke halaman utama."""
    algo = request.form.get('algorithm', '').strip()
    mode = request.form.get('mode', '').strip()
    text = request.form.get('text', '').strip()

    # --- Validasi dasar ---
    if not text:
        flash("Teks tidak boleh kosong!", "danger")
        return render_template('index.html',
                               algo=algo, mode=mode, text='',
                               result_data=None, request_form=request.form)

    if mode not in ('encrypt', 'decrypt'):
        flash("Mode harus Encrypt atau Decrypt.", "danger")
        return render_template('index.html',
                               algo=algo, mode=mode, text=text,
                               result_data=None, request_form=request.form)

    result_data = None
    key_summary = ""

    try:
        # ---- Caesar ----
        if algo == 'caesar':
            shift_raw = request.form.get('caesar_shift', '').strip()
            if not shift_raw or not shift_raw.lstrip('-').isdigit():
                raise ValueError("Caesar shift harus berupa angka.")
            shift = int(shift_raw)
            if not 1 <= shift <= 25:
                raise ValueError("Caesar shift harus antara 1 sampai 25.")
            result_data = process_caesar(text, shift, mode)
            key_summary = f"Shift: {shift}"

        # ---- Vigenere ----
        elif algo == 'vigenere':
            keyword = request.form.get('vigenere_keyword', '').strip()
            if not keyword:
                raise ValueError("Vigenere keyword tidak boleh kosong.")
            if not keyword.isalpha():
                raise ValueError("Vigenere keyword hanya boleh berisi huruf A-Z.")
            result_data = process_vigenere(text, keyword, mode)
            key_summary = f"Keyword: {keyword.upper()}"

        # ---- Affine ----
        elif algo == 'affine':
            a_raw = request.form.get('affine_a', '').strip()
            b_raw = request.form.get('affine_b', '').strip()
            if not a_raw or not b_raw:
                raise ValueError("Nilai a dan b harus diisi.")
            if not a_raw.lstrip('-').isdigit() or not b_raw.lstrip('-').isdigit():
                raise ValueError("Nilai a dan b harus berupa angka bulat.")
            result_data = process_affine(text, int(a_raw), int(b_raw), mode)
            key_summary = f"a={a_raw}, b={b_raw}"

        # ---- Hill ----
        elif algo == 'hill':
            size_raw = request.form.get('hill_size', '2')
            if size_raw not in ('2', '3'):
                raise ValueError("Ukuran matriks Hill harus 2 atau 3.")
            matrix_size = int(size_raw)
            key_matrix = []
            for i in range(matrix_size):
                row = []
                for j in range(matrix_size):
                    val_raw = request.form.get(f'hill_{matrix_size}x{matrix_size}_{i}_{j}', '').strip()
                    if not val_raw or not val_raw.lstrip('-').isdigit():
                        raise ValueError(f"Elemen matriks [{i}][{j}] harus berupa angka.")
                    row.append(int(val_raw))
                key_matrix.append(row)
            result_data = process_hill(text, key_matrix, mode)
            key_summary = f"Matrix {matrix_size}x{matrix_size}"

        # ---- Playfair ----
        elif algo == 'playfair':
            keyword = request.form.get('playfair_keyword', '').strip()
            if not keyword:
                raise ValueError("Playfair keyword tidak boleh kosong.")
            if not keyword.isalpha():
                raise ValueError("Playfair keyword hanya boleh berisi huruf A-Z.")
            result_data = process_playfair(text, keyword, mode)
            key_summary = f"Keyword: {keyword.upper()}"

        else:
            flash("Algoritma tidak dikenali. Pilih salah satu dari daftar.", "danger")
            return render_template('index.html',
                                   algo=algo, mode=mode, text=text,
                                   result_data=None, request_form=request.form)

        # --- Simpan ke history ---
        _save_history(algo, mode, text, key_summary, result_data['result'])

        return render_template('index.html',
                               result_data=result_data,
                               algo=algo, mode=mode, text=text,
                               request_form=request.form)

    except ValueError as ve:
        flash(str(ve), "danger")
    except Exception as e:
        flash(f"Terjadi kesalahan tak terduga: {str(e)}", "danger")
        traceback.print_exc()

    # Kembali ke form dengan input tetap
    return render_template('index.html',
                           algo=algo, mode=mode, text=text,
                           result_data=None, request_form=request.form)


@app.route('/history', methods=['GET'])
def history():
    """Halaman riwayat enkripsi/dekripsi."""
    return render_template('history.html',
                           history=session.get('history', []))


@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Hapus semua riwayat dari session."""
    session.pop('history', None)
    flash("Riwayat berhasil dihapus.", "success")
    return redirect(url_for('history'))


# ==================== HELPERS ====================

def _save_history(algo, mode, text, key_summary, result):
    """Simpan item ke session history (maks 20)."""
    if 'history' not in session:
        session['history'] = []

    item = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'algorithm': algo,
        'mode': mode,
        'text': text[:80] + ('…' if len(text) > 80 else ''),
        'key_summary': key_summary,
        'result': result
    }
    session['history'].insert(0, item)
    if len(session['history']) > 20:
        session['history'] = session['history'][:20]
    session.modified = True


# ==================== ENTRY POINT ====================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
