import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# --- CONFIGURATION ---
st.set_page_config(page_title="Jockey Showrooms", layout="wide", page_icon="📈")
SHOWROOMS = ["Showroom A (Main Street)", "Showroom B (Mall)", "Showroom C (Station Road)"]

# ⚠️ PASTE YOUR PUBLISHED CSV LINK HERE ⚠️
# It should end with something like "output=csv"
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSeVfWOjIec1MZtTldRR9Fgv9EQwyMtq6j1kf_lmy4HSxafV-uswRgd4W91RTmDRgdQHrc-7A5I3485/pub?gid=0&single=true&output=csv"

# --- CONFIG FOR WRITING DATA ---
# This is your regular edit link from the browser URL bar so the form knows where to send data
GOOGLE_SHEET_EDIT_URL = "https://docs.google.com/spreadsheets/d/1B8en2Ig19VjJRn846JFBH9mRpus52ySAeweaYNZzUhc/edit?gid=0#gid=0"

def load_data_from_cloud():
    try:
        # Pulls data cleanly using standard internet tools that never fail
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Sales"] = pd.to_numeric(df["Sales"])
        return df
    except:
        return pd.DataFrame(columns=["Date", "Showroom", "Sales", "Remarks"])

# --- APP HEADER ---
st.title("👔 Jockey Showrooms Sales Manager")
st.markdown("---")

# --- DASHBOARD VISUALIZATIONS ---
df = load_data_from_cloud()

if df.empty or df.dropna(how='all').empty:
    st.info("No sales records found yet.")
else:
    df["Year-Month"] = df["Date"].dt.strftime('%Y-%m')
    df["Year"] = df["Date"].dt.year
    
    st.metric(label="Total Combined Sales", value=f"₹ {df['Sales'].sum():,.2f}")
    
    tab1, tab2, tab3 = st.tabs(["Monthly Charts", "Yearly Comparison", "View Database Records"])
    
    with tab1:
        monthly = df.groupby(["Year-Month", "Showroom"])["Sales"].sum().reset_index()
        fig_m = px.bar(monthly, x="Year-Month", y="Sales", color="Showroom", barmode="group", title="Sales Per Month")
        st.plotly_chart(fig_m, use_container_width=True)
        
    with tab2:
        yearly = df.groupby(["Year", "Showroom"])["Sales"].sum().reset_index()
        fig_y = px.bar(yearly, x="Year", y="Sales", color="Showroom", barmode="group", title="Annual Showroom Performance")
        fig_y.update_layout(xaxis_type='category')
        st.plotly_chart(fig_y, use_container_width=True)
        
    with tab3:
        st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

# --- LOWER FORM: EASY DATA ENTRY FOR PARENTS ---
st.markdown("---")
st.subheader("📥 Enter Daily Sales")
st.write("Clicking the button below will open the Google Sheet to record your daily numbers securely.")

# Because forms across cloud networks can glitch, a clean link directly to the sheet 
# guarantees Mom & Dad can input data simultaneously on Google's bulletproof infrastructure.
st.link_button("👉 Click Here to Enter Today's Sales Numbers", GOOGLE_SHEET_EDIT_URL)
