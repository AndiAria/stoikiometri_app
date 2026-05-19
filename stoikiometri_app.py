import streamlit as st
from chempy import balance_stoichiometry
from collections import OrderedDict

st.title("🧪 Kalkulator Stoikiometri")
st.write("Aplikasi untuk menyetarakan persamaan reaksi dan menghitung stoikiometri sederhana")

# 1. Inisialisasi session_state agar data tidak hilang saat rerun
if "disetarakan" not in st.session_state:
    st.session_state.disetarakan = False
    st.session_state.reac = None
    st.session_state.prod = None
    st.session_state.hasil_reaksi = ""

# Input teks reaksi
reaksi = st.text_input("Masukkan persamaan reaksi", placeholder="Contoh: H2 + O2 -> H2O")

# Tombol untuk menyetarakan
if st.button("Setarakan Reaksi"):
    if reaksi.strip() == "":
        st.warning("⚠ Masukkan persamaan reaksi terlebih dahulu")
        st.session_state.disetarakan = False
    else:
        try:
            if "->" not in reaksi:
                raise ValueError("Gunakan tanda '->' untuk memisahkan reaktan dan produk")

            kiri, kanan = reaksi.split("->")
            reaktan = set(i.strip() for i in kiri.split("+") if i.strip())
            produk = set(i.strip() for i in kanan.split("+") if i.strip())

            reac, prod = balance_stoichiometry(reaktan, produk)

            hasil_kiri = " + ".join([f"{v if v != 1 else ''}{k}" for k, v in OrderedDict(reac).items()])
            hasil_kanan = " + ".join([f"{v if v != 1 else ''}{k}" for k, v in OrderedDict(prod).items()])
            
            # Simpan hasil ke session_state
            st.session_state.reac = reac
            st.session_state.prod = prod
            st.session_state.hasil_reaksi = hasil_kiri + " -> " + hasil_kanan
            st.session_state.disetarakan = True

        except Exception as e:
            st.error("❌ Format reaksi salah. Gunakan format seperti: H2 + O2 -> H2O")
            st.text(f"Detail error: {e}")
            st.session_state.disetarakan = False

# 2. Tampilkan bagian stoikiometri di LUAR blok if button atas, gunakan session_state
if st.session_state.disetarakan:
    st.success("✅ Persamaan reaksi berhasil disetarakan!")
    st.code(st.session_state.hasil_reaksi)

    st.subheader("Perhitungan Stoikiometri")
    
    # Ambil data dari session_state
    reac = st.session_state.reac
    prod = st.session_state.prod
    
    semua_zat = list(reac.keys()) + list(prod.keys())
    zat_diketahui = st.selectbox("Pilih zat diketahui", semua_zat)
    zat_ditanya = st.selectbox("Pilih zat yang ditanya", semua_zat)
    massa = st.number_input(f"Masukkan massa {zat_diketahui} (gram)", min_value=0.0, step=1.0)

    Mr = {"H2": 2, "O2": 32, "H2O": 18, "Fe": 56, "Fe2O3": 160, "N2": 28, "NH3": 17, "CO2": 44, "CH4": 16}

    if st.button("Hitung Stoikiometri"):
        if zat_diketahui not in Mr or zat_ditanya not in Mr:
            st.warning("⚠ Mr zat belum tersedia di dalam program")
        else:
            mol_diketahui = massa / Mr[zat_diketahui]
            koef_diketahui = reac.get(zat_diketahui, prod.get(zat_diketahui))
            koef_ditanya = reac.get(zat_ditanya, prod.get(zat_ditanya))
            
            mol_ditanya = mol_diketahui * koef_ditanya / koef_diketahui
            massa_ditanya = mol_ditanya * Mr[zat_ditanya]
            st.success(f"✅ Massa {zat_ditanya} = {massa_ditanya:.2f} gram")
