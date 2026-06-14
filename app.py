import streamlit as st
import pandas as pd

if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go To",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

if page == "Home":
    st.title("Personal Expense Tracker")
    st.write("Track your income and expenses easily.")

elif page == "Add Transaction":
    st.title("Add Transaction")

    t_type = st.selectbox("Type", ["Income", "Expense"])

    if t_type == "Income":
        category = st.text_input("Income Source")
    else:
        category = st.selectbox(
            "Expense Category",
            ["Food", "Travel", "Shopping", "Bills",
             "Education", "Medical", "Others"]
        )

    amount = st.number_input("Amount", min_value=0.0)
    date = st.date_input("Date")
    description = st.text_area("Description")

    if st.button("Add"):
        st.session_state.transactions.append({
            "type": t_type,
            "category": category,
            "amount": amount,
            "date": str(date),
            "description": description
        })
        st.success("Transaction Added Successfully")

elif page == "View Transactions":
    st.title("Transaction History")

    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(df)
    else:
        st.warning("No transactions available")

elif page == "Summary":
    st.title("Summary")

    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)

        total_income = df[df["type"] == "Income"]["amount"].sum()
        total_expense = df[df["type"] == "Expense"]["amount"].sum()

        balance = total_income - total_expense

        st.write("### Total Income:", total_income)
        st.write("### Total Expenses:", total_expense)
        st.write("### Balance:", balance)

        st.write("### Category Wise Expenses")

        expense_df = df[df["type"] == "Expense"]

        if not expense_df.empty:
            summary = expense_df.groupby("category")["amount"].sum()
            st.bar_chart(summary)
    else:
        st.warning("No data available")