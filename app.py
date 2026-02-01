# -*- coding: utf-8 -*-
import streamlit as st
import random
import time
import requests

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Dice Game", layout="wide")

st.markdown(
    "<div style='text-align:center; font-size:38px; font-weight:800;'>🎲 DICE GAME 🎲</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div style='text-align:center; font-size:22px; font-weight:600;'>🎯 Roll 1–100 | ✅ 56–100 WIN | ❌ 1–55 Host Wins | 💰 500 Buy-In</div>",
    unsafe_allow_html=True
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "balances" not in st.session_state:
    st.session_state.balances = {}

if "last_roll" not in st.session_state:
    st.session_state.last_roll = {}

# -----------------------------
# LAYOUT
# -----------------------------
left, center, right = st.columns([1, 2, 1])

# -----------------------------
# LOAD PLAYERS FROM SERVER
# -----------------------------
if not st.session_state.balances:
    try:
        r = requests.get("http://127.0.0.1:8000/players")
        data = r.json()
        for name, balance in data.items():
            st.session_state.balances[name] = balance
            st.session_state.last_roll[name] = None
    except:
        st.warning("⚠️ FastAPI server not running")

# -----------------------------
# ADD PLAYER
# -----------------------------
with left:
    st.subheader("Add Player")
    name = st.text_input("Player name")

    if st.button("➕ Add Player"):
        if name:
            r = requests.post(f"http://127.0.0.1:8000/signup?name={name}")
            data = r.json()

            if "error" in data:
                st.warning(data["error"])
            else:
                st.session_state.balances[name] = data["balance"]
                st.session_state.last_roll[name] = None

# -----------------------------
# GAME PLAY
# -----------------------------
with center:
    if st.session_state.balances:
        player = st.selectbox("Player", list(st.session_state.balances.keys()))
        bet = st.slider("Bet 🎯", 1, 500, 10)
        roll_display = st.empty()

        can_play = st.session_state.balances[player] > 0
if st.button("ROLL 🎲", use_container_width=True, disabled=not can_play):

            # 🎞️ Fake animation
            for _ in range(40):
                roll_display.markdown(
                    f"<h1 style='text-align:center;font-size:80px;'>🎲 {random.randint(1,100)}</h1>",
                    unsafe_allow_html=True
                )
                time.sleep(0.05)

            # 🎲 REAL roll from server
            r = requests.post(
                "http://127.0.0.1:8000/roll",
                json={"name": player, "amount": bet}
            )
            data = r.json()

            if "error" in data:
                st.error(data["error"])
            else:
                roll = data["roll"]
                result = data["result"]
                balance = data["balance"]

                st.session_state.balances[player] = balance
                st.session_state.last_roll[player] = roll

                roll_display.markdown(
                    f"<h1 style='text-align:center;font-size:100px;'>🎲 {roll}</h1>",
                    unsafe_allow_html=True
                )

                if result == "win":
                    st.balloons()
                    st.success(f"🔥 {player} wins {bet}!")
                else:
                    st.error(f"💀 Host wins {bet}")

# -----------------------------
# STATS PANEL
# -----------------------------
with right:
    st.subheader("Players")
    for p, bal in st.session_state.balances.items():
        last = st.session_state.last_roll[p]
        st.write(f"**{p}** — 💰 {bal} 🎲 {last if last else ''}")

    # -----------------------------
    # HOST BALANCE
    # -----------------------------
    try:
        r = requests.get("http://127.0.0.1:8000/host")
        host_data = r.json()
        st.write(f"🏦 **Host Bank:** {host_data['host_balance']}")
    except:
        pass

    # -----------------------------
    # RESET BUTTON
    # -----------------------------
    if st.button("🔄 Reset Game"):
        requests.post("http://127.0.0.1:8000/reset")
        st.session_state.balances = {}
        st.session_state.last_roll = {}
        st.experimental_rerun()
