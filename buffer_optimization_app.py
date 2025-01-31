import streamlit as st
import pandas as pd

# Streamlit app title and description
st.title("Heavy Metal Sensing: Buffer Optimization")
st.write("Upload your experimental data and optimize buffer conditions for heavy metal electrochemical detection.")

# Upload file section
uploaded_file = st.file_uploader("Upload a CSV or Excel file with experimental results", type=["csv", "xlsx"])

# Display sample data if uploaded
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(data.head())
    except Exception as e:
        st.error("Error loading file. Please check the format.")
        st.write(e)

# Analysis settings section
st.header("Buffer Optimization Settings")

# Select heavy metal target
metal_target = st.selectbox("Select Heavy Metal Ion", ["Lead (Pb²⁺)", "Cadmium (Cd²⁺)", "Mercury (Hg²⁺)", "Arsenic (As³⁺)"])

# pH input
ph_value = st.number_input("Select pH", min_value=2.0, max_value=9.0, value=4.5, step=0.1)

# Select buffer system
st.subheader("Buffer System")
buffer_type = st.selectbox("Buffer Type", ["Acetate", "Phosphate", "Britton-Robinson", "Ammonium Acetate"])

# Select buffer concentration
buffer_concentration = st.slider("Buffer Concentration (mM)", min_value=10, max_value=200, value=50, step=10)

# Ionic Strength Adjustment
st.subheader("Ionic Strength Adjustment")
supporting_electrolyte = st.selectbox("Select Supporting Electrolyte", ["KCl", "NaNO₃", "None"])
electrolyte_concentration = st.slider("Electrolyte Concentration (mM)", min_value=0, max_value=100, value=20, step=5)

# Initialize session state for buffer optimization results
if "buffer_optimization" not in st.session_state:
    st.session_state.buffer_optimization = []

# Add buffer conditions to session state
with st.form("buffer_form"):
    add_buffer = st.form_submit_button("Add Buffer Optimization Condition")
    
    if add_buffer:
        st.session_state.buffer_optimization.append({
            "Metal Ion": metal_target,
            "pH": ph_value,
            "Buffer Type": buffer_type,
            "Buffer Concentration (mM)": buffer_concentration,
            "Supporting Electrolyte": supporting_electrolyte,
            "Electrolyte Concentration (mM)": electrolyte_concentration
        })
        st.success("Buffer condition added successfully!")

# Display buffer optimization results
st.write("Optimized Buffer Conditions:")
buffer_df = pd.DataFrame(st.session_state.buffer_optimization)
st.dataframe(buffer_df)

# Download results
if not buffer_df.empty:
    csv = buffer_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Optimized Buffer Data", data=csv, file_name="buffer_optimization.csv", mime="text/csv")

# Submit button for final query
if st.button("Submit Optimization Query"):
    st.success("Optimization query submitted with the following settings:")
    st.write("Selected Metal Ion:", metal_target)
    st.write("pH:", ph_value)
    st.write("Buffer Type:", buffer_type)
    st.write("Buffer Concentration:", buffer_concentration, "mM")
    st.write("Supporting Electrolyte:", supporting_electrolyte)
    st.write("Electrolyte Concentration:", electrolyte_concentration, "mM")
