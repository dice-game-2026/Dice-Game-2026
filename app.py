import streamlit as st
import random
import time

st.set_page_config(page_title="Dice Token Game", page_icon="🎲")
st.title("🎲 Dice Token Game")

st.markdown(
    "<p style='color:green; font-weight:bold'>🎯 Roll a number from 1-100. Any roll over 55 wins!</p>",
    unsafe_allow_html=True
)

# --- Initialize session state ---
if "balances" not in st.session_state:
    st.session_state["balances"] = {}
if "wins" not in st.session_state:
    st.session_state["wins"] = {}
if "losses" not in st.session_state:
    st.session_state["losses"] = {}
if "last_roll" not in st.session_state:
    st.session_state["last_roll"] = {}

# --- Reset Game ---
if st.button("🔄 Reset Game"):
    st.session_state.balances.clear()
    st.session_state.wins.clear()
    st.session_state.losses.clear()
    st.session_state.last_roll.clear()
    st.success("Game reset! All player data cleared.")

st.markdown("---")

# --- Add / Initialize Player ---
st.subheader("➕ Add / Initialize Player")
player_name = st.text_input("Enter player name to add")
starting_tokens = st.number_input("Enter starting tokens", min_value=1, step=1)

if st.button("Add Player"):
    if not player_name:
        st.warning("Enter a player name!")
    elif player_name in st.session_state.balances:
        st.warning(f"Player {player_name} already exists with {st.session_state.balances[player_name]} tokens.")
    else:
        st.session_state.balances[player_name] = starting_tokens
        st.session_state.wins[player_name] = 0
        st.session_state.losses[player_name] = 0
        st.session_state.last_roll[player_name] = None
        st.success(f"Player {player_name} added with {starting_tokens} tokens!")

st.markdown("---")

# --- Top Up Tokens Section ---
st.subheader("💰 Top Up Tokens")
if st.session_state.balances:
    topup_player = st.selectbox("Select player to add tokens", list(st.session_state.balances.keys()))
    topup_amount = st.number_input("Number of tokens to add", min_value=1, step=1, key="topup_amount")
    if st.button("Add Tokens"):
        st.session_state.balances[topup_player] += topup_amount
        st.success(f"{topup_player} now has {st.session_state.balances[topup_player]} tokens!")

st.markdown("---")

# --- Dice Roll Section ---
st.subheader("🎲 Roll Dice")
if st.session_state.balances:
    selected_player = st.selectbox("Select player", list(st.session_state.balances.keys()), key="roll_player")
    bet = st.number_input("Enter token bet", min_value=1, step=1, key="roll_bet")

    if st.button("Roll Dice"):
        if bet > st.session_state.balances[selected_player]:
            st.warning(f"{selected_player} only has {st.session_state.balances[selected_player]} tokens! Use 'Top Up Tokens' to add more.")
        else:
            with st.spinner("Rolling the dice..."):
                time.sleep(2)

            roll = random.randint(1, 100)
            st.session_state.last_roll[selected_player] = roll

            if roll > 55:
                st.session_state.balances[selected_player] += bet
                st.session_state.wins[selected_player] += 1
                st.markdown(f"<h2 style='color:green'>🎲 {selected_player} rolled: {roll}</h2>", unsafe_allow_html=True)
                st.success(f"🎉 {selected_player} wins {bet} tokens! (Profit: {bet} tokens)")
            else:
                st.session_state.balances[selected_player] -= bet
                st.session_state.balances[selected_player] = max(0, st.session_state.balances[selected_player])
                st.session_state.losses[selected_player] += 1
                st.markdown(f"<h2 style='color:red'>🎲 {selected_player} rolled: {roll}</h2>", unsafe_allow_html=True)
                st.error(f"🏠 House wins! {selected_player} lost {bet} tokens")

st.markdown("---")

# --- Display Balances & Leaderboard ---
if st.session_state.balances:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Player Balances & Stats")
        for player in st.session_state.balances:
            balance = st.session_state.balances[player]
            wins = st.session_state.wins.get(player, 0)
            losses = st.session_state.losses.get(player, 0)
            last_roll = st.session_state.last_roll.get(player)
            roll_text = f" | Last Roll: {last_roll}" if last_roll is not None else ""
            st.markdown(f"**{player}**: Balance={balance} tokens | Wins={wins} | Losses={losses}{roll_text}")

    with col2:
        st.subheader("🏆 Leaderboard (Most Wins)")
        sorted_leaderboard = sorted(st.session_state.wins.items(), key=lambda x: x[1], reverse=True)
        for player, win_count in sorted_leaderboard:
            st.markdown(f"**{player}**: {win_count} wins 🏅")
