import streamlit as st

st.set_page_config(page_title="ARKL Intake Calculator", layout="centered")

st.title("📊 Perhitungan Intake ARKL (dengan tE)")
st.markdown("Non-Karsinogen & Karsinogen")

# ======================
# INPUT
# ======================
st.sidebar.header("Parameter Input")

C = st.sidebar.number_input("Konsentrasi (C) mg/L", value=1.0)

IR = st.sidebar.number_input("Intake Rate (L/jam)", value=0.083)  
# default 2 L/hari ≈ 0.083 L/jam

tE = st.sidebar.number_input("Waktu Pajanan (jam/hari)", value=24.0)

EF = st.sidebar.number_input("Frekuensi Pajanan (hari/tahun)", value=350)
ED = st.sidebar.number_input("Durasi Pajanan (tahun)", value=30)

BW = st.sidebar.number_input("Berat Badan (kg)", value=60.0)

RfD = st.sidebar.number_input("RfD (mg/kg/hari)", value=0.001)
CSF = st.sidebar.number_input("Cancer Slope Factor", value=0.0)

lifetime = st.sidebar.number_input("Lifetime (tahun)", value=70)

# ======================
# AVERAGING TIME
# ======================
AT_non = ED * 365
AT_cancer = lifetime * 365

# ======================
# INTAKE
# ======================
# Intake sekarang mempertimbangkan tE
intake_non = (C * IR * tE * EF * ED) / (BW * AT_non)
intake_cancer = (C * IR * tE * EF * ED) / (BW * AT_cancer)

# ======================
# RISK
# ======================
HQ = intake_non / RfD if RfD != 0 else 0
cancer_risk = intake_cancer * CSF

# ======================
# OUTPUT
# ======================
st.header("📈 Hasil")

st.subheader("Non-Karsinogen")
st.write(f"Intake: {intake_non:.6f} mg/kg/hari")
st.write(f"HQ: {HQ:.3f}")

if HQ < 1:
    st.success("Aman")
else:
    st.error("Berisiko")

st.markdown("---")

st.subheader("Karsinogen")
st.write(f"Intake: {intake_cancer:.6f} mg/kg/hari")
st.write(f"Cancer Risk: {cancer_risk:.6e}")

if cancer_risk < 1e-6:
    st.success("Risiko sangat kecil")
elif 1e-6 <= cancer_risk <= 1e-4:
    st.warning("Perlu perhatian")
else:
    st.error("Risiko tinggi")

# ======================
# CATATAN
# ======================
st.markdown("---")
st.warning("""
Perhatian:
- IR harus dalam satuan L/jam jika menggunakan tE
- Jangan gunakan IR (L/hari) + tE sekaligus → akan double count
- AT non-karsinogen = ED × 365
- AT karsinogen = lifetime × 365
""")
