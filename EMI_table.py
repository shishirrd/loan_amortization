#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import streamlit as st
import base64
import webbrowser

# In[2]:
pd.set_option("display.max_columns", None)

# In[3]:
st.sidebar.image('st_logo.png')
st.sidebar.write("👋 Hi, I’m Shishir! I've recently developed a love for coding.")
st.sidebar.write("🌱 I’m currently learning Python to augment my job as a senior financial analyst.")
st.sidebar.write("📫 Reach me @ shishir.rd@gmail.com")
st.sidebar.write("My Github is https://github.com/shishirrd")

st.header("Loan Amortization Table Generator")
st.write('Tired of online calculators that gave me only the monthly payment amount, I decided to build something more useful for the data-curious.')
st.write('Go ahead and select the interest rate, loan term and the loan amount. An amortization table gets generated on screen and can also be downloaded to an Excel CSV file!')

with st.expander("Click on this box to input your loan parameters"):
    interest_rate = st.number_input("Your loan's interest rate", min_value=1.00, max_value=20.00, step=0.50)
    loan_term = st.number_input("Term of your loan in years", min_value=1, max_value=99, step=1)
    loan_amount = st.number_input("Your loan amount", 
                        min_value=100000, max_value=100000000, step=500000)

int_input = interest_rate
int_rate = int_input/100
monthly_rate = int_rate/12
term = loan_term
principal = loan_amount

# In[4]:
months = term*12

# In[5]:
monthly_interest = principal*monthly_rate
# In[6]:
emi_multiplier = (1+monthly_rate)**months
# In[7]:
EMI = (principal*monthly_rate)*emi_multiplier/(emi_multiplier-1)
# In[8]:
balance = principal+monthly_interest-EMI
# In[9]:
table = pd.DataFrame(columns=['Month','Monthly Payment', 'Monthly Interest','Principal repaid','Loan Balance'])
columns = list(table)
data = []

# In[10]:
for i in range(months):
    monthly_interest = principal*monthly_rate
    principal_payment = EMI-monthly_interest
    principal -= principal_payment
    month = i+1
    item = [month, round(EMI), round(monthly_interest), round(principal_payment), round(principal)]
    zipped = zip(columns, item)
    a_dictionary = dict(zipped)
    table = table.append(a_dictionary, ignore_index=True)

# In[11]:

#table = table.append(data, True)
total_payment = table['Monthly Payment'].sum()
total_interest = table['Monthly Interest'].sum()

st.write(f"Your monthly payment is {round(EMI):,} & total payment across the loan's term is {round(total_payment):,}")
st.write(f"The payout percentage (i.e. principal/total payment) for your loan is ~{round(total_payment*100/loan_amount)}%")
table

def download_link(object_to_download, download_filename, download_link_text):
        
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

if st.button('Download Dataframe to Excel'):
        tmp_download_link = download_link(table, 'EMI_Amort_table' + '.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)
