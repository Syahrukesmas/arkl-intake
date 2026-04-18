import streamlit as st
import pandas as pd

st.set_page_config(page_title="ARKL Calculator", layout="wide")

st.title("📊 Aplikasi Analisis Risiko Kesehatan Lingkungan (ARKL)")

st.markdown("Hitung Intake, Hazard Quotient (HQ), dan Cancer Risk")

# ======================
# INPUT UMUM
# ======================
st.sidebar.header("Input Umum")

C = st.sidebar.number_input("Konsentrasi (C)", value=1.0)
BW = st.sidebar.number_input("Berat Badan (kg)", value=60.0)
EF = st.sidebar.number_input("Frekuensi Pajanan (hari/tahun)", value=350)
ED = st.sidebar.number_input("Durasi Pajanan (tahun)", value=30)
AT = st.sidebar.number_input("Averaging Time (hari)", value=25550)

RfD = st.sidebar.number_input("RfD (mg/kg/hari)", value=0.001)
CSF = st.sidebar.number_input("Cancer Slope Factor (CSF)", value=0.0)

st.sidebar.markdown("---")

# ======================
# INGESTION
# ======================
st.header("💧 Pajanan Ingestion")

IR_ing = st.number_input("Intake Rate (L/hari)", value=2.0)

intake_ing = (C * IR_ing * EF * ED) / (BW * AT)

# ======================
# INHALATION
# ======================
st.header("🌫️ Pajanan Inhalation")

IR_inh = st.number_input("Inhalation Rate (m3/hari)", value=20.0)

intake_inh = (C * IR_inh * EF * ED) / (BW * AT)

# ======================
# DERMAL
# ======================
st.header("🧴 Pajanan Dermal")

SA = st.number_input("Skin Area (cm2)", value=18000.0)
AF = st.number_input("Adherence Factor", value=0.2)
ABS = st.number_input("Absorption Factor", value=0.1)

intake_dermal = (C * SA * AF * ABS * EF * ED) / (BW * AT * 10000)

# ======================
# TOTAL INTAKE
# ======================
total_intake = intake_ing + intake_inh + intake_dermal

# ======================
# HQ & RISK
# ======================
HQ = total_intake / RfD if RfD != 0 else 0
cancer_risk = total_intake * CSF

# ======================
# OUTPUT
# ======================
st.header("📈 Hasil Perhitungan")

col1, col2, col3 = st.columns(3)

col1.metric("Intake Ingestion", f"{intake_ing:.6f}")
col2.metric("Intake Inhalation", f"{intake_inh:.6f}")
col3.metric("Intake Dermal", f"{intake_dermal:.6f}")

st.markdown("---")

st.metric("Total Intake", f"{total_intake:.6f}")
st.metric("Hazard Quotient (HQ)", f"{HQ:.3f}")
st.metric("Cancer Risk", f"{cancer_risk:.6e}")

# ======================
# INTERPRETASI
# ======================
st.header("🧾 Interpretasi")

if HQ < 1:
    st.success("Non-Karsinogen: Aman (HQ < 1)")
else:
    st.error("Non-Karsinogen: Berisiko (HQ > 1)")

if cancer_risk < 1e-6:
    st.success("Risiko Kanker: Sangat kecil")
elif 1e-6 <= cancer_risk <= 1e-4:
    st.warning("Risiko Kanker: Perlu perhatian")
else:
    st.error("Risiko Kanker: Tinggi")

# ======================
# DATAFRAME OUTPUT
# ======================
data = {
    "Jenis Pajanan": ["Ingestion", "Inhalation", "Dermal"],
    "Intake": [intake_ing, intake_inh, intake_dermal]
}

df = pd.DataFrame(data)

st.subheader("📊 Breakdown Intake")
st.dataframe(df)
