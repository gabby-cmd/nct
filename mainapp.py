import streamlit as st
import pandas as pd

# Sample NCT Data
def get_nct_data():
    return pd.DataFrame({
        "NCT ID": ["NCT05853965", "NCT03992170", "NCT06245629"],
        "Description": [
            "Combination Treatment of Belantamab Mafodotin and Venetoclax in Treatment of Relapsed and Refractory t(11;14) Multiple Myeloma",
            "Study of Daratumumab in Multiple Myeloma (MM) Patients in >VGPR/MRD-positive (DART4MM)",
            "Bortezomib-bendamustine-melphalan vs Melphalan for Multiple Myeloma"
        ],
        "Eligibility Criteria": [
            "Subjects must be ≥18 years old, ECOG ≤2, documented MM with measurable disease. Prior treatments required. Adequate organ function necessary. Pregnancy restrictions apply.",
            "Patients >VGPR/MRD-positive, ≥12 weeks from any therapy, ECOG 0-2, lab values within range, no recent therapy, disease-free for 5 years, effective contraception required, informed consent signed.",
            "Patients with first relapse after ASCT, treated with second ASCT as part of second-line treatment. Conditioning at ASCT2 with bortezomib-bendamustine-melphalan or high-dose melphalan."
        ]
    })

# Streamlit App
st.title("Clinical Trial Matching for Multiple Myeloma")

uploaded_file = st.file_uploader("Upload Patient Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Matching logic
    def match_nct(primary_diagnosis):
        matches = []
        if "C90" in str(primary_diagnosis):
            matches.append("NCT05853965")
            matches.append("NCT03992170")
            matches.append("NCT06245629")
        return ", ".join(matches) if matches else "No Match"
    
    df["Matched NCT IDs"] = df["Primary Diagnosis"].apply(match_nct)
    
    # Display results
    for index, row in df.iterrows():
        st.write(f"### Patient: {row['Patient Name']}")
        st.write(f"Matched NCT IDs: {row['Matched NCT IDs']}")
