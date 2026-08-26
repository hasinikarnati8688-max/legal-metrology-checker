import streamlit as st
import requests
st.title("Legal Metrology Label Scanner")
uploaded_file = st.file_uploader("Upload a product label image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    if st.button("Analyze Label"):
        with st.spinner("Processing image and checking compliance..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            try:
                response = requests.post("http://127.0.0.1:8000/scan", files=files)               
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")                    
                    st.subheader("📋 Analysis Results")
                    st.write(data.get("analysis"))                   
                    with st.expander("Show Extracted Raw Text"):
                        st.text(data.get("extracted_text"))
                else:
                    st.error(f"Error from server: {response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to FastAPI server: {e}")
