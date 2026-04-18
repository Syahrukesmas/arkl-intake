import streamlit as st

st.set_page_config(page_title="ARKL Intake Calculator", layout="centered")

st.title("📊 Perhitungan Asupan (Intake) ARKL")
st.markdown("Fokus: Non-Karsinogen (HQ) & Karsinogen (Cancer Risk)")

# ======================
# INPUT DASAR
# ======================
st.sidebar.header("Input Parameter")

C = st.sidebar.number_input("Konsentrasi (C) mg/L", value=1.0)
IR = st.sidebar.number_input("Intake Rate (L/hari)", value=2.0)
EF = st.sidebar.number_input("Frekuensi Pajanan (hari/tahun)", value=350)
ED = st.sidebar.number_input("Durasi Pajanan (tahun)", value=30)
BW = st.sidebar.number_input("Berat Badan (kg)", value=60.0)

RfD = st.sidebar.number_input("RfD (mg/kg/hari)", value=0.001)
CSF = st.sidebar.number_input("Cancer Slope Factor (CSF)", value=0.0)

lifetime = st.sidebar.number_input("Lifetime (tahun, untuk karsinogen)", value=70)

# ======================
# AVERAGING TIME
# ======================
AT_non = ED * 365
AT_cancer = lifetime * 365

# ======================
# PERHITUNGAN INTAKE
# ======================
intake_non = (C * IR * EF * ED) / (BW * AT_non)
intake_cancer = (C * IR * EF * ED) / (BW * AT_cancer)

# ======================
# RISK
# ======================
HQ = intake_non / RfD if RfD != 0 else 0
cancer_risk = intake_cancer * CSF

# ======================
# OUTPUT
# ======================
st.header("📈 Hasil Perhitungan")

st.subheader("Non-Karsinogen")
st.write(f"Intake: {intake_non:.6f} mg/kg/hari")
st.write(f"Hazard Quotient (HQ): {HQ:.3f}")

if HQ < 1:
    st.success("Aman (HQ < 1)")
else:
    st.error("Berisiko (HQ > 1)")

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
st.info("""
Catatan penting:
- Non-karsinogen pakai AT = ED × 365
- Karsinogen pakai AT = lifetime × 365
- Gunakan nilai RfD & CSF dari sumber resmi (EPA / WHO)
""")
