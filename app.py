import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# File to save data

file_path = "expenses.csv"

# App Title

st.set_page_config(page_title=" Expense Tracker", page_icon="💰", layout="centered")
st.title("Expense Tracker")
st.write("Track your daily expenses easily!")

# Load Data or Initialize
if "data" not in st.session_state:
    if os.path.exists(file_path):
        st.session_state.data = pd.read_csv(file_path)
        # Ensure Amount column is numeric
        st.session_state.data["Amount"] = pd.to_numeric(st.session_state.data["Amount"])
    else:
        st.session_state.data = pd.DataFrame(columns=["Item", "Amount", "Category"])

# Input Section
st.header("Add a New Expense")
item = st.text_input("Expense Name")
amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
category = st.selectbox(
    "Category",
    ["Food", "Transport", "Shopping", "Bills", "Other"]
)

# Add Expense Button

if st.button("Add Expense"):
    if item.strip() == "":
        st.warning("Please enter an expense name.")
    else:
        new_entry = {"Item": item, "Amount": float(amount), "Category": category}
        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_entry])],
            ignore_index=True
        )
        # Ensure Amount stays numeric
        st.session_state.data["Amount"] = pd.to_numeric(st.session_state.data["Amount"])
        # Save to CSV
        st.session_state.data.to_csv(file_path, index=False)
        st.success(f"Added {item} - ${amount:.2f} ({category})")

# Display Expenses
st.header("Your Expenses")
if st.session_state.data.empty:
    st.info("No expenses added yet.")
else:
    # Show table
    st.write(st.session_state.data)

    # Total Expenses

    total = st.session_state.data["Amount"].sum()
    st.subheader(f"Total Expense: ${total:.2f}")

    # Bar Chart by Item

    st.subheader("Expense by Item")
    st.bar_chart(st.session_state.data.set_index("Item")["Amount"])

    # Pie Chart by Category

    st.subheader("Expense Distribution by Category")
    category_data = st.session_state.data.groupby("Category")["Amount"].sum()

    if not category_data.empty:
        fig, ax = plt.subplots()
        ax.pie(category_data, labels=category_data.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures pie is circular
        st.pyplot(fig)
    else:
        st.info("No expenses to plot yet.")


# Optional: Clear All Data

st.sidebar.header("Options")
if st.sidebar.button("Clear All Expenses"):
    st.session_state.data = pd.DataFrame(columns=["Item", "Amount", "Category"])
    if os.path.exists(file_path):
        os.remove(file_path)
    st.success("All expenses cleared!")