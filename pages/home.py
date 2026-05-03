import streamlit as st
import pandas as pd
import numpy as np
# importing the team analysis csv for overall analysis
df=pd.read_csv("data\\team_analysis_df.csv")
bower_df=pd.read_csv("data\\bowler_wicket_runs.csv")
train_df=pd.read_csv("data\\cleaned_ipl_data.csv")
st.set_page_config(layout="wide")
st.set_page_config(
    page_title="Home",
    page_icon="🏦",
)
# ------page setup ------
# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.header {
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
<div class="header">
    <h4>WELCOME TO IPL STATS HUB</h4>
    <h1>The Ultimate Home of IPL Insights (2008-2025)</h1>
    <p>Explore powerful analytics, records, and match insights.</p>
</div>
""", unsafe_allow_html=True)
# assing the value for the header folder

# # ---------- KPI CARDS ----------
col1, col2, col3, col4 = st.columns(4)
total_matches = df['match_id'].nunique()
col1.markdown(f"""
<div class="card">
    <h5>Total Matches</h5>
    <div class="metric">{total_matches}</div>
</div>
""", unsafe_allow_html=True)
col2.markdown(f"""
<div class="card">
    <h5>Total Seasons</h5>
    <div class="metric">{df['year'].nunique()}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="card">
    <h5>Total Runs</h5>
    <div class="metric">{train_df['runs_batter'].sum()}</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="card" style="border-left: 5px solid #ff4b4b; padding-left: 10px;">
    <h5>Total Wickets</h5>
    <div class="metric">{bower_df['bowler_wicket'].sum()}</div>
</div>
""", unsafe_allow_html=True)
st.markdown("## IPL At a Glance")

# ---------- SMALL STATS ----------
most_bowler=bower_df.groupby('bowler')['bowler_wicket'].sum().reset_index().sort_values(by='bowler_wicket',ascending=False).head(1)
best_bowler=bower_df.head(1)
c1, c2, c3, c4, c5, c6 = st.columns(6)
@st.cache_data
def most_runs_overall(df):
    return(
        df.groupby('batter')['runs_batter'].sum().reset_index().sort_values(by='runs_batter',ascending=False).head(1)
        )
most_runs_overalldf=most_runs_overall(train_df)
c1.metric("Most Runs", 
          most_runs_overalldf['runs_batter'].iloc[0],
          most_runs_overalldf['batter'].iloc[0]
          )
@st.cache_data
def most_runs(df):
    return(
        df.groupby(['season','batter'])['runs_batter'].sum().reset_index().sort_values(by='runs_batter',ascending=False).head(1) 
        )
most_runs_seasondf=most_runs(train_df)
c2.metric(
    "Most Season Runs",
    most_runs_seasondf['runs_batter'].iloc[0],
    most_runs_seasondf['batter'].iloc[0]
    )

c3.metric(
    "Most Wickets",
    most_bowler['bowler_wicket'].iloc[0],
    most_bowler['bowler'].iloc[0]
)
c4.metric(
    "Best Bowling",
    f"{best_bowler['bowler_wicket'].iloc[0]}/{best_bowler['runs_bowler'].iloc[0]}",
    best_bowler['bowler'].iloc[0]
)
# most catches and most matches are calculated in the main.ipynb file and the values are assigned here
@st.cache_data
def wicket_keeper(df):
    return df.loc[df['wicket_kind'] == 'stumped', 'fielders'].dropna()

wickets_keeper1 = wicket_keeper(train_df).unique()
@st.cache_data
def get_top_catches(df,wkt):
    return (
        df[
            (df['wicket_kind'] == 'caught') &
            (~df['fielders'].isin(wkt))
        ]
        .groupby('fielders')
        .size()
        .reset_index(name='count')
        .sort_values(by='count', ascending=False)
    )

top_catches_df = get_top_catches(train_df,wickets_keeper1).head(1)
#----------------------------------------------------------------------------->
c5.metric("Most Catches",f"{top_catches_df['count'].iloc[0]}",top_catches_df['fielders'].iloc[0])

#most matches played by indevizula canbe some cntrovertialas it is not simmiler to onlinenet
@st.cache_data
def get_most_matches(df):
        batter=df[['match_id','batter']].rename(columns={'batter':'player'})
        bowler=df[['match_id','bowler']].rename(columns={'bowler':'player'})
        fielder=df[['match_id','fielders']].rename(columns={'fielders':'player'})
        playersinmatch=pd.concat([bowler,batter,fielder])
        playersinmatch=playersinmatch.drop_duplicates()
        # Remove repeated appearance of same player in same 

        matches_count = (
        playersinmatch.groupby('player')['match_id'].nunique().reset_index(name='matches').sort_values(by='matches', ascending=False)
    )

        return matches_count
matches_df = get_most_matches(train_df)
top_match_player = matches_df.iloc[0]

c6.metric("Most Matches", f"{top_match_player['matches']}",top_match_player['player'])


# # ---------- TABLE SECTION ----------
# ---------- TOP PLAYERS ----------
col1, col2,col3 = st.columns(3)
# df for the final teamsincludeing the top final teams and the number of times they have won the final
@st.cache_data
def get_final_teams(df):
    mst=df[df['stage']=='Final'].drop_duplicates(subset=['match_id','date'])
    mst=mst['match_won_by'].value_counts().reset_index().sort_values(by='count', ascending=False)
    return mst
final_teams_df = get_final_teams(train_df)
with col1:
    st.markdown("### Most Successful Teams")
    st.dataframe(final_teams_df)
# top run scorers calculation
@st.cache_data
def get_top_run_scorers(df):
    return df.groupby('batter')['runs_batter'].sum().reset_index().sort_values(by='runs_batter', ascending=False)

top_run_scorers_df=get_top_run_scorers(train_df)
with col2:
    st.markdown("### Top Run Scorers")
    st.dataframe(top_run_scorers_df.reset_index(drop=True))
# top wicket takers calculatioon
@st.cache_data
def get_top_wicket_takers(df):
    return df.groupby('bowler')[['bowler_wicket','runs_bowler','valid_ball']].sum().reset_index().sort_values(by='bowler_wicket', ascending=False)
top_wicket_takers_df=get_top_wicket_takers(train_df)
with col3:
    st.markdown("### Top Wicket Takers")
    st.dataframe(top_wicket_takers_df.reset_index(drop=True))
# highest run in ipl
col1, col2,col3,col4 = st.columns(4)

with col1:
    st.markdown("### Highest team total")
    @st.cache_data
    def highest_team_total_df(df):
        higest_team_total=df.groupby(["date","batting_team"])['bowler_wicket'].sum().reset_index()
        higest_team_total = higest_team_total.merge(df[['date','innings','batting_team','target_score']],\
        on=['date','batting_team'],how='left').sort_values(by=['innings','target_score'],ascending=[True,False]).drop_duplicates(subset=['date','batting_team'])
        higest_team_total['scorecard']=higest_team_total['target_score'].astype(str)+"/"+higest_team_total['bowler_wicket'].astype(str)
        return higest_team_total
    highest_team_total=highest_team_total_df(train_df)
    st.dataframe(highest_team_total[['batting_team','scorecard']].reset_index(drop=True))
with col2:
    st.markdown("### Most win Season")
    @st.cache_data
    def most_win_season(df):
        mostwin=df.groupby('season')['match_won_by'].value_counts().reset_index().sort_values(by='count',ascending=False)
        mostwin['team_season']=mostwin['match_won_by']+"   ("+mostwin['season'].astype(str)+")"
        return mostwin
    most_win_season_df=most_win_season(df)
    st.dataframe(most_win_season_df[['team_season','count']].reset_index(drop=True))
with col3:
    st.markdown("### Most 6s in Season ")
    @st.cache_data
    def most_6s_season(df):
        new_df=df[df['innings']<=2]
        most_6s=new_df.groupby(['season','batter'])['6s'].sum().reset_index().sort_values(by='6s',ascending=False)
        most_6s['batter_season']=most_6s['batter']+"   ("+most_6s['season'].astype(str)+")"
        return most_6s
    most_6s_season_df=most_6s_season(train_df)
    st.dataframe(most_6s_season_df[['batter_season','6s']].reset_index(drop=True))
with col4:
    st.markdown("### Most 4s in Season")
    @st.cache_data
    def most_4s_season(df):
        new_df=df[df['innings']<=2]
        most_4s=new_df.groupby(['season','batter'])['4s'].sum().reset_index().sort_values(by='4s',ascending=False)
        most_4s['batter_season']=most_4s['batter']+"   ("+most_4s['season'].astype(str)+")"
        return most_4s
    most_4s_season_df=most_4s_season(train_df)
    st.dataframe(most_4s_season_df[['batter_season','4s']].reset_index(drop=True))