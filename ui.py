import requests
import streamlit as st
import pandas as pd

color_map = {"Churn": "#ef5c5c", "Not Churn": "#86efac"}


st.markdown(
    """
    <style>
        .stFileUploader {
            max-width: 46rem;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            max-width: 85vw;
            display: flex;
            flex-direction: column;

        }
        .stMarkdown {
            text-align: center;
        }
       .element-container:nth-of-type(2) {
            max-width: 46rem;
            margin-left: auto;
            margin-right: auto
        }
    </style>
""",
    unsafe_allow_html=True,
)


with st.container():
    st.write("#### Credit Card Customer Churn Prediction")
    input_file = st.file_uploader(
        "Upload input data file", type="csv", accept_multiple_files=False
    )
    if input_file:
        st.write(f"Uploaded {input_file.name}")
if input_file:
    used_cols = [
        "clientnum",
        "gender",
        "education_level",
        "customer_age",
        "dependent_count",
        "months_on_book",
        "total_relationship_count",
        "months_inactive_12_mon",
        "contacts_count_12_mon",
        "credit_limit",
        "total_revolving_bal",
        "total_amt_chng_q4_q1",
        "total_trans_amt",
        "total_trans_ct",
        "total_ct_chng_q4_q1",
        "avg_utilization_ratio",
    ]
    df = pd.read_csv(input_file)[used_cols]
    response = requests.post(
        "http://localhost:8000/predict",
        json=df.to_dict(orient="records"),
        headers={"Content-Type": "application/json"},
    )
    df = pd.DataFrame(response.json())
    df = df[["clientnum", "prediction"] + used_cols[1:]]
    with st.container():
        st.dataframe(
            df.style.apply(
                lambda x: x.map(color_map).map(
                    "background-color: {}; color: black;".format
                ),
                axis=1,
                subset="prediction",
            ),
            use_container_width=True,
        )
