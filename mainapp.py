import streamlit as st
import pandas as pd

# Streamlit App
st.title("Clinical Trial Matching for Multiple Myeloma and Ovarian Cancer")

# Upload NCT Details CSV
nct_file = st.file_uploader("Upload NCT Details (CSV)", type=["csv"])
nct_data = None
if nct_file:
    nct_data = pd.read_csv(nct_file)
    required_nct_columns = {"NCT ID", "Study Name", "Eligibility Criteria"}
    if not required_nct_columns.issubset(nct_data.columns):
        st.error("Missing required columns in NCT CSV: 'NCT ID', 'Study Name', 'Eligibility Criteria'")
        nct_data = None

# Upload Patient Data CSV
uploaded_file = st.file_uploader("Upload Patient Data (CSV)", type=["csv"])

if uploaded_file and nct_data is not None:
    df = pd.read_csv(uploaded_file)
    required_patient_columns = {"patientid", "patientname", "primarydiag", "secondarydiag", "gender", "icdcode"}
    if not required_patient_columns.issubset(df.columns):
        st.error("Missing required columns in CSV: patientid, patientname, primarydiag, secondarydiag, gender, icdcode")
    else:
        search_patient = st.text_input("Search Patient by Name:")

        # Directly print the NCT trials when the names match
        if search_patient:
            patient_data = df[df["patientname"].str.lower() == search_patient.lower()]
            if not patient_data.empty:
                for _, row in patient_data.iterrows():
                    st.write(f"### Patient: {row['patientname']} ({row['gender']})")
                    st.write(f"Primary Diagnosis: {row['primarydiag']}")
                    st.write(f"Secondary Diagnosis: {row['secondarydiag']}")
                    
                    st.write("### Matched Clinical Trials:")
                    # Display all NCT trials
                    for _, nct_row in nct_data.iterrows():
                        st.write(f"- **NCT ID**: {nct_row['NCT ID']}, **Study Name**: {nct_row['Study Name']}")
                        st.write(f"  **Eligibility Criteria**: {nct_row['Eligibility Criteria']}")
            else:
                st.write("Patient not found.")
