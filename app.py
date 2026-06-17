import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# --- FUNGSI KEANGGOTAAN FUZZY (UMUM) ---
# ==========================================
def bahu_kiri(x, a, b):
    if x <= a: return 1.0
    elif a < x < b: return (b - x) / (b - a)
    else: return 0.0

def segitiga(x, a, b, c):
    if x <= a or x >= c: return 0.0
    elif a < x <= b: return (x - a) / (b - a)
    elif b < x < c: return (c - x) / (c - b)

def bahu_kanan(x, a, b):
    if x <= a: return 0.0
    elif a < x < b: return (x - a) / (b - a)
    else: return 1.0

# ==========================================
# --- FUNGSI BANTUAN GRAFIK & INTERPRETASI ---
# ==========================================
def plot_grafik(x_domain, y_kiri, y_tengah, y_kanan, label_kiri, label_tengah, label_kanan, input_val, mu_kiri, mu_tengah, mu_kanan, title, xlabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_domain, y_kiri, label=label_kiri, color='blue', linewidth=2)
    ax.plot(x_domain, y_tengah, label=label_tengah, color='green', linewidth=2)
    ax.plot(x_domain, y_kanan, label=label_kanan, color='red', linewidth=2)
    
    # Menandai titik input pada grafik
    ax.axvline(x=input_val, color='black', linestyle='--', label=f'Input: {input_val}')
    ax.plot(input_val, mu_kiri, 'bo', markersize=8)
    ax.plot(input_val, mu_tengah, 'go', markersize=8)
    ax.plot(input_val, mu_kanan, 'ro', markersize=8)
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"$\mu(x)$ / Derajat Keanggotaan")
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right')
    return fig

def tampilkan_interpretasi(input_val, mu_kiri, mu_tengah, mu_kanan, label_kiri, label_tengah, label_kanan, satuan=""):
    kategori = {label_kiri: mu_kiri, label_tengah: mu_tengah, label_kanan: mu_kanan}
    status_dominan = max(kategori, key=kategori.get)
    
    st.success(f"""
    **Kesimpulan Analisis:** Berdasarkan nilai input sebesar **{input_val}{satuan}**, derajat keanggotaan terkuat berada pada kategori **{status_dominan}** dengan tingkat keyakinan (nilai $\mu$) sebesar **{kategori[status_dominan]:.2f}**.
    """)

# ==========================================
# --- KONFIGURASI KESELURUHAN HALAMAN ---
# ==========================================
st.set_page_config(page_title="Praktikum Logika Fuzzy", layout="wide")

# Sidebar Navigasi
st.sidebar.title("Navigasi Sistem")
st.sidebar.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=80)
st.sidebar.write("Silahkan pilih studi kasus di bawah ini untuk melihat luaran praktikum:")
pilihan = st.sidebar.radio("PILIH STUDI KASUS:", [
    "Kasus 1: Penilaian Mahasiswa", 
    "Kasus 2: Kelayakan Beasiswa", 
    "Kasus 3: Tingkat Kemacetan"
])

st.sidebar.divider()
st.sidebar.info("Dibuat untuk memenuhi Tugas Praktikum Logika Fuzzy (Fuzzifikasi) menggunakan Streamlit.")

# ==========================================
# === KASUS 1: PENILAIAN MAHASISWA ===
# ==========================================
if pilihan == "Kasus 1: Penilaian Mahasiswa":
    st.title("📚 Kasus 1: Sistem Penilaian Mahasiswa")
    st.write("Sistem ini digunakan untuk menentukan tingkat capaian nilai ujian mahasiswa ke dalam himpunan Fuzzy: Rendah, Sedang, atau Tinggi.")
    st.divider()

    # --- LUARAN 1: INTERFACE ---
    st.header("1. Interface Streamlit")
    x_val = st.slider("Geser untuk memasukkan Nilai Ujian mahasiswa (Domain: 0 - 100):", min_value=0, max_value=100, value=50)
    st.divider()

    # --- LUARAN 2: FUNGSI KEANGGOTAAN ---
    st.header("2. Fungsi Keanggotaan")
    st.write("Rumus matematis (Piecewise Function) yang digunakan untuk pemodelan kurva:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Himpunan Rendah (Bahu Kiri)**")
        st.latex(r'''
        \mu_{Rendah}(x) = \begin{cases} 1, & x \le 40 \\ \frac{60 - x}{60 - 40}, & 40 < x < 60 \\ 0, & x \ge 60 \end{cases}
        ''')
    with col_b:
        st.markdown("**Himpunan Sedang (Segitiga)**")
        st.latex(r'''
        \mu_{Sedang}(x) = \begin{cases} 0, & x \le 40 \text{ atau } x \ge 80 \\ \frac{x - 40}{60 - 40}, & 40 < x \le 60 \\ \frac{80 - x}{80 - 60}, & 60 < x < 80 \end{cases}
        ''')
    with col_c:
        st.markdown("**Himpunan Tinggi (Bahu Kanan)**")
        st.latex(r'''
        \mu_{Tinggi}(x) = \begin{cases} 0, & x \le 60 \\ \frac{x - 60}{80 - 60}, & 60 < x < 80 \\ 1, & x \ge 80 \end{cases}
        ''')
    st.divider()

    # Hitung nilai fuzzy di balik layar
    mu_kiri = bahu_kiri(x_val, 40, 60)
    mu_tgh = segitiga(x_val, 40, 60, 80)
    mu_kanan = bahu_kanan(x_val, 60, 80)

    # --- LUARAN 3: PERHITUNGAN DERAJAT KEANGGOTAAN ---
    st.header("3. Perhitungan Derajat Keanggotaan")
    st.write(f"Hasil nilai matematis ($\mu$) kalkulasi Fuzzifikasi dari input nilai **{x_val}**:")
    c1, c2, c3 = st.columns(3)
    c1.metric("$\mu$ Rendah", f"{mu_kiri:.2f}")
    c2.metric("$\mu$ Sedang", f"{mu_tgh:.2f}")
    c3.metric("$\mu$ Tinggi", f"{mu_kanan:.2f}")
    st.divider()

    # --- LUARAN 4: GRAFIK HIMPUNAN FUZZY ---
    st.header("4. Grafik Himpunan Fuzzy")
    x_dom = np.linspace(0, 100, 500)
    fig = plot_grafik(x_dom, [bahu_kiri(xi, 40, 60) for xi in x_dom], [segitiga(xi, 40, 60, 80) for xi in x_dom], [bahu_kanan(xi, 60, 80) for xi in x_dom],
                      "Rendah", "Sedang", "Tinggi", x_val, mu_kiri, mu_tgh, mu_kanan, "Kurva Keanggotaan Nilai Ujian", "Nilai Ujian")
    st.pyplot(fig)
    st.divider()

    # --- LUARAN 5: INTERPRETASI HASIL ---
    st.header("5. Interpretasi Hasil")
    tampilkan_interpretasi(x_val, mu_kiri, mu_tgh, mu_kanan, "Rendah", "Sedang", "Tinggi")

# ==========================================
# === KASUS 2: KELAYAKAN BEASISWA ===
# ==========================================
elif pilihan == "Kasus 2: Kelayakan Beasiswa":
    st.title("🎓 Kasus 2: Sistem Kelayakan Beasiswa")
    st.write("Sistem ini digunakan untuk memetakan Indeks Prestasi Kumulatif (IPK) ke dalam taraf kelayakan: Tidak Layak, Dipertimbangkan, atau Layak.")
    st.divider()

    # --- LUARAN 1: INTERFACE ---
    st.header("1. Interface Streamlit")
    x_val = st.slider("Geser untuk memasukkan nilai IPK mahasiswa (Domain: 0.00 - 4.00):", min_value=0.00, max_value=4.00, value=2.75, step=0.01)
    st.divider()

    # --- LUARAN 2: FUNGSI KEANGGOTAAN ---
    st.header("2. Fungsi Keanggotaan")
    st.write("Rumus matematis (Piecewise Function) yang digunakan untuk pemodelan kurva IPK:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Himpunan Tidak Layak (Bahu Kiri)**")
        st.latex(r'''
        \mu_{Tidak\ Layak}(x) = \begin{cases} 1, & x \le 1.5 \\ \frac{2.5 - x}{2.5 - 1.5}, & 1.5 < x < 2.5 \\ 0, & x \ge 2.5 \end{cases}
        ''')
    with col_b:
        st.markdown("**Himpunan Dipertimbangkan (Segitiga)**")
        st.latex(r'''
        \mu_{Dipertimbangkan}(x) = \begin{cases} 0, & x \le 1.5 \text{ atau } x \ge 3.5 \\ \frac{x - 1.5}{2.5 - 1.5}, & 1.5 < x \le 2.5 \\ \frac{3.5 - x}{3.5 - 2.5}, & 2.5 < x < 3.5 \end{cases}
        ''')
    with col_c:
        st.markdown("**Himpunan Layak (Bahu Kanan)**")
        st.latex(r'''
        \mu_{Layak}(x) = \begin{cases} 0, & x \le 2.5 \\ \frac{x - 2.5}{3.5 - 2.5}, & 2.5 < x < 3.5 \\ 1, & x \ge 3.5 \end{cases}
        ''')
    st.divider()

    # Hitung nilai fuzzy di balik layar
    mu_kiri = bahu_kiri(x_val, 1.5, 2.5)
    mu_tgh = segitiga(x_val, 1.5, 2.5, 3.5)
    mu_kanan = bahu_kanan(x_val, 2.5, 3.5)

    # --- LUARAN 3: PERHITUNGAN DERAJAT KEANGGOTAAN ---
    st.header("3. Perhitungan Derajat Keanggotaan")
    st.write(f"Hasil nilai matematis ($\mu$) kalkulasi Fuzzifikasi dari input IPK **{x_val}**:")
    c1, c2, c3 = st.columns(3)
    c1.metric("$\mu$ Tidak Layak", f"{mu_kiri:.2f}")
    c2.metric("$\mu$ Dipertimbangkan", f"{mu_tgh:.2f}")
    c3.metric("$\mu$ Layak", f"{mu_kanan:.2f}")
    st.divider()

    # --- LUARAN 4: GRAFIK HIMPUNAN FUZZY ---
    st.header("4. Grafik Himpunan Fuzzy")
    x_dom = np.linspace(0, 4, 500)
    fig = plot_grafik(x_dom, [bahu_kiri(xi, 1.5, 2.5) for xi in x_dom], [segitiga(xi, 1.5, 2.5, 3.5) for xi in x_dom], [bahu_kanan(xi, 2.5, 3.5) for xi in x_dom],
                      "Tidak Layak", "Dipertimbangkan", "Layak", x_val, mu_kiri, mu_tgh, mu_kanan, "Kurva Keanggotaan Kelayakan IPK", "IPK")
    st.pyplot(fig)
    st.divider()

    # --- LUARAN 5: INTERPRETASI HASIL ---
    st.header("5. Interpretasi Hasil")
    tampilkan_interpretasi(x_val, mu_kiri, mu_tgh, mu_kanan, "Tidak Layak", "Dipertimbangkan", "Layak")

# ==========================================
# === KASUS 3: TINGKAT KEMACETAN ===
# ==========================================
else:
    st.title("🚗 Kasus 3: Sistem Kepadatan Lalu Lintas (Kemacetan)")
    st.write("Sistem ini memodelkan kondisi jalan raya berdasarkan volume kendaraan ke dalam himpunan Fuzzy: Lancar, Padat, atau Macet.")
    st.divider()

    # --- LUARAN 1: INTERFACE ---
    st.header("1. Interface Streamlit")
    x_val = st.slider("Geser untuk memasukkan Jumlah Kendaraan di jalan (Domain: 0 - 1000):", min_value=0, max_value=1000, value=450)
    st.divider()

    # --- LUARAN 2: FUNGSI KEANGGOTAAN ---
    st.header("2. Fungsi Keanggotaan")
    st.write("Rumus matematis (Piecewise Function) yang digunakan untuk pemodelan kurva jumlah kendaraan:")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Himpunan Lancar (Bahu Kiri)**")
        st.latex(r'''
        \mu_{Lancar}(x) = \begin{cases} 1, & x \le 300 \\ \frac{500 - x}{500 - 300}, & 300 < x < 500 \\ 0, & x \ge 500 \end{cases}
        ''')
    with col_b:
        st.markdown("**Himpunan Padat (Segitiga)**")
        st.latex(r'''
        \mu_{Padat}(x) = \begin{cases} 0, & x \le 300 \text{ atau } x \ge 700 \\ \frac{x - 300}{500 - 300}, & 300 < x \le 500 \\ \frac{700 - x}{700 - 500}, & 500 < x < 700 \end{cases}
        ''')
    with col_c:
        st.markdown("**Himpunan Macet (Bahu Kanan)**")
        st.latex(r'''
        \mu_{Macet}(x) = \begin{cases} 0, & x \le 500 \\ \frac{x - 500}{700 - 500}, & 500 < x < 700 \\ 1, & x \ge 700 \end{cases}
        ''')
    st.divider()

    # Hitung nilai fuzzy di balik layar
    mu_kiri = bahu_kiri(x_val, 300, 500)
    mu_tgh = segitiga(x_val, 300, 500, 700)
    mu_kanan = bahu_kanan(x_val, 500, 700)

    # --- LUARAN 3: PERHITUNGAN DERAJAT KEANGGOTAAN ---
    st.header("3. Perhitungan Derajat Keanggotaan")
    st.write(f"Hasil nilai matematis ($\mu$) kalkulasi Fuzzifikasi dari volume kendaraan **{x_val}**:")
    c1, c2, c3 = st.columns(3)
    c1.metric("$\mu$ Lancar", f"{mu_kiri:.2f}")
    c2.metric("$\mu$ Padat", f"{mu_tgh:.2f}")
    c3.metric("$\mu$ Macet", f"{mu_kanan:.2f}")
    st.divider()

    # --- LUARAN 4: GRAFIK HIMPUNAN FUZZY ---
    st.header("4. Grafik Himpunan Fuzzy")
    x_dom = np.linspace(0, 1000, 500)
    fig = plot_grafik(x_dom, [bahu_kiri(xi, 300, 500) for xi in x_dom], [segitiga(xi, 300, 500, 700) for xi in x_dom], [bahu_kanan(xi, 500, 700) for xi in x_dom],
                      "Lancar", "Padat", "Macet", x_val, mu_kiri, mu_tgh, mu_kanan, "Kurva Keanggotaan Jumlah Kendaraan", "Jumlah Kendaraan")
    st.pyplot(fig)
    st.divider()

    # --- LUARAN 5: INTERPRETASI HASIL ---
    st.header("5. Interpretasi Hasil")
    tampilkan_interpretasi(x_val, mu_kiri, mu_tgh, mu_kanan, "Lancar", "Padat", "Macet", satuan=" kendaraan")
