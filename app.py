# -*- coding: utf-8 -*-
import streamlit as st
import random
import time

st.set_page_config(page_title="Dice Game", layout="wide")

# 🎲 BIG TITLE
st.markdown(
    """
    <div style='text-align:center; font-size:42px; font-weight:800;'>
        🎲 DICE GAME 🎲
    </div>
    """,
    unsafe_allow_html=True
)

# 📜 SIMPLE RULES (now under title)
st.markdown(
    """
    <div style='text-align:center; font-size:22px; font-weight:600;'>
        Roll a number from 1 to 100 | 56 to 100 = WIN | 1 to 55 = Host Wins | 500 Buy-In | Max Bet 50
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Initialize session state
# -----------------------------
if "balances" not in st.session_state:
    st.session_state.balances = {}
if "wins" not in st.session_state:
    st.session_state.wins = {}
if "losses" not in st.session_state:
    st.session_state.losses = {}
if "last_roll" not in st.session_state:
    st.session_state.last_roll = {}
if "house" not in st.session_state:
    st.session_state.house = 5000

# -----------------------------
# 3 COLUMN DASHBOARD
# -----------------------------
left, center, right = st.columns([1, 2, 1], gap="small")

# -----------------------------
# LEFT PANEL (Add Player)
# -----------------------------
with left:
    name_col, btn_col = st.columns([3,1])
    with name_col:
        name = st.text_input("Player", label_visibility="collapsed", placeholder="Add player")
    with btn_col:
        add_clicked = st.button("➕")

    if add_clicked:
        if name and name not in st.session_state.balances:
            st.session_state.balances[name] = 500
            st.session_state.wins[name] = 0
            st.session_state.losses[name] = 0
            st.session_state.last_roll[name] = None

# -----------------------------
# CENTER PANEL (GAME ACTION)
# -----------------------------
with center:
    if st.session_state.balances:
        row = st.columns([2,1])
        with row[0]:
            player = st.selectbox("Player", list(st.session_state.balances.keys()))
        with row[1]:
            bet = st.slider("Bet 🎯", 1, 50, 10)

        roll_display = st.empty()

        if st.button("ROLL 🎲", use_container_width=True):

            if bet > st.session_state.balances[player]:
                st.warning("Not enough tokens")
            else:
                # 🎲 5 SECOND ROLL ANIMATION
                for _ in range(50):  # 50 frames
                    roll_display.markdown(
                        f"<h1 style='text-align:center;font-size:80px;'>🎲 {random.randint(1,100)}</h1>",
                        unsafe_allow_html=True
                    )
                    time.sleep(0.1)  # 0.1 x 50 ≈ 5 seconds

                roll = random.randint(1, 100)
                st.session_state.last_roll[player] = roll

                roll_display.markdown(
                    f"<h1 style='text-align:center;font-size:100px;'>🎲 {roll}</h1>",
                    unsafe_allow_html=True
                )

                if roll > 55:
                    st.session_state.balances[player] += bet
                    st.session_state.wins[player] += 1
                    st.session_state.house -= bet
                    st.balloons()
                    st.success(f"{player} WINS {bet}!")
                else:
                    st.session_state.balances[player] -= bet
                    st.session_state.losses[player] += 1
                    st.session_state.house += bet
                    st.error(f"Host wins {bet}!")

# -----------------------------
# RIGHT PANEL (Stats)
# -----------------------------
with right:
    st.metric("🎤 Host Tokens", st.session_state.house)

    for p in st.session_state.balances:
        bal = st.session_state.balances[p]
        w = st.session_state.wins[p]
        l = st.session_state.losses[p]
        last = st.session_state.last_roll[p]
        roll_text = f" 🎲{last}" if last else ""
        st.write(f"**{p}** 💰{bal} | ✅{w} ❌{l}{roll_text}")

    if st.button("🔄 Reset"):
        st.session_state.balances.clear()
        st.session_state.wins.clear()
        st.session_state.losses.clear()
        st.session_state.last_roll.clear()
        st.session_state.house = 5000
