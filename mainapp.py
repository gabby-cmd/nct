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
        
        # Matching logic
        def match_nct(icd_code):
            matched_trials = nct_data[nct_data["Eligibility Criteria"].str.contains(icd_code, case=False, na=False)]["NCT ID"].tolist()
            return matched_trials if matched_trials else ["No Match"]
        
        df["Matched NCT IDs"] = df["icdcode"].apply(match_nct)
        
        # Display results
        if search_patient:
            patient_data = df[df["patientname"].str.lower() == search_patient.lower()]
            if not patient_data.empty:
                for _, row in patient_data.iterrows():
                    st.write(f"### Patient: {row['patientname']} ({row['gender']})")
                    st.write(f"Primary Diagnosis: {row['primarydiag']}")
                    st.write(f"Secondary Diagnosis: {row['secondarydiag']}")
                    matched_nct_ids = row['Matched NCT IDs']
                    
                    matched_nct_info = nct_data[nct_data["NCT ID"].isin(matched_nct_ids)]
                    if not matched_nct_info.empty:
                        st.write("### Matched Clinical Trials")
                        st.dataframe(matched_nct_info)
            else:
                st.write("Patient not found.")
