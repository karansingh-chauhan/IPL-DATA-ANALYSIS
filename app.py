import streamlit as st
import pandas as pd
# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="IPL Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
df=pd.read_csv("data\\cleaned_ipl_data.csv")
# -----------------------
# CUSTOM SIDEBAR DESIGN
# -----------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #1e293b);
    color: white;
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] label {
    color: white;
}

/* Add spacing */
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# SIDEBAR HEADER
# -----------------------
st.sidebar.markdown("## 🏏 IPL Dashboard")
st.sidebar.markdown("---")

# Optional logo
st.sidebar.image(
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDsidp4Iv6d2bFb62u6R1OC1KRR_jFxeOqKA&s",
    use_container_width=True
)

st.sidebar.markdown("---")

# -----------------------
# PAGE SETUP
# -----------------------
home_page = st.Page(
    page="pages/home.py",
    title="🏠 Home",
    default=True
)

match_page = st.Page(
    page="pages/Matches.py",
    title="📅 Matches"
)

team_page = st.Page(
    page="pages/Teams.py",
    title="👥 Player"
)
analyze_page = st.Page(
    page="pages/tmkoc.py",
    title="👥 tmkoc"
)

# -----------------------
# NAVIGATION
# -----------------------
pg = st.navigation(
    pages=[home_page, match_page, team_page, analyze_page]
)

# -----------------------
# SIDEBAR EXTRA (INTERACTIVE)
# -----------------------
st.sidebar.markdown("### 📊 Quick Stats")

# dummy placeholders (replace with real data)
st.sidebar.metric("Matches",f"{df['match_id'].nunique()}")
st.sidebar.metric("Teams", f"{df['batting_team'].nunique()}")

st.sidebar.markdown("---")

# Filters section
# with st.sidebar.expander("⚙️ Filters"):
#     st.selectbox("Season", ["2023", "2024", "2025"])
#     st.selectbox("Team", ["All", "MI", "CSK", "RCB"])

# -----------------------
# RUN APP
# -----------------------
pg.run()