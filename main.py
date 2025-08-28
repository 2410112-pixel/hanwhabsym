import random
import streamlit as st

# 🃏 카드 클래스 정의
class PlayerCard:
    """게임에 사용되는 선수 카드를 나타내는 클래스"""
    def __init__(self, name, atk, def_, special=None):
        self.name = name
        self.base_atk = atk
        self.base_def = def_
        self.atk = atk
        self.def_ = def_
        self.exp = 0
        self.level = 1
        self.special = special
        self.used_special = False
        self.revive_used = False

    def level_up(self):
        if self.exp >= 3:
            self.level += 1
            self.atk += 1
            self.def_ += 1
            self.exp = 0
            return True
        return False

    def __str__(self):
        spc = f" | 특수: {self.special}" if self.special else ""
        return f"({self.name}) Lv.{self.level} (공: {self.atk} / 수: {self.def_}){spc}"

# 🎴 카드 풀
card_pool = [
    PlayerCard("노시환", 9, 5,),
    PlayerCard("채은성", 6, 9),
    PlayerCard("하주석", 5, 6),
    PlayerCard("문현빈", 7, 5),
    PlayerCard("김태연", 4, 8),
    PlayerCard("이진영", 6, 6),
    PlayerCard("김인환", 5, 4,),
    PlayerCard("폰세", 7, 6),
    PlayerCard("류현진", 8, 9),
    PlayerCard("김서현", 6, 7),
    PlayerCard("박상원", 7, 6),
    PlayerCard("한승혁", 4, 5),

    # 특수 카드
    PlayerCard("리베라토", 8, 7, special="double_atk"),
    PlayerCard("최재훈", 5, 9, special="one_hit_win"),
    PlayerCard("정우람", 6, 8, special="shield"),
    PlayerCard("문동주", 7, 6, special="reflect",),
    PlayerCard("장민재", 5, 7, special="revive",),
    PlayerCard("주현상", 6, 6, special="shield"),

    # 전설 카드
    PlayerCard("장종훈", 9, 7),
    PlayerCard("김태균", 8, 8),
    PlayerCard("송진우", 6, 10),
    PlayerCard("정민철", 7, 8),
    PlayerCard("구대성", 8, 9),
    PlayerCard("박찬호", 10, 9),
]

# 🔄 게임 초기화
def reset_game():
    cards = card_pool.copy()
    random.shuffle(cards)
    st.session_state.user_cards = cards[:13]
    st.session_state.com_cards = cards[13:26]
    st.session_state.com_used = set()
    st.session_state.user_score = 0
    st.session_state.com_score = 0
    st.session_state.round = 1
    st.session_state.game_over = False

# 🧠 컴퓨터 카드 선택
def computer_choose_card(com_cards, user_card):
    unused = [card for card in com_cards if card.name not in st.session_state.com_used]
    if not unused:
        return com_cards[0]

    # 플레이어 카드 방어력이 높으면 공격력이 높은 카드 선택
    if user_card.def_ > user_card.atk:
        chosen = max(unused, key=lambda c: c.atk)
    # 플레이어 카드 공격력이 높으면 수비력이 높은 카드 선택
    else:
        candidates = [c for c in unused if c.def_ >= user_card.atk]
        chosen = max(candidates, key=lambda c: c.def_) if candidates else max(unused, key=lambda c: c.atk)

    st.session_state.com_used.add(chosen.name)
    return chosen

# 🪄 특수 능력 처리
def apply_special(card, opponent_card):
    msg = ""
    if card.special and not card.used_special:
        if card.special == "double_atk":
            card.atk *= 2
            msg = f"✨ **{card.name}**의 특수능력 발동! 공격력이 2배로 증가!"
            card.used_special = True
        elif card.special == "one_hit_win":
            msg = f"💥 **{card.name}**의 특수능력 발동! 이번 라운드는 무조건 승리!"
            card.used_special = True
        elif card.special == "shield":
            msg = f"🛡️ **{card.name}**의 특수능력 발동! 이번 공격을 방어합니다!"
        elif card.special == "reflect":
            msg = f"↩️ **{card.name}**의 특수능력 발동! 상대의 공격을 반사합니다!"
        elif card.special == "revive":
            msg = f"💖 **{card.name}**의 특수능력 발동! 패배해도 한 번 부활할 수 있습니다!"
    return msg

# 🚩 초기 실행
if 'user_cards' not in st.session_state:
    reset_game()

# 🎮 UI 구성
st.title("⚾ 한화 이글스 카드 배틀 - 특수 능력 & 레벨업 모드")

# ---
# 특수 능력 설명 추가
st.markdown("---")
st.subheader("🔮 특수 능력 설명")
st.info("""
- **double_atk**: 공격력이 2배로 증가합니다.
- **one_hit_win**: 해당 라운드에서 무조건 승리합니다. (단, 상대방도 같은 능력이면 무승부)
- **shield**: 상대방의 공격을 방어합니다.
- **reflect**: 상대방의 공격을 반사하여 승리합니다.
- **revive**: 한 번 패배해도 부활하여 살아남습니다.
""")
st.markdown("---")

if st.button("🔄 게임 초기화"):
    reset_game()

if st.session_state.game_over:
    if len(st.session_state.user_cards) == 0:
        st.error("💻 컴퓨터 승리! 당신의 모든 선수가 패배했습니다.")
    elif len(st.session_state.com_cards) == 0:
        st.success("🎉 당신 승리! 컴퓨터의 모든 선수가 패배했습니다.")
    st.stop()

st.subheader(f"라운드 {st.session_state.round}")

st.markdown(f"👤 **내 카드 ({len(st.session_state.user_cards)}명)**")
for idx, card in enumerate(st.session_state.user_cards):
    st.write(f"{idx + 1}. {card}")

# 특수 능력 설명이 포함된 카드 선택 상자
def format_card_with_special(i):
    card = st.session_state.user_cards[i]
    if card.special == "double_atk":
        return f"{card} (공격력 2배)"
    elif card.special == "one_hit_win":
        return f"{card} (무조건 승리)"
    elif card.special == "shield":
        return f"{card} (공격 방어)"
    elif card.special == "reflect":
        return f"{card} (공격 반사)"
    elif card.special == "revive":
        return f"{card} (한 번 부활)"
    else:
        return str(card)

try:
    choice = st.selectbox("사용할 카드를 선택하세요:", range(len(st.session_state.user_cards)),
                          format_func=format_card_with_special)
except ValueError:
    st.error("사용할 수 있는 카드가 없습니다. 게임을 초기화해주세요.")
    st.stop()

if st.button("⚔️ 대결 시작"):
    user_card = st.session_state.user_cards[choice]
    com_card = computer_choose_card(st.session_state.com_cards, user_card)

    st.write(f"👤 당신: {user_card.name}")
    st.write(f"💻 컴퓨터: {com_card.name}")

    user_msg = apply_special(user_card, com_card)
    if user_msg: st.info(user_msg)

    com_msg = apply_special(com_card, user_card)
    if com_msg: st.info(com_msg)

    # 특수 능력 우선 처리
    result = None
    if user_card.special == "one_hit_win" and not user_card.used_special:
        result = 'user'
    elif com_card.special == "one_hit_win" and not com_card.used_special:
        result = 'com'
    elif user_card.special == "reflect" and not user_card.used_special:
        result = 'user'
    elif com_card.special == "reflect" and not com_card.used_special:
        result = 'com'
    elif user_card.special == "shield" and not user_card.used_special:
        result = 'draw' # 내 실드로 무효화
    elif com_card.special == "shield" and not com_card.used_special:
        result = 'draw' # 상대 실드로 무효화
    else:
        # 일반 대결: 공격력-수비력 차이로 승패 결정
        user_score = user_card.atk - com_card.def_
        com_score = com_card.atk - user_card.def_

        if user_score > com_score:
            result = 'user'
        elif com_score > user_score:
            result = 'com'
        else:
            result = 'draw'

    # 결과 처리
    if result == 'user':
        st.success("🎉 당신이 이겼습니다!")
        if com_card.special == "revive" and not com_card.revive_used:
            st.warning(f"💖 **{com_card.name}**이 부활했습니다!")
            com_card.revive_used = True
        else:
            st.session_state.com_cards.remove(com_card)
        user_card.exp += 1
        if user_card.level_up():
            st.balloons()
            st.write(f"⬆️ **{user_card.name}**이 레벨업했습니다!")
    elif result == 'com':
        st.error("💻 컴퓨터가 승리했습니다!")
        if user_card.special == "revive" and not user_card.revive_used:
            st.warning(f"💖 **{user_card.name}**이 부활했습니다!")
            user_card.revive_used = True
        else:
            st.session_state.user_cards.remove(user_card)
        com_card.exp += 1
        if com_card.level_up():
            st.write(f"💻 **{com_card.name}**이 레벨업했습니다!")
    else:
        st.info("🤝 무승부입니다! 두 카드 모두 살아남습니다!")

    st.session_state.round += 1

    if not st.session_state.user_cards or not st.session_state.com_cards:
        st.session_state.game_over = True
