import streamlit as st
import pandas as pd

# Sample NCT Data
def get_nct_data():
    return pd.DataFrame({
        "NCT ID": [
            "NCT05853965", "NCT03992170", "NCT06245629",
            "NCT02159820", "NCT05642871", "NCT06556342"
        ],
        "Description": [
            "Combination Treatment of Belantamab Mafodotin and Venetoclax in Treatment of Relapsed and Refractory t(11;14) Multiple Myeloma",
            "Study of Daratumumab in Multiple Myeloma (MM) Patients in >VGPR/MRD-positive (DART4MM)",
            "Bortezomib-bendamustine-melphalan vs Melphalan for Multiple Myeloma",
            "Lower Dose Decitabine (DAC)-Primed TC (Carboplatin-Paclitaxel) Regimen in Ovary Cancer",
            "DKI Combined With APT for Post-treatment Assessment of Ovarian Malignancies and Correlation With XRCC2 Gene",
            "The Efficacy and Safety of FRD001 in Ultrasound Contrast Imaging for Malignant Ovarian Masses in Women"
        ],
        "Eligibility Criteria": [
            "Subjects must be ≥18 years old, ECOG ≤2, documented MM with measurable disease. Prior treatments required. Adequate organ function necessary. Pregnancy restrictions apply.",
            "Patients >VGPR/MRD-positive, ≥12 weeks from any therapy, ECOG 0-2, lab values within range, no recent therapy, disease-free for 5 years, effective contraception required, informed consent signed.",
            "Diagnosis of first relapse after previous ASCT for multiple myeloma. Treated with a second ASCT as part of second-line treatment. Conditioning with bortezomib-bendamustine-melphalan or high-dose melphalan only.",
            "FIGO stages II to IV fallopian tube cancer or primary peritoneal cancer, no prior chemotherapy, ECOG 0-3, adequate organ function, age ≥18.",
            "No previous ovarian tumours or surgeries, no concurrent cancers, confirmed diagnosis, receiving platinum-based chemotherapy for ≥3 cycles, no MRI contraindications.",
            "Female, age 18-75, untreated ovarian masses, expected survival ≥3 months, ECOG 0-2, adequate organ function, effective contraception, informed consent signed."
        ]
    })

# Streamlit App
st.title("Clinical Trial Matching for Multiple Myeloma and Ovarian Cancer")

uploaded_file = st.file_uploader("Upload Patient Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    search_patient = st.text_input("Search Patient by Name:")
    
    # Matching logic
    def match_nct(primary_diagnosis):
        matches = []
        if "C90" in str(primary_diagnosis):
            matches.extend(["NCT05853965", "NCT03992170", "NCT06245629"])
        if "C56" in str(primary_diagnosis):
            matches.extend(["NCT02159820", "NCT05642871", "NCT06556342"])
        return matches if matches else ["No Match"]
    
    df["Matched NCT IDs"] = df["Primary Diagnosis"].apply(match_nct)
    
    # Display results
    if search_patient:
        patient_data = df[df["Patient Name"].str.lower() == search_patient.lower()]
        if not patient_data.empty:
            for _, row in patient_data.iterrows():
                st.write(f"### Patient: {row['Patient Name']} ({row['Gender']})")
                st.write(f"Primary Diagnosis: {row['Primary Diagnosis']}")
                st.write(f"Secondary Diagnosis: {row['Secondary Diagnosis']}")
                matched_nct_ids = row['Matched NCT IDs']
                nct_data = get_nct_data()
                for nct_id in matched_nct_ids:
                    nct_info = nct_data[nct_data["NCT ID"] == nct_id]
                    if not nct_info.empty:
                        st.write(f"**NCT ID:** {nct_id}")
                        st.write(f"**Description:** {nct_info['Description'].values[0]}")
        else:
            st.write("Patient not found.")
