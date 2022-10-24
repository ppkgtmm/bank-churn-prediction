import requests
import streamlit as st

color_map = {
    'churn': '#ef4444',
    'not churn': '#86efac'
}

st.markdown('''
    <style>
        div.stButton > button:first-child { 
            width: inherit; 
        }
        #credit-card-customer-churn-prediction {
            text-align: center;
        }
        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 0rem;
        }
        .stMarkdown {
            text-align: center;
        }
    </style>
''', unsafe_allow_html=True)
st.write('#### Credit Card Customer Churn Prediction')
col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox(
        'Gender',
        ('M', 'F')
    )
    dependent_count = st.number_input('Dependent Count', min_value=0)
    months_inactive_12_mon = st.number_input('Inactive Months', min_value=0, max_value=12)
    total_revolving_bal = st.number_input('Total Revolving Balance', min_value=0.0)
    total_trans_amt = st.number_input('Total Transaction Amount', min_value=0.0)

with col2:
    education = st.selectbox(
        'Education',
        ('High School','College', 'Graduate', 'Post-Graduate','Doctorate', 'Uneducated', 'Unknown')
    )
    months_on_book = st.number_input('Months on Book', min_value=0)
    contacts_count_12_mon = st.number_input('Contact Count', min_value=0)
    total_amt_chng_q4_q1 = st.number_input('Change Amount Q4/Q1', min_value=0.0)
    total_trans_ct = st.number_input('Total Transaction Count', min_value=0)

with col3:
    age = st.number_input('Age', min_value=0)
    total_relationship_count = st.number_input('Relationship Count', min_value=0)
    credit_limit = st.number_input('Credit Limit', min_value=0.0)
    total_ct_chng_q4_q1 = st.number_input('Change Count Q4/Q1', min_value=0.0)
    avg_utilization_ratio = st.number_input('Average Utilization Ratio', min_value=0.0, max_value=1.0, step=0.01)

st.write('')
col4, col5, col6 = st.columns(3)
with col5:
    button = st.button('Predict')
    if button:
        # result = 'churn'.lower()
        response = requests.post(
            'http://localhost:8000/predict', 
            json=[dict(
                gender=gender,
                education_level=education,
                customer_age=age,
                dependent_count=dependent_count,
                months_on_book=months_on_book,
                total_relationship_count=total_relationship_count,
                months_inactive_12_mon=months_inactive_12_mon,
                contacts_count_12_mon=contacts_count_12_mon,
                credit_limit=credit_limit,
                total_revolving_bal=total_revolving_bal,
                total_amt_chng_q4_q1=total_amt_chng_q4_q1,
                total_trans_amt=total_trans_amt,
                total_trans_ct=total_trans_ct,
                total_ct_chng_q4_q1=total_ct_chng_q4_q1,
                avg_utilization_ratio=avg_utilization_ratio,
            )],
            headers={'Content-Type': 'application/json'}
        ).json()
        result = str(response[0]['prediction']).lower()
        st.markdown('''
            <style>
                .stMarkdown {
                    text-align: center;
                    color: ''' + color_map[result] + ''';
                }
                p {
                    font-size: 22px;
                    margin-botton: 0px;
                    font-weight: bold;
                }
            </style>
        ''', unsafe_allow_html=True)
        st.write(result.upper())