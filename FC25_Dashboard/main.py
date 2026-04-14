import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="FC 25 Dashboard", layout="wide")

st.title("⚽ FC 25 Ultimate Team Dashboard")
st.markdown("Analysi l-performance dyal l-l3aba f FC 25")



@st.cache_data
def load_data():
    df = pd.read_csv("all_players.csv")
    return df


try:
    df = load_data()

    st.sidebar.header("🔍 Filtres")

    leagues = df['League'].unique()
    selected_league = st.sidebar.selectbox("Khtar l-Botola (League):", leagues)

    teams = df[df['League'] == selected_league]['Team'].unique()
    selected_team = st.sidebar.selectbox("Khtar l-Fari9 (Team):", teams)


    filtered_df = df[(df['League'] == selected_league) & (df['Team'] == selected_team)]


    st.subheader(f"{selected_team} statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("players numbers", len(filtered_df))
    with col2:
        st.metric("average age", f"{filtered_df['Age'].mean():.1f} ans")
    with col3:
        best_player = filtered_df.loc[filtered_df['OVR'].idxmax()]
        st.metric("best player (OVR)", f"{best_player['Name']} ({best_player['OVR']})")

    # table
    st.write("### 📋 players List ")
    cols_to_show = ['Name', 'Age', 'Nation', 'Position', 'OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
    st.dataframe(filtered_df[cols_to_show], use_container_width=True)



    # ==========================================
    # GRAPHES
    # ==========================================
    st.write("### 📊 Top 10 players ")
    top_10 = filtered_df.sort_values(by='OVR', ascending=False).head(10)
    st.bar_chart(top_10.set_index('Name')['OVR'])

    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        st.write("### ⚡ PAC vs SHO")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=filtered_df,
            x='PAC',
            y='SHO',
            hue='Position',
            style='Position',
            s=100,
            ax=ax1
        )
        plt.title(f" shooting and speed - {selected_team}")
        plt.xlabel(" Pace")
        plt.ylabel("Shooting")
        plt.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig1)

    with col_graph2:
        st.write("### 🛡️ DEF vs DRI")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.scatterplot(
            data=filtered_df,
            x='DRI',
            y='DEF',
            hue='Position',
            style='Position',
            s=100,
            ax=ax2
        )
        plt.title(f" Dribble and Defence - {selected_team}")
        plt.xlabel("Dribble (DRI)")
        plt.ylabel("Defence (DEF)")
        plt.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig2)

# ==========================================
#EXCEPTIONS
# ==========================================
except FileNotFoundError:
    st.error("⚠️ file not found 'all_players.csv'. make sure you put it near  main.py!")
except Exception as e:
    st.error(f"Oups! there is a problem: {e}")