import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math



st.title("Study Loan Repayment calculator")

st.write("### Fill up the details")

col1,col2,col3 = st.columns(3)
educationloanvalue= col1.number_input("Loan Value",min_value=0,value=500000)
interestrate= col2.number_input("Interest Rate (in %)", min_value=0.0, value= 8.00) 
loanterm = col3.number_input("Loan Term (in years)", min_value=0, value= 10)


# Calculation 
monthly_interest_rate= (interestrate/100)/12
number_of_payments = loanterm*12
monthly_payment = (educationloanvalue
                   *(monthly_interest_rate*(1+ monthly_interest_rate)**number_of_payments)
                   /((1+monthly_interest_rate)** number_of_payments-1)
                   )

#display repayments

total_payments = monthly_payment*number_of_payments
total_interest = total_payments-educationloanvalue

st.write("### Repayments")

col1,col2,col3 = st.columns(3)
col1.metric(label="Monthly Repayments",value = f"Rs. {monthly_payment:,.2f}")
col2.metric(label="Total Repayments",value = f"Rs. {total_payments:,.0f}")
col3.metric(label="Total Interest",value = f"Rs. {total_interest:,.0f}")


#create a data-frae with thepayment schedule
schedule=[]
remaining_balance= educationloanvalue

for i in range(1,number_of_payments+1):
    int_payment =remaining_balance*monthly_interest_rate
    prin_payment= monthly_payment-int_payment
    remaining_balance -= prin_payment
    year =math.ceil(i/12)
    schedule.append(
        [
            i,
            monthly_payment,
            prin_payment,
            int_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month","Payment","Principal","Interest","Remaining Balance","Year"],
)

st.write("### Payment Schedule")
payment_df = df[["Year","Remaining Balance"]].groupby("Year").min()
st.line_chart(payment_df)


st.write(df)
