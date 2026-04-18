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

st.title("🧪 Kalkulator Intake ARKL Terintegrasi")

# 2. PEMBUATAN TAB
tab1, tab2 = st.tabs(["🟢 Non-Karsinogen", "🔴 Karsinogen"])

# --- FUNGSI GLOBAL UNTUK INPUT ---
def get_inputs(suffix):
    col1, col2, col3 = st.columns(3)
    with col1:
        c = st.number_input("Konsentrasi (C)", format="%.4f", value=0.0100, key=f"c_{suffix}")
        r = st.number_input("Laju Asupan (R)", value=0.83, key=f"r_{suffix}")
    with col2:
        te = st.number_input("Waktu Paparan (tE)", value=24, key=f"te_{suffix}")
        fe = st.number_input("Frekuensi (fE)", value=350, key=f"fe_{suffix}")
    with col3:
        dt = st.number_input("Durasi (Dt)", value=30, key=f"dt_{suffix}")
        wb = st.number_input("Berat Badan (Wb)", value=70.0, key=f"wb_{suffix}")
    return c, r, te, fe, dt, wb

# ==========================================
# TAB 1: NON-KARSINOGEN
# ==========================================
with tab1:
    st.subheader("Perhitungan Non-Karsinogen")
    c_n, r_n, te_n, fe_n, dt_n, wb_n = get_inputs("non")
    rfd = st.number_input("Reference Dose (RfD)", format="%.5f", value=0.02000, key="rfd_val")
    
    avg_t_non = dt_n * 365
    intake_non = (c_n * r_n * te_n * fe_n * dt_n) / (wb_n * avg_t_non) if (wb_n * avg_t_non) != 0 else 0
    hq = intake_non / rfd if rfd != 0 else 0
    
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("t_avg", f"{avg_t_non} hari")
    c2.metric("Intake", f"{intake_non:.5f}")
    c3.metric("HQ", f"{hq:.4f}", delta="AMAN" if hq <= 1 else "TIDAK AMAN", delta_color="normal" if hq <= 1 else "inverse")

# ==========================================
# TAB 2: KARSINOGEN
# ==========================================
with tab2:
    st.subheader("Perhitungan Karsinogen")
    c_k, r_k, te_k, fe_k, dt_k, wb_k = get_inputs("kar")
    sf = st.number_input("Slope Factor (SF)", format="%.5f", value=0.00100, key="sf_val")
    
    avg_t_kar = 25550
    intake_kar = (c_k * r_k * te_k * fe_k * dt_k) / (wb_k * avg_t_kar) if (wb_k * avg_t_kar) != 0 else 0
    ecr = intake_kar * sf # DI SINI PERBAIKANNYA (Baris 79)
    
    st.divider()
    k1, k2, k3 = st.columns(3)
    k1.metric("t_avg", f"{avg_t_kar} hari")
    k2.metric("Intake", f"{intake_kar:.7f}")
    k3.metric("ECR", f"{ecr:.7f}", delta="AMAN" if ecr <= 0.0001 else "TIDAK AMAN", delta_color="normal" if ecr <= 0.0001 else "inverse")

# --- FOOTER ---
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666666; font-size: 0.9em;">
        ⚠️ <i>Dalam Tahap Pengembangan. Hubungi Email: muhamaddoni689@gmail.com</i>
    </div>
    """, unsafe_allow_html=True)
