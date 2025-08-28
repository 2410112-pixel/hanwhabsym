import random
import streamlit as st

class PlayerCard:
    def __init__(self, name, atk, def_, special=None):
        self.name = name
        self.base_atk = atk
        self.base_def = def_
        self.atk = atk
        self.def_ = def_
        self.exp = 0  # 경험치
        self.level = 1
        self.special = special  # 특수 능력 문자열

    def level_up(self):
        # 경험치가 3 넘으면 레벨업, 공격/수비 +1, 경험치 초기화
        if self.exp >= 3:
            self.level += 1
            self.atk += 1
            self.def_ += 1
            self.exp = 0
            return True
        return False

    def __str__(self):
        spc = f" | 특수능력: {self.special}" if self.special else ""
        return f"{self.name} Lv.{self.level} (공격력: {self.atk} / 수비력: {self.def_}){spc}"

# 특수 능력 예시
# 'double_atk': 공격력 2배 한 번 사용 가능
# 'one_hit_win': 한 번 무조건 이김 (패배 시 1회 사용)
special_cards = {
    "리베라토": "double_atk",
    "최재훈": "one_hit_win"
}

card_pool = [
    PlayerCard("노시환", 8, 7),
    PlayerCard("채은성", 7, 8),
    PlayerCard("하주석", 6, 6),
    PlayerCard("문현빈", 7, 5),
    PlayerCard("김태연", 5, 7),
    PlayerCard("이진영", 6, 8),
    PlayerCard("김인환", 4, 5),
    PlayerCard("최재훈", 5, 9, special="one_hit_win"),
    PlayerCard("리베라토", 7, 8, special="double_atk"),
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
    candidates = [card for card in com_cards if card.def_ >= user_card.atk]
    if candidates:
        chosen = max(candidates, key=lambda c: c.atk)
    else:
        chosen = max(com_cards, key=lambda c: c.atk)
    return chosen

def apply_special(card, opponent_card, is_user):
    # 특수능력 적용 (사용 후 능력 제거)
    msg = ""
    if card.special == "double_atk":
        card.atk *= 2
        msg = f"{card.name}의 특수능력! 공격력이 2배가 되었습니다!"
        card.special = None  # 한 번 사용 후 사라짐
    elif card.special == "one_hit_win":
        # 상대 공격력 무시하고 무조건 이김 한 번 가능
        # 게임 결과 처리에서 별도로 반영
        msg = f"{card.name}의 특수능력! 이번 라운드 무조건 승리합니다!"
        card.special = None
    return msg

if 'user_cards' not in st.session_state or 'game_over' not in st.session_state:
    reset_game()

st.title("🟠 한화 이글스 카드 배틀 - 특수능력 + 레벨업 모드")

if st.button("게임 초기화"):
    reset_game()

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

        # 특수능력 먼저 적용 (사용 메시지 출력)
        user_msg = apply_special(user_card, com_card, True)
        if user_msg:
            st.write(user_msg)
        com_msg = apply_special(com_card, user_card, False)
        if com_msg:
            st.write(com_msg)

        # 무조건 승리 특수능력 처리
        user_forced_win = (user_card.special is None and "one_hit_win" in [user_card.special, None]) and user_msg and "무조건 승리" in user_msg
        com_forced_win = (com_card.special is None and "one_hit_win" in [com_card.special, None]) and com_msg and "무조건 승리" in com_msg

        # 이긴 선수 판단
        if user_msg and "무조건 승리" in user_msg:
            user_wins = True
            com_wins = False
        elif com_msg and "무조건 승리" in com_msg:
            user_wins = False
            com_wins = True
        else:
            user_wins = user_card.atk > com_card.def_
            com_wins = com_card.atk > user_card.def_

        if user_wins and not com_wins:
            st.write("🎉 당신 선수 승리!")
            st.session_state.com_cards.remove(com_card)
            st.session_state.user_score += 1
            user_card.exp += 1
            if user_card.level_up():
                st.write(f"⬆️ {user_card.name} 레벨업! 공격력과 수비력이 1씩 증가했습니다!")
        elif com_wins and not user_wins:
            st.write("💻 컴퓨터 선수 승리!")
            st.session_state.user_cards.remove(user_card)
            st.session_state.com_score += 1
            com_card.exp += 1
            if com_card.level_up():
                st.write(f"⬆️ {com_card.name} 레벨업! 공격력과 수비력이 1씩 증가했습니다!")
        elif user_wins and com_wins:
            st.write("⚔️ 양 선수 모두 공격 성공! 무승부 처리 (둘 다 살아있음)")
        else:
            st.write("🤝 양 선수 모두 공격 실패! 무승부 처리 (둘 다 살아있음)")

        st.write(f"📊 현재 점수 => 당신: {st.session_state.user_score} | 컴퓨터: {st.session_state.com_score}")

        # 특수능력 사용 후 공격력 복구 (double_atk는 한 번만 사용되고 소멸되니 걱정 없음)
        user_card.atk = user_card.base_atk + (user_card.level - 1)
        com_card.atk = com_card.base_atk + (com_card.level - 1)

        st.session_state.round += 1

        if len(st.session_state.user_cards) == 0 or len(st.session_state.com_cards) == 0:
            st.session_state.game_over = True

