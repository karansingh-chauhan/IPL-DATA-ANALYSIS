import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏏 Player Performance Dashboard")

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("data\\cleaned_ipl_data.csv")  # update path

df = load_data()

# -----------------------
# PLAYER SELECTION
# -----------------------
# combine batter + bowler names
players = pd.concat([df['batter'], df['bowler']]).dropna().unique()
players = sorted(players)

selected_player = st.selectbox("Select Player", players, index=0)

# filter data
bat_df = df[df['batter'] == selected_player]
bowl_df = df[df['bowler'] == selected_player]
batting_data=df['batter'].unique()
bowling_data=df['bowler'].unique()

# -----------------------
# LAYOUT
# -----------------------
tab1, tab2 = st.tabs(["🏏 Batting Stats", "🎯 Bowling Stats"])

# =======================
# 🏏 BATTING TAB
# =======================
with tab1:

    if len(bat_df) == 0:
        st.warning("No batting data available")
    elif selected_player not in batting_data:
        st.warning(" No batting data  found")
    else:
        runs = bat_df['runs_batter'].sum()
        balls = bat_df.shape[0]
        dismissals = bat_df[bat_df['bowler_wicket'] == selected_player].shape[0]

        strike_rate = (runs / balls) * 100 if balls > 0 else 0
        avg = (runs / dismissals) if dismissals > 0 else runs

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Runs", runs)
        col2.metric("Balls", balls)
        col3.metric("Strike Rate", round(strike_rate, 2))
        col4.metric("Average", round(avg, 2))

        # -----------------------
        # Runs per over
        # -----------------------
        runs_over = bat_df.groupby('over')['runs_batter'].sum().reset_index()

        fig1 = px.bar(
            runs_over,
            x='over',
            y='runs_batter',
            title="Runs per Over"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # -----------------------
        # Cumulative runs (worm)
        # -----------------------
        bat_df = bat_df.copy()
        bat_df['cumulative_runs'] = bat_df['runs_batter'].cumsum()

        fig2 = px.line(
            bat_df,
            x=bat_df.index,
            y='cumulative_runs',
            title="Cumulative Runs"
        )
        st.plotly_chart(fig2, use_container_width=True)

# =======================
# 🎯 BOWLING TAB
# =======================
with tab2:

    if len(bowl_df) == 0:
        st.warning("No bowling data available")
    elif selected_player not in bowling_data:   
        st.warning(" No bowling data  found")
    else:
        runs_conceded = bowl_df['runs_batter'].sum()
        balls = bowl_df.shape[0]
        wickets = bowl_df['bowler_wicket'].sum()

        overs = bowl_df.shape[0]/6
        economy = (runs_conceded / overs) if overs > 0 else 0

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Wickets", wickets)
        col2.metric("Runs Conceded", runs_conceded)
        col3.metric("Overs", round(overs, 2))
        col4.metric("Economy", round(economy, 2))

        # -----------------------
        # Runs conceded per over
        # -----------------------
        bowl_over = bowl_df.groupby('over')['runs_batter'].sum().reset_index()

        fig3 = px.bar(
            bowl_over,
            x='over',
            y='runs_batter',
            title="Runs Conceded per Over"
        )
        st.plotly_chart(fig3, use_container_width=True)

        # -----------------------
        # Wickets distribution
        # -----------------------
        wickets_type = bowl_df['wicket_kind'].value_counts().reset_index()
        wickets_type.columns = ['type', 'count']

        fig4 = px.pie(
            wickets_type,
            names='type',
            values='count',
            title="Wicket Types"
        )
        st.plotly_chart(fig4, use_container_width=True)