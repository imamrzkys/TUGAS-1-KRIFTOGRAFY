/**
 * Aurora Glass CryptoLab – main.js
 * Tugas 1 Kriptografi – Semester 6 – 2025/2026 Genap
 */

'use strict';

document.addEventListener('DOMContentLoaded', function () {

    /* =====================================================
       1. THEME TOGGLE
       ===================================================== */
    const html        = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');

    const savedTheme = localStorage.getItem('cryptolab-theme') || 'dark';
    applyTheme(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const next = html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem('cryptolab-theme', next);
        });
    }

    function applyTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        const icon  = themeToggle ? themeToggle.querySelector('i') : null;
        const label = themeToggle ? themeToggle.querySelector('.theme-label') : null;
        if (icon)  icon.className = theme === 'dark' ? 'fa-solid fa-moon me-1' : 'fa-solid fa-sun me-1';
        if (label) label.textContent = theme === 'dark' ? 'Dark' : 'Light';
    }

    /* =====================================================
       2. ALGORITHM SELECTOR – show/hide key inputs
       ===================================================== */
    const algoSelect = document.getElementById('algorithm');
    const keyGroups  = document.querySelectorAll('.key-group');

    function showAlgoGroup(algo) {
        keyGroups.forEach(function (g) { g.classList.add('d-none'); });
        const target = document.getElementById('group-' + algo);
        if (target) target.classList.remove('d-none');
        // Re-generate matrix ONLY when user switches TO hill from another algo
        // (server-side already rendered it on page load)
    }

    if (algoSelect) {
        algoSelect.addEventListener('change', function () {
            const selected = this.value;
            showAlgoGroup(selected);
            // Generate matrix fresh when switching TO hill
            if (selected === 'hill') generateHillMatrix();
        });
        // Show current algo on page load (server already rendered hill inputs)
        showAlgoGroup(algoSelect.value);
    }

    /* =====================================================
       3. HILL MATRIX – dynamic size change
       ===================================================== */
    const hillSizeSelect      = document.getElementById('hill_size');
    const hillMatrixContainer = document.getElementById('hill-matrix-container');

    // Defaults for each size
    const DEFAULTS = {
        2: [[3, 3], [2, 5]],
        3: [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    };

    if (hillSizeSelect) {
        hillSizeSelect.addEventListener('change', generateHillMatrix);
    }

    function generateHillMatrix() {
        if (!hillSizeSelect || !hillMatrixContainer) return;

        const size     = parseInt(hillSizeSelect.value, 10) || 2;
        const defaults = DEFAULTS[size] || DEFAULTS[2];

        // Clear previous inputs
        hillMatrixContainer.innerHTML = '';
        hillMatrixContainer.style.gridTemplateColumns = 'repeat(' + size + ', 58px)';

        for (var r = 0; r < size; r++) {
            for (var c = 0; c < size; c++) {
                var inp       = document.createElement('input');
                inp.type      = 'number';
                inp.className = 'matrix-input-cell';
                inp.name      = 'hill_' + size + 'x' + size + '_' + r + '_' + c;
                inp.id        = inp.name;
                inp.value     = defaults[r][c];
                inp.required  = true;
                inp.setAttribute('aria-label', 'Baris ' + r + ' Kolom ' + c);
                hillMatrixContainer.appendChild(inp);
            }
        }
    }

    /* =====================================================
       4. COPY RESULT BUTTON
       ===================================================== */
    var copyBtn = document.getElementById('copyBtn');

    if (copyBtn) {
        copyBtn.addEventListener('click', function () {
            var text = (this.getAttribute('data-clipboard-text') || '').trim();
            if (!text) {
                showToast('Tidak ada teks untuk disalin.', 'warning');
                return;
            }
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(text)
                    .then(onCopySuccess)
                    .catch(function () { fallbackCopy(text); });
            } else {
                fallbackCopy(text);
            }
        });
    }

    function fallbackCopy(text) {
        var ta        = document.createElement('textarea');
        ta.value      = text;
        ta.style.cssText = 'position:fixed;opacity:0;left:-9999px;top:0;';
        document.body.appendChild(ta);
        ta.focus();
        ta.select();
        try {
            document.execCommand('copy');
            onCopySuccess();
        } catch (_) {
            showToast('Gagal menyalin teks.', 'error');
        }
        document.body.removeChild(ta);
    }

    function onCopySuccess() {
        showToast('Hasil disalin ke clipboard! ✓', 'success');
        var label = document.getElementById('copyBtnLabel');
        if (label) {
            var original = label.textContent;
            label.textContent = 'Copied!';
            setTimeout(function () { label.textContent = original; }, 2000);
        }
    }

    /* =====================================================
       5. TOAST NOTIFICATIONS
       ===================================================== */
    function showToast(message, type) {
        var palette = {
            success: { color: '#10b981', icon: 'fa-circle-check' },
            error:   { color: '#ef4444', icon: 'fa-circle-xmark' },
            warning: { color: '#f59e0b', icon: 'fa-triangle-exclamation' },
            info:    { color: '#3b82f6', icon: 'fa-circle-info' }
        };
        var p = palette[type] || palette.info;

        var toast = document.createElement('div');
        toast.className = 'ag-toast';
        toast.style.borderColor = p.color;
        toast.innerHTML =
            '<i class="fa-solid ' + p.icon + '" style="color:' + p.color + ';flex-shrink:0"></i>' +
            '<span>' + message + '</span>';
        document.body.appendChild(toast);

        setTimeout(function () {
            toast.style.animation = 'toast-out 0.3s ease forwards';
            setTimeout(function () {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 350);
        }, 2800);
    }

    /* =====================================================
       6. CLEAR BUTTON
       ===================================================== */
    var clearBtn  = document.getElementById('clearBtn');
    var textInput = document.getElementById('text');

    if (clearBtn) {
        clearBtn.addEventListener('click', function () {
            if (textInput) textInput.value = '';

            var resets = {
                caesar_shift:     '3',
                vigenere_keyword: 'KEY',
                affine_a:         '5',
                affine_b:         '8',
                playfair_keyword: 'MONARCHY'
            };
            Object.keys(resets).forEach(function (id) {
                var el = document.getElementById(id);
                if (el) el.value = resets[id];
            });

            // Reset Hill matrix to defaults
            if (hillSizeSelect) {
                hillSizeSelect.value = '2';
                generateHillMatrix();
            }

            if (textInput) textInput.focus();
            showToast('Form dikosongkan.', 'info');
        });
    }

    /* =====================================================
       7. FORM SUBMIT – loading state + lightweight validation
       ===================================================== */
    var form      = document.getElementById('cryptoForm');
    var submitBtn = document.getElementById('submitBtn');

    if (form && submitBtn) {
        form.addEventListener('submit', function (e) {
            // Validate: text not empty
            var text = document.getElementById('text');
            if (!text || !text.value.trim()) {
                e.preventDefault();
                showToast('Teks tidak boleh kosong!', 'warning');
                if (text) text.focus();
                return;
            }

            // Validate: Affine a coprime 26
            var algo = document.getElementById('algorithm');
            if (algo && algo.value === 'affine') {
                var aEl = document.getElementById('affine_a');
                var a   = aEl ? parseInt(aEl.value, 10) : NaN;
                if (!isNaN(a) && gcd(Math.abs(a), 26) !== 1) {
                    e.preventDefault();
                    showToast('Nilai a harus coprime dengan 26!', 'error');
                    return;
                }
            }

            // Validate: Hill matrix inputs exist and are numbers
            if (algo && algo.value === 'hill') {
                var sizeEl  = document.getElementById('hill_size');
                var size    = sizeEl ? parseInt(sizeEl.value, 10) : 2;
                var missing = false;
                for (var ri = 0; ri < size && !missing; ri++) {
                    for (var ci = 0; ci < size && !missing; ci++) {
                        var cellName = 'hill_' + size + 'x' + size + '_' + ri + '_' + ci;
                        var cell     = document.querySelector('[name="' + cellName + '"]');
                        if (!cell || cell.value.trim() === '' || isNaN(parseInt(cell.value, 10))) {
                            missing = true;
                        }
                    }
                }
                if (missing) {
                    e.preventDefault();
                    showToast('Isi semua elemen matriks Hill dengan angka!', 'error');
                    return;
                }
            }

            // Show loading state
            var lblEl = submitBtn.querySelector('.btn-label');
            var spnEl = submitBtn.querySelector('.btn-spinner');
            if (lblEl) lblEl.textContent = 'Processing…';
            if (spnEl) spnEl.classList.remove('d-none');
            submitBtn.disabled = true;
        });
    }

    function gcd(a, b) { return b === 0 ? a : gcd(b, a % b); }

    /* =====================================================
       8. AUTO-UPPERCASE keyword inputs
       ===================================================== */
    ['vigenere_keyword', 'playfair_keyword'].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', function () {
                var pos  = this.selectionStart;
                this.value = this.value.toUpperCase();
                this.setSelectionRange(pos, pos);
            });
        }
    });

}); // end DOMContentLoaded
