import streamlit as st
from chempy import balance_stoichiometry
from collections import OrderedDict

st.title("🧪 Kalkulator Stoikiometri")
st.write("Aplikasi untuk menyetarakan persamaan reaksi dan menghitung stoikiometri sederhana")

reaksi = st.text_input("Masukkan persamaan reaksi", placeholder="Contoh: H2 + O2 -> H2O")

if st.button("Setarakan Reaksi"):
    if reaksi.strip() == "":
        st.warning("⚠ Masukkan persamaan reaksi terlebih dahulu")
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
            hasil_reaksi = hasil_kiri + " -> " + hasil_kanan

            st.success("✅ Persamaan reaksi berhasil disetarakan!")
            st.code(hasil_reaksi)

            st.subheader("Perhitungan Stoikiometri")
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
        except Exception as e:
            st.error("❌ Format reaksi salah. Gunakan format seperti: H2 + O2 -> H2O")
            st.text(f"Detail error: {e}")
