import streamlit as st
import pandas as pd
import plotly.express as px
import sys
st.write(sys.version)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Matches",
    page_icon="🏏",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
.main {
    background-color: #f5f7fb;
}

/* Header */
.title {
    background: linear-gradient(90deg, #0b1f4d, #1e3c72);
    padding: 25px;
    border-radius: 10px;
    color: white;
    text-align: center;
}

/* Tabs Styling (WORKING FIX) */
div[role="tablist"] button p {
    font-size: 20px !important;
    font-weight: bold !important;
}

/* Date Input */
div[data-testid="stDateInput"] input {
    height: 50px;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    cleaned_ipl_data = "https://drive.google.com/uc?export=download&id=1e2-twd_ih87O2bmXWZpEGJR5KMLiIEMA"
    df = pd.read_csv(cleaned_ipl_data)
    df['date'] = pd.to_datetime(df['date']).dt.date
    return df

train_df = load_data()

# ---------------- HEADER ----------------
st.markdown("""
<div class="title">
    <h2>🏏 IPL Match Explorer (2008–2025)</h2>
</div>
""", unsafe_allow_html=True)

st.subheader("Select a match date")
d = st.date_input("")

# ---------------- DATE VALIDATION ----------------
if d:
    if d.year < 2008 or d.year > 2025:
        st.warning("Please select a valid IPL year (2008–2025)")
        st.stop()

    matches_on_date = train_df[train_df['date'] == d]

    if matches_on_date.empty:
        st.warning("No matches found on this date")
        st.stop()

    # ---------------- MATCH DATA ----------------
    row = matches_on_date.iloc[0]

    # ---------------- MATCH HEADER ----------------
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #0b1f4d, #1e3c72);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
    ">
        <h3>{row['batting_team']} 🆚 {row['bowling_team']}</h3>
        <h2>{row['target_score']} / {row['chased_score']}</h2>
        <p>{d}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- RESULT ----------------
    result = (
        f"{row['match_won_by']} won the Super Over"
        if row['win_outcome'] == 'tie'
        else f"{row['match_won_by']} won by {row['win_outcome']}"
    )

    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #1e3c72, #0b1f4d);
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid green;
        font-size: 18px;
        font-weight: bold;
    ">
    🏆 {result}
    </div>
    """, unsafe_allow_html=True)

    if row['stage'] == 'Final':
        st.balloons()

    # ---------------- FUNCTIONS ining 1----------------
    @st.cache_data
    def batting_team(df,i):
        df = df[df['innings'] ==i]
        df = (
            df.groupby(['batter','bat_pos'])[['runs_batter','balls_faced','4s','6s']]
            .sum()
            .reset_index()
            .sort_values(by='runs_batter', ascending=False)
        )
        df['SR'] = round((df['runs_batter'] / df['balls_faced']) * 100, 2)
        return df
      #  for the ining bowling team
    def battingbowll(df,i):
        df = df[df['innings'] ==i]
        df = (
            df.groupby(['bowler'])[['bowler_wicket','runs_bowler','valid_ball']]
            .sum()
            .reset_index()
            .sort_values(by='bowler_wicket', ascending=False)
        )
        return df

    @st.cache_data
    def top_runscore(df):
        df=(df.groupby('batter')['runs_batter']
        .sum()
        .reset_index()
        .sort_values(by='runs_batter', ascending=False)
        )
        return df
    # // topbowler wicket
    @st.cache_data
    def top_wicket(df):
        df=(df.groupby('bowler')['bowler_wicket']
        .sum()
        .reset_index()
        .sort_values(by='bowler_wicket', ascending=False)
        )
        return df
    batting_score_df = top_runscore(matches_on_date)
    bowling_wck_df = top_wicket(matches_on_date)
    #---------------function for the batting team--------------------
    
    #---------------function for the bolwling team--------------------
    # ---------------- HIGHLIGHTS ----------------
    st.markdown("### 📊 Match Highlights")

    col1, col2, col3 = st.columns(3)

    top_batter = batting_score_df.iloc[0]
    top_bowler = bowling_wck_df.sort_values(by='bowler_wicket', ascending=False).iloc[0]

    col1.metric("Top Scorer", top_batter['runs_batter'], top_batter['batter'])
    col2.metric("Best Bowler", top_bowler['bowler_wicket'], top_bowler['bowler'])
    # col3.metric("Strike Rate", top_batter['SR'])

    st.markdown("---")

    # ---------------- TABS ----------------
    tab1, tab2 ,tab3= st.tabs(["🏏 SUMMARY", "🎯 SCORECARD","🎢 GRAPH"])
    # -----------------summry ------------------- player of the match
    pom = row['player_of_match']

    # Check if player appeared as batter
    if pom in matches_on_date['batter'].values:
        team = row['batting_team']
    else:
        team = row['bowling_team']
    with tab1:
        st.markdown(f"""
        <div style="
        background: linear-gradient(90deg, #0b1f4d, #1e3c72);
        padding: 12px;
        border-radius:12px;
        color: white;
        text-align: left;
        ">
        <h2>Player of the Match</h2>
        <h3>{pom} ({team})</h3>
        </div>
         """, unsafe_allow_html=True)
        st.markdown("---")
        col1,col2,col3=st.columns([5,4,5])
        with col2:
            st.subheader(f"{row['batting_team']} - {row['target_score']}/{matches_on_date[matches_on_date['batting_team']==row['batting_team']]['bowler_wicket'].sum()}")# crestinga  stringehcihtellesthetesmnameandscorechased ormadewithwicket
        # st.dataframe(batting_df, use_container_width=True)
        col1,col2=st.columns([9,10])
        with col1:
            st.caption("batting")
            # calling the function for the top 3 batsmen in match
            ining1_match=batting_team(matches_on_date,1)
            st.dataframe(ining1_match[['batter','runs_batter','balls_faced']].head(3).reset_index(drop=True))
        with col2:
            st.caption("bowling")
            bowling_match=battingbowll(matches_on_date,1)
            st.dataframe(bowling_match[['bowler','bowler_wicket','runs_bowler']].head(3).reset_index(drop=True))
        #  creating a new dataframe colimd for the seconf ining 
        st.markdown("---")
        col1,col2,col3=st.columns([5,4,5])
        with col2:
            
            
            st.subheader(f"{row['bowling_team']} - {row['chased_score']}/{matches_on_date[matches_on_date['bowling_team']==row['batting_team']]['bowler_wicket'].sum()}")# crestinga  stringehcihtellesthetesmnameandscorechased ormadewithwicket
        # st.dataframe(batting_df, use_container_width=True)
        col1,col2=st.columns([9,10])
        with col1:
            st.caption("batting")
            # calling the function for the top 3 batsmen in match
            ining1_match=batting_team(matches_on_date,2)
            st.dataframe(ining1_match[['batter','runs_batter','balls_faced']].head(3).reset_index(drop=True))
        with col2:
            st.caption("bowling")
            bowling_match=battingbowll(matches_on_date,2)
            st.dataframe(bowling_match[['bowler','bowler_wicket','runs_bowler']].head(3).reset_index(drop=True))
        #  we have playedthe bowler of opposite team into the sd=ide of batsman from the other tea, 
        
    with tab2:
        st.subheader("Bowling Scorecard")

        tab1, tab2 = st.tabs([
            f"🏏 {row['batting_team']} Batting",
            f"🎯 {row['bowling_team']} Bowling"
        ])

        with tab1:
            extras_dict = matches_on_date[matches_on_date['innings']==1]['extra_type'].value_counts().to_dict()
# remove unwanted key
            extras_dict.pop('no_extra_runs', None)
            st.markdown("---")
            col1,col2,col3=st.columns([5,4,5])
            with col2:
                st.subheader(f"{row['batting_team']} - {row['target_score']}/{matches_on_date[matches_on_date['batting_team']==row['batting_team']]['bowler_wicket'].sum()}")# crestinga  stringehcihtellesthetesmnameandscorechased ormadewithwicket
        # st.dataframe(batting_df, use_container_width=True)
            st.dataframe(batting_team(matches_on_date, 1).reset_index(drop=True))
            st.badge(f"Extras = {matches_on_date[matches_on_date['innings']==1]['runs_extras'].sum()} {extras_dict}", color="red")
            st.badge(f"TEAM TOTAL SCORE = {row['target_score']-1}")
            st.dataframe(battingbowll(matches_on_date, 2).reset_index(drop=True))
        with tab2:
            extras_dict = matches_on_date[matches_on_date['innings']==2]['extra_type'].value_counts().to_dict()
# remove unwanted key
            extras_dict.pop('no_extra_runs', None)
            st.markdown("---")
            col1,col2,col3=st.columns([5,4,5])
            with col2:
                st.subheader(f"{row['bowling_team']} - {row['chased_score']}/{matches_on_date[matches_on_date['bowling_team']==row['batting_team']]['bowler_wicket'].sum()}")# crestinga  stringehcihtellesthetesmnameandscorechased ormadewithwicket
        # st.dataframe(batting_df, use_container_width=True)
            st.dataframe(batting_team(matches_on_date, 2).reset_index(drop=True))
            st.badge(f"Extras = {matches_on_date[matches_on_date['innings']==2]['runs_extras'].sum()} {extras_dict}", color="red")
            st.badge(f"TEAM TOTAL SCORE = {row['chased_score']}")
            st.dataframe(battingbowll(matches_on_date,1).reset_index(drop=True))
        
        with tab3:
            
            st.subheader("📊 Match Insights Dashboard")

            # -----------------------------
            # DATA (your match dataframe)
            # -----------------------------
            df = matches_on_date.copy()

            # -----------------------------
            # SIDEBAR / FILTERS
            # -----------------------------
            teams = df['batting_team'].unique()

            col1, col2 = st.columns(2)

            with col1:
                selected_team = st.selectbox("Select Team", teams)

            with col2:
                over_range = st.slider("Select Over Range", 1, 20, (1, 20))

            # -----------------------------
            # FILTER DATA
            # -----------------------------
            filtered_df = df[
                (df['over'] >= over_range[0]) &
                (df['over'] <= over_range[1])
            ]

            team_df = filtered_df[filtered_df['batting_team'] == selected_team]

            # -----------------------------
            # GRAPH 1: WORM GRAPH (Runs Progression)
            # -----------------------------
            st.markdown("### 🐛 Runs Progression (Worm Graph)")

            worm_data = filtered_df.groupby(['over', 'batting_team'])['runs_batter'].sum().reset_index()

            fig1 = px.line(
                worm_data,
                x='over',
                y='runs_batter',
                color='batting_team',
                markers=True
            )

            st.plotly_chart(fig1, use_container_width=True)

            # -----------------------------
            # GRAPH 2: MANHATTAN CHART
            # -----------------------------
            st.markdown("### 🏙️ Runs Per Over (Manhattan Chart)")

            manhattan = team_df.groupby('over')['runs_batter'].sum().reset_index()

            fig2 = px.bar(
                manhattan,
                x='over',
                y='runs_batter',
                title=f"{selected_team} Runs Per Over"
            )

            st.plotly_chart(fig2, use_container_width=True)

            # -----------------------------
            # GRAPH 3: TEAM COMPARISON
            # -----------------------------
            st.markdown("### ⚔️ Team Comparison")

            comparison = filtered_df.groupby(['batting_team'])['runs_batter'].sum().reset_index()

            fig3 = px.pie(
                comparison,
                names='batting_team',
                values='runs_batter',
                title="Total Runs Contribution"
            )

            st.plotly_chart(fig3, use_container_width=True)

            # -----------------------------
            # GRAPH 4: STRIKE RATE TREND
            # -----------------------------
            st.markdown("### 🔥 Strike Rate Trend")

            sr_data = team_df.groupby('over').agg({
                'runs_batter': 'sum',
                'balls_faced': 'count'
            }).reset_index()

            sr_data['strike_rate'] = (sr_data['runs_batter'] / sr_data['balls_faced']) * 100

            fig4 = px.line(
                sr_data,
                x='over',
                y='strike_rate',
                markers=True,
                title=f"{selected_team} Strike Rate"
            )

            st.plotly_chart(fig4, use_container_width=True)