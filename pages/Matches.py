from unittest import result

import streamlit as st
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="Matches",
    page_icon="🏏",
)
st.set_page_config(layout="wide")
# loading the data into the matches file
train_df=pd.read_csv("cleaned_ipl_data.csv")
# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.title {
    background: linear-gradient(90deg, #0b1f4d, #1e3c72);
    padding: 30px;
    border-radius: 10px;
    color: white;
}
.card {
    background-color: #1e3c72;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}
.metric {
    font-size: 28px;
    font-weight: bold;
}
.small-text {
    color: gray;
}
</style>
""", unsafe_allow_html=True)
# ---------- HEADER ----------
st.markdown("""
<div class="title">
    <h4>INDIAN PREMIER LEAGUE(2008-2025)</h4>
   
</div>
""", unsafe_allow_html=True)
# User input
train_df['date'] = pd.to_datetime(train_df['date']).dt.date
st.markdown("""
<style>
/* Increase height & font size of date input */
div[data-testid="stDateInput"] input {
    height: 55px;
    font-size: 25px;
}
</style>
""", unsafe_allow_html=True)
a=st.subheader("Select a match date (2008–2025)")
d = st.date_input("")
YEAR=d.year
if YEAR < 2008 or YEAR > 2025:
    st.warning("Please select a date between 2008 and 2025.")
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExanppYjdsZjNnaGpuODM2Yml3dz\
        JtZ2F6eXJ2cWtoN201b214bXAwciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/u4kOABli4LqualwiPr/giphy.gif",caption="u didn't see the date did u? 🏏", width=300)
elif d:
    if d not in train_df['date'].unique():
        st.warning("No matches were played on this date.")

        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzRxZWhqazR4M2poZzZ2MmphNng2aHJ5eW1uMm85aDloN2Y4amo3OCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Wq9RLX06zRg4UM42Qf/giphy.gif", width=300, caption="Try selecting another date 🏏")
    else:
        matches_on_date = train_df[train_df['date'] == d]
        col1,col2=st.columns(2)
        col1.markdown(f"""
                    <div class="card">
                    <h5>{d}</h5>
                    <div class="metric">{matches_on_date['batting_team'].unique()[0]}({matches_on_date['target_score'].unique()[0]})  VS  {matches_on_date['bowling_team'].unique()[0]}({matches_on_date['chased_score'].unique()[0]})</div>
                    </div>
                    """, unsafe_allow_html=True)
        # creating a condtion to check wther the match won by runs or is it a tie match 
        if (matches_on_date['win_outcome'].iloc[0]=='tie'):
            st.subheader(f"{matches_on_date['match_won_by'].iloc[0]} Won the Super Over")
        else:   
            result=(f"{matches_on_date['match_won_by'].iloc[0]} Won by {matches_on_date['win_outcome'].iloc[0]}")
            st.success(f"🏆 {result}")
            st.balloons()
        st.header("Scorecard:")
        col1,col2,col3=st.columns(3)
        col1.markdown(f"""
                      <div class='card'>
                      <div class='metric'>{matches_on_date['batting_team'].unique()[0]} Innings
                      </div>""",unsafe_allow_html=True)
        col2.markdown(f"""
                      <div class='card'>
                       <h5>Matche Summary</h5>
                      </div>""",unsafe_allow_html=True)
        col3.markdown(f"""
                      <div class='card'>
                      <div class='metric'>{matches_on_date['bowling_team'].unique()[0]} Innings
                      </div>""",unsafe_allow_html=True)
        
        col1,col2,col3=st.columns(3)
        with col1:
            st.dataframe(train_df.head())