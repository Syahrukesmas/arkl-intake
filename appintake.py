import streamlit as st

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Kalkulator ARKL Standar Kemenkes", page_icon="⚖️", layout="wide")

# CSS untuk tampilan profesional dan kontras tinggi
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
    [data-testid="stMetricValue"] { color: #1f1f1f !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Kalkulator Asupan (Intake) ARKL")
st.write("Aplikasi perhitungan risiko kesehatan berdasarkan standar formula pajanan.")

# 2. PEMBUATAN TAB
tab1, tab2 = st.tabs(["🟢 Non-Karsinogen (HQ)", "🔴 Karsinogen (ECR)"])

# --- FUNGSI INPUT SESUAI RUMUS GAMBAR ---
def get_arkl_inputs(suffix):
    col1, col2, col3 = st.columns(3)
    with col1:
        c = st.number_input("Konsentrasi (C) - mg/m3 atau mg/L", format="%.4f", value=0.0100, key=f"c_{suffix}")
        r = st.number_input("Laju Asupan (R)", value=0.83, key=f"r_{suffix}", help="Udara: 0.83 m3/jam, Air: 2 L/hari")
    with col2:
        te = st.number_input("Waktu Pajanan (tE) - jam/hari", value=24, key=f"te_{suffix}")
        fe = st.number_input("Frekuensi Pajanan (fE) - hari/tahun", value=350, key=f"fe_{suffix}")
    with col3:
        dt = st.number_input("Durasi Pajanan (Dt) - tahun", value=30, key=f"dt_{suffix}")
        wb = st.number_input("Berat Badan (Wb) - kg", value=70.0, key=f"wb_{suffix}")
    return c, r, te, fe, dt, wb

# ==========================================
# TAB 1: NON-KARSINOGEN
# ==========================================
with tab1:
    st.header("Analisis Non-Karsinogen")
    c, r, te, fe, dt, wb = get_arkl_inputs("non")
    
    # Input Ambang Batas
    rfd = st.number_input("Reference Dose (RfD/RfC) - mg/kg-hari", format="%.5f", value=0.02000, key="rfd")

    # Rumus: t_avg = Dt * 365
    t_avg_non = dt * 365
    intake_non = (c * r * te * fe * dt) / (wb * t_avg_non) if (wb * t_avg_non) != 0 else 0
    hq = intake_non / rfd if rfd != 0 else 0

    st.divider()
    res1, res2, res3 = st.columns(3)
    res1.metric("t_avg (Waktu Rata-rata)", f"{t_avg_non} hari")
    res2.metric("Intake (I)", f"{intake_non:.5f}")
    
    if hq > 1:
        res3.metric("Hazard Quotient (HQ)", f"{hq:.4f}", delta="TIDAK AMAN", delta_color="inverse")
    else:
        res3.metric("Hazard Quotient (HQ)", f"{hq:.4f}", delta="AMAN")

# ==========================================
# TAB 2: KARSINOGEN
# ==========================================
with tab2:
    st.header("Analisis Karsinogen")
    c, r, te, fe, dt, wb = get_arkl_inputs("kar")
    
    # Input Ambang Batas
    sf = st.number_input("Slope Factor (SF)", format="%.5f", value=0.00100, key="sf")

    # Rumus: t_avg = 70 tahun * 365 hari
    t_avg_kar = 25550
    intake_kar = (c * r * te * fe * dt) / (wb * t_avg_kar) if (wb * t_avg_kar) != 0 else 0
    ecr = intake_
