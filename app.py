# -*- coding: utf-8 -*-
import streamlit as st
import random
import time

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Dice Token Game",
    layout="wide"  # wide allows columns on tablets/desktop
)

st.title("Dice Token Game 🎲")
st.caption("Roll 1–100. Any roll >55 wins!")

# -----------------------------
# Initialize session state
# -----------------------------
if "balances" not in st.session_state:
    st.session_state["balances"] = {}
if "wins" not in st.session_state:
    st.session_state["wins"] = {}
if "losses" not in st.session_state:
    st.session_state["losses"] = {}
if "last_roll" not in st.session_state:
    st.session_state["last_roll"] = {}
if "house" not in st.session_state:
    st.session_state["house"] = 5000  # house bankroll

# -----------------------------
# Reset Game
# -----------------------------
st.markdown("---")
if st.button("🔄 Reset Game"):
    st.session_state.balances.clear()
    st.session_state.wins.clear()
    st.session_state.losses.clear()
    st.session_state.last_roll.clear()
    st.session_state.house = 5000
    st.success("Game reset! All player data cleared, house bankroll reset to 5,000.")

st.markdown("---")

# -----------------------------
# Add / Initialize Player
# -----------------------------
st.subheader("Add / Initialize Player")
col1, col2 = st.columns([2, 1])

with col1:
    player_name = st.text_input("Enter player name to add")

with col2:
    if st.button("Add Player"):
        if not player_name:
            st.warning("Enter a player name!")
        elif player_name in st.session_state.balances:
            st.warning(f"{player_name} already exists with {st.session_state.balances[player_name]} tokens.")
        else:
            st.session_state.balances[player_name] = 500  # fixed buy-in
            st.session_state.wins[player_name] = 0
            st.session_state.losses[player_name] = 0
            st.session_state.last_roll[player_name] = None
            st.success(f"Player {player_name} added with 500 tokens (buy-in).")

st.markdown("---")

# -----------------------------
# Dice Roll Section
# -----------------------------
st.subheader("🎲 Roll Dice")
if st.session_state.balances:
    col1, col2 = st.columns([2, 1])

    with col1:
        selected_player = st.selectbox("Select player", list(st.session_state.balances.keys()))

    with col2:
        bet = st.number_input(
            "Bet (max 50)",
            min_value=1,
            max_value=50,
            step=1
        )

    if st.button("Roll Dice", key="roll"):
        if bet > st.session_state.balances[selected_player]:
            st.warning(f"{selected_player} only has {st.session_state.balances[selected_player]} tokens!")
        else:
            with st.spinner("Rolling the dice..."):
                time.sleep(2)

            roll = random.randint(1, 100)
            st.session_state.last_roll[selected_player] = roll

            if roll > 55:
                st.session_state.balances[selected_player] += bet
                st.session_state.wins[selected_player] += 1
                st.session_state.house -= bet
                st.success(f"{selected_player} rolled {roll} and wins {bet} tokens!")
            else:
                st.session_state.balances[selected_player] -= bet
                st.session_state.losses[selected_player] += 1
                st.session_state.house += bet
                st.error(f"{selected_player} rolled {roll}. House wins {bet} tokens!")

st.markdown("---")

# -----------------------------
# Player Balances & House Bankroll (Columns)
# -----------------------------
st.subheader("Player Balances & House Bankroll")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧑 Players")
    for player in st.session_state.balances:
        balance = st.session_state.balances[player]
        wins = st.session_state.wins.get(player, 0)
        losses = st.session_state.losses.get(player, 0)
        last_roll = st.session_state.last_roll.get(player)
        roll_text = f" | Last Roll: {last_roll}" if last_roll is not None else ""
        st.write(f"{player}: Balance={balance} | Wins={wins} | Losses={losses}{roll_text}")

with col2:
    st.markdown("### 🏠 House Bankroll")
    st.metric(label="House Tokens", value=st.session_state.house)

st.markdown("---")

# -----------------------------
# Leaderboard
# -----------------------------
st.subheader("🏆 Leaderboard (Most Wins)")
sorted_leaderboard = sorted(st.session_state.wins.items(), key=lambda x: x[1], reverse=True)
for player, win_count in sorted_leaderboard:
    st.write(f"{player}: {win_count} wins")
