import streamlit as st
import pandas as pd

# Streamlit App
st.title("Clinical Trial Matching for Multiple Myeloma and Ovarian Cancer")

# Upload NCT Details CSV
nct_file = st.file_uploader("Upload NCT Details (CSV)", type=["csv"])
nct_data = None
if nct_file:
    nct_data = pd.read_csv(nct_file)

# Upload Patient Data CSV
uploaded_file = st.file_uploader("Upload Patient Data (CSV)", type=["csv"])

if uploaded_file and nct_data is not None:
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
                
                matched_nct_info = nct_data[nct_data["NCT ID"].isin(matched_nct_ids)]
                if not matched_nct_info.empty:
                    st.write("### Matched Clinical Trials")
                    st.dataframe(matched_nct_info)
        else:
            st.write("Patient not found.")
