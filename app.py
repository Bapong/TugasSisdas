import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- FUNGSI KEANGGOTAAN UMUM ---
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

def plot_grafik(x_domain, y_kiri, y_tengah, y_kanan, label_kiri, label_tengah, label_kanan, input_val, mu_kiri, mu_tengah, mu_kanan, title, xlabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_domain, y_kiri, label=label_kiri, color='blue')
    ax.plot(x_domain, y_tengah, label=label_tengah, color='green')
    ax.plot(x_domain, y_kanan, label=label_kanan, color='red')
    
    ax.axvline(x=input_val, color='black', linestyle='--', label=f'Input: {input_val}')
    ax.plot(input_val, mu_kiri, 'bo')
    ax.plot(input_val, mu_tengah, 'go')
    ax.plot(input_val, mu_kanan, 'ro')
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("\u03BC(x)")
    ax.legend()
    return fig

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Tugas Praktikum Logika Fuzzy", layout="wide")
st.sidebar.title("Navigasi Kasus")
pilihan = st.sidebar.radio("Pilih Studi Kasus:", ["Kasus 1: Penilaian", "Kasus 2: Beasiswa", "Kasus 3: Kemacetan"])

# --- KASUS 1: PENILAIAN MAHASISWA ---
if pilihan == "Kasus 1: Penilaian":
    st.title("Kasus 1: Penilaian Mahasiswa")
    x_val = st.slider("Masukkan Nilai Ujian (0 - 100):", 0, 100, 50)
    
    mu_kiri = bahu_kiri(x_val, 40, 60)
    mu_tgh = segitiga(x_val, 40, 60, 80)
    mu_kanan = bahu_kanan(x_val, 60, 80)
    
    st.subheader("Derajat Keanggotaan")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rendah", f"{mu_kiri:.2f}")
    c2.metric("Sedang", f"{mu_tgh:.2f}")
    c3.metric("Tinggi", f"{mu_kanan:.2f}")
    
    x_dom = np.linspace(0, 100, 500)
    fig = plot_grafik(x_dom, [bahu_kiri(xi, 40, 60) for xi in x_dom], [segitiga(xi, 40, 60, 80) for xi in x_dom], [bahu_kanan(xi, 60, 80) for xi in x_dom],
                      "Rendah", "Sedang", "Tinggi", x_val, mu_kiri, mu_tgh, mu_kanan, "Fungsi Keanggotaan Nilai Ujian", "Nilai Ujian")
    st.pyplot(fig)

# --- KASUS 2: KELAYAKAN BEASISWA ---
elif pilihan == "Kasus 2: Beasiswa":
    st.title("Kasus 2: Kelayakan Beasiswa")
    x_val = st.slider("Masukkan IPK (0.00 - 4.00):", 0.00, 4.00, 2.75, step=0.01)
    
    mu_kiri = bahu_kiri(x_val, 1.5, 2.5)
    mu_tgh = segitiga(x_val, 1.5, 2.5, 3.5)
    mu_kanan = bahu_kanan(x_val, 2.5, 3.5)
    
    st.subheader("Derajat Keanggotaan")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tidak Layak", f"{mu_kiri:.2f}")
    c2.metric("Dipertimbangkan", f"{mu_tgh:.2f}")
    c3.metric("Layak", f"{mu_kanan:.2f}")
    
    x_dom = np.linspace(0, 4, 500)
    fig = plot_grafik(x_dom, [bahu_kiri(xi, 1.5, 2.5) for xi in x_dom], [segitiga(xi, 1.5, 2.5, 3.5) for xi in x_dom], [bahu_kanan(xi, 2.5, 3.5) for xi in x_dom],
                      "Tidak Layak", "Dipertimbangkan", "Layak", x_val, mu_kiri, mu_tgh, mu_kanan, "Fungsi Keanggotaan IPK", "IPK")
    st.pyplot(fig)

# --- KASUS 3: TINGKAT KEMACETAN ---
else:
    st.title("Kasus 3: Tingkat Kemacetan")
    x_val = st.slider("Masukkan Jumlah Kendaraan (0 - 1000):", 0, 1000, 450)
    
    mu_kiri = bahu_kiri(x_val, 300, 500)
    mu_tgh = segitiga(x_val, 300, 500, 700)
    mu_kanan = bahu_kanan(x_val, 500, 700)
    
    st.subheader("Derajat Keanggotaan")
    c1, c2, c3 = st.columns(3)
    c1.metric("Lancar", f"{mu_kiri:.2f}")
    c2.metric("Padat", f"{mu_tgh:.2f}")
    c3.metric("Macet", f"{mu_kanan:.2f}")
    
    x_dom = np.linspace(0, 1000, 500)
    fig = plot_grafik(x_dom, [bahu_kiri(xi, 300, 500) for xi in x_dom], [segitiga(xi, 300, 500, 700) for xi in x_dom], [bahu_kanan(xi, 500, 700) for xi in x_dom],
                      "Lancar", "Padat", "Macet", x_val, mu_kiri, mu_tgh, mu_kanan, "Fungsi Keanggotaan Jumlah Kendaraan", "Jumlah Kendaraan")
    st.pyplot(fig)
