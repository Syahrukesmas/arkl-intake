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

# --- FOOTER ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666666; font-size: 0.9em;">
        ⚠️ <i>Aplikasi ini dalam Tahap Pengembangan.</i><br>
        Hubungi Email: <a href="mailto:muhamaddoni689@gmail.com">muhamaddoni689@gmail.com</a>
    </div>
    """, unsafe_allow_html=True)
