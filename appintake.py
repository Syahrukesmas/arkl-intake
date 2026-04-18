import streamlit as st

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Kalkulator ARKL Terpadu", page_icon="🧪", layout="wide")

# CSS untuk memperbaiki tampilan box agar teks terbaca jelas
st.markdown("""
    <style>
    .stMetric { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e6e9ef;
    }
    [data-testid="stMetricLabel"] { color: #555555 !important; }
    [data-testid="stMetricValue"] { color: #1f1f1f !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Kalkulator Intake ARKL")
st.write("Silakan pilih kategori perhitungan di bawah ini:")

# 2. PEMBUATAN TAB
tab1, tab2 = st.tabs(["🟢 Non-Karsinogen", "🔴 Karsinogen"])

# --- FUNGSI GLOBAL UNTUK INPUT (Agar Rapih) ---
def get_inputs(suffix):
    col1, col2, col3 = st.columns(3)
    with col1:
        c = st.number_input("Konsentrasi (C) - mg/m3 atau mg/L", format="%.4f", value=0.0100, key=f"c_{suffix}")
        r = st.number_input("Laju Asupan (R)", value=0.83, key=f"r_{suffix}")
    with col2:
        te = st.number_input("Waktu Paparan (tE) - jam/hari", value=24, key=f"te_{suffix}")
        fe = st.number_input("Frekuensi (fE) - hari/tahun", value=350, key=f"fe_{suffix}")
    with col3:
        dt = st.number_input("Durasi (Dt) - tahun", value=30, key=f"dt_{suffix}")
        wb = st.number_input("Berat Badan (Wb) - kg", value=70.0, key=f"wb_{suffix}")
    return c, r, te, fe, dt, wb

# ==========================================
# TAB 1: NON-KARSINOGEN
# ==========================================
with tab1:
    st.subheader("Perhitungan Intake Non-Karsinogen")
    c, r, te, fe, dt, wb = get_inputs("non")
    
    # Rumus: avgT = Dt * 365
    avg_t_non = dt * 365
    intake_non = (c * r * te * fe * dt) / (wb * avg_t_non) if (wb * avg_t_non) != 0 else 0
    
    st.divider()
    st.metric(label="Hasil Intake Non-Karsinogen", value=f"{intake_non:.5f} mg/kg-hari")
    st.caption("Gunakan nilai ini untuk dibandingkan dengan RfD (Intake / RfD = HQ).")

# ==========================================
# TAB 2: KARSINOGEN
# ==========================================
with tab2:
    st.subheader("Perhitungan Intake Karsinogen")
    c, r, te, fe, dt, wb = get_inputs("kar")
    
    # Rumus: avgT = LifeTime (70 tahun * 365 hari = 25.550)
    life_time = 25550
    intake_kar = (c * r * te * fe * dt) / (wb * life_time) if (wb * life_time) != 0 else 0
    
    st.divider()
    st.metric(label="Hasil Intake Karsinogen", value=f"{intake_kar:.7f} mg/kg-hari")
    st.caption("Gunakan nilai ini untuk dikalikan dengan Slope Factor (Intake * SF = ECR).")
# ==========================================
# TAB 3: NILAI RFD/RFC
# ==========================================
with tab3:
# 3. INPUT NILAI AMBANG BATAS (RfD / RfC)
st.subheader("🔍 Karakteristik Risiko")
choice = st.radio("Pilih Referensi Ambang Batas:", ["RfD (Oral/Dermal)", "RfC (Inhalasi)"], horizontal=True)

res_col1, res_col2 = st.columns(2)
with res_col1:
    if choice == "RfD (Oral/Dermal)":
        ref_val = st.number_input("Masukkan Nilai RfD (mg/kg-hari)", format="%.5f", value=0.02000)
    else:
        ref_val = st.number_input("Masukkan Nilai RfC (mg/m3)", format="%.5f", value=0.02000)

# 4. LOGIKA PERHITUNGAN
# Intake (Ink)
avg_t = dt_val * 365
ink = (c_val * r_val * te_val * fe_val * dt_val) / (wb_val * avg_t) if (wb_val * avg_t) != 0 else 0

# Hazard Quotient (HQ)
# Jika RfC digunakan, beberapa literatur membandingkan C langsung dengan RfC.
# Namun secara ARKL Kemenkes, Ink dibandingkan dengan RfD.
hq = ink / ref_val if ref_val != 0 else 0

# 5. TAMPILAN HASIL
with res_col2:
    st.metric(label="Hasil Intake (Ink)", value=f"{ink:.5f} mg/kg-hari")
    if hq > 1:
        st.metric(label="Hazard Quotient (HQ)", value=f"{hq:.4f}", delta="TIDAK AMAN", delta_color="inverse")
        st.error("⚠️ Kesimpulan: Risiko Non-Karsinogenik bersifat Signifikan (HQ > 1).")
    else:
        st.metric(label="Hazard Quotient (HQ)", value=f"{hq:.4f}", delta="AMAN")
        st.success("✅ Kesimpulan: Risiko Non-Karsinogenik tidak signifikan (HQ <= 1).")

# --- FOOTER ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666666; font-size: 0.9em;">
        ⚠️ <i>Aplikasi ini dalam Tahap Pengembangan.</i><br>
        Hubungi Email: <a href="mailto:muhamaddoni689@gmail.com">muhamaddoni689@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)
