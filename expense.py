import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def load_expenses():
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file)

def save_expenses():
    st.session_state.expenses.to_csv('expenses.csv', index=False)
    st.success("Expenses saved successfully!")

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(data=st.session_state.expenses, x='Category', y='Amount', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No expenses to visualize!")

st.markdown('<div class="stTitle">My Expense Tracker !!!</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="stHeader">Add Expense</div>', unsafe_allow_html=True)
    date = st.date_input('Date')
    category = st.selectbox('Category', ['Food', 'Transport', 'Entertainment', 'Utilities', 'Groceries', 'Shopping', 'Other'])
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    description = st.text_input('Description')
    if st.button('Add'):
        add_expense(date, category, amount, description)
        st.success('Expense added!')

    st.markdown('<div class="stHeader">File Operations</div>', unsafe_allow_html=True)
    if st.button('Save Expenses'):
        save_expenses()
    if st.button('Load Expenses'):
        load_expenses()

st.markdown('<div class="stHeader">Expenses</div>', unsafe_allow_html=True)
st.dataframe(st.session_state.expenses, width=800, height=400)

st.markdown('<div class="stHeader">Visualization</div>', unsafe_allow_html=True)
if st.button('Visualize Expenses'):
    visualize_expenses()
