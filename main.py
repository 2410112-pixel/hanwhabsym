import random
import streamlit as st

class PlayerCard:
    def __init__(self, name, atk, def_):
        self.name = name
        self.atk = atk
        self.def_ = def_

    def __str__(self):
        return f"{self.name} (공격력: {self.atk} / 수비력: {self.def_})"

# 선수 능력치 새로 세팅
card_pool = [
    PlayerCard("노시환", 8, 7),
    PlayerCard("채은성", 7, 8),
    PlayerCard("하주석", 6, 6),
    PlayerCard("문현빈", 7, 5),
    PlayerCard("김태연", 5, 7),
    PlayerCard("이진영", 6, 8),
    PlayerCard("김인환", 4, 5),
    PlayerCard("최재훈", 5, 9),
    PlayerCard("리베라토", 7, 8),
    PlayerCard("폰세", 6, 7),
    PlayerCard("류현진", 8, 9),
    PlayerCard("김서현", 6, 7),
    PlayerCard("박상원", 7, 8),
    PlayerCard("한승혁", 5, 6)
]

def reset_game():
    random.shuffle(card_pool)
    st.session_state.user_cards = card_pool[:7]
    st.session_state.com_cards = card_pool[7:14]
    st.session_state.user_score = 0
    st.session_state.com_score = 0
    st.session_state.round = 1
    st.session_state.game_over = False

def computer_choose_card(com_cards, user_card):
    # 컴퓨터 AI: 사용자 공격력 이상 수비력 카드 우선, 없으면 공격력 높은 카드 선택
    candidates = [card for card in com_cards if card.def_ >= user_card.atk]
    if candidates:
        chosen = max(candidates, key=lambda c: c.atk)
    else:
        chosen = max(com_cards, key=lambda c: c.atk)
    return chosen

if 'user_cards' not in st.session_state or 'game_over' not in st.session_state:
    reset_game()

st.title("🟠 한화 이글스 카드 배틀 - 생존자 모드")

if st.button("게임 초기화"):
    reset_game()
    st.experimental_rerun()

if st.session_state.game_over:
    if len(st.session_state.user_cards) == 0:
        st.write("💻 컴퓨터 승리! 당신의 모든 선수가 패배했습니다.")
    elif len(st.session_state.com_cards) == 0:
        st.write("🎉 당신 승리! 컴퓨터의 모든 선수가 패배했습니다.")
else:
    st.write(f"### 라운드 {st.session_state.round}")

    st.write(f"👤 당신 선수들 ({len(st.session_state.user_cards)}명 남음):")
    for idx, card in enumerate(st.session_state.user_cards):
        st.write(f"{idx + 1}. {card}")

    user_choice = st.selectbox(
        "사용할 선수를 선택하세요",
        options=range(len(st.session_state.user_cards)),
        format_func=lambda x: str(st.session_state.user_cards[x])
    )

    if st.button("대결!"):
        user_card = st.session_state.user_cards[user_choice]
        com_card = computer_choose_card(st.session_state.com_cards, user_card)

        st.write(f"👤 당신 선택: {user_card}")
        st.write(f"💻 컴퓨터 선택: {com_card}")

        user_wins = user_card.atk > com_card.def_
        com_wins = com_card.atk > user_card.def_

        if user_wins and not com_wins:
            st.write("🎉 당신 선수 승리!")
            st.session_state.com_cards.remove(com_card)
            st.session_state.user_score += 1
        elif com_wins and not user_wins:
            st.write("💻 컴퓨터 선수 승리!")
            st.session_state.user_cards.remove(user_card)
            st.session_state.com_score += 1
        elif user_wins and com_wins:
            st.write("⚔️ 양 선수 모두 공격 성공! 무승부 처리 (둘 다 살아있음)")
        else:
            st.write("🤝 양 선수 모두 공격 실패! 무승부 처리 (둘 다 살아있음)")

        st.write(f"📊 현재 점수 => 당신: {st.session_state.user_score} | 컴퓨터: {st.session_state.com_score}")

        st.session_state.round += 1

        # 게임 종료 조건 체크
        if len(st.session_state.user_cards) == 0 or len(st.session_state.com_cards) == 0:
            st.session_state.game_over = True

        st.experimental_rerun()
