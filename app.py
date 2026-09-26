import streamlit as st
import pandas as pd
import io

from scraper import process_dataframe

st.set_page_config(
    page_title="Social Media Extractor",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

.block-container{
    max-width:1100px;
    padding-top:2rem;
}

.hero{
    text-align:center;
    padding:40px;
    border-radius:20px;
    background:linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    color:white;
    margin-bottom:30px;
}

.hero h1{
    font-size:50px;
    font-weight:700;
}

.hero p{
    font-size:18px;
}

.stButton > button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-size:18px;
    font-weight:600;
}

[data-testid="stFileUploader"]{
    border:2px dashed #3b82f6;
    border-radius:15px;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🚀 Social Media Extractor</h1>
<p>
Upload an Excel file and extract
LinkedIn, Facebook, Instagram and Amazon links.
</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("Preview")

    st.dataframe(df.head())

    if st.button("Start Extraction"):

        with st.spinner("Processing websites..."):

            result_df = process_dataframe(df)

        linkedin_count = (
            result_df["LinkedIn"]
            .astype(str)
            .ne("")
            .sum()
        )

        facebook_count = (
            result_df["Facebook"]
            .astype(str)
            .ne("")
            .sum()
        )

        instagram_count = (
            result_df["Instagram"]
            .astype(str)
            .ne("")
            .sum()
        )

        amazon_count = (
            result_df["Amazon Found"]
            .astype(str)
            .eq("Yes")
            .sum()
        )

        st.success("Extraction Complete")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric(
            "LinkedIn",
            linkedin_count
        )

        c2.metric(
            "Facebook",
            facebook_count
        )

        c3.metric(
            "Instagram",
            instagram_count
        )

        c4.metric(
            "Amazon",
            amazon_count
        )

        output = io.BytesIO()

        result_df.to_excel(
            output,
            index=False,
            engine="openpyxl"
        )

        output.seek(0)

        st.download_button(
            label="📥 Download Excel",
            data=output,
            file_name="social_media_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )