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

# 🎴 카드 풀 (총 30명)
card_pool = [
    # 일반 선수 (특수 능력 없음)
    PlayerCard("김태연", 4, 8),
    PlayerCard("이진영", 6, 6),
    PlayerCard("김인환", 5, 4,),
    PlayerCard("박상원", 7, 6),
    PlayerCard("한승혁", 4, 5),
    PlayerCard("임종찬", 6, 6),
    PlayerCard("김범수", 5, 7),
    PlayerCard("이원석", 8, 7),
    PlayerCard("장민재", 5, 7),
    PlayerCard("주현상", 6, 6),
    PlayerCard("윤산흠", 5, 7),

    # 특수 능력 선수 (12명)
    PlayerCard("리베라토", 8, 7, special="double_atk"),
    PlayerCard("최재훈", 5, 9, special="one_hit_win"),
    PlayerCard("정우람", 6, 8, special="shield"),
    PlayerCard("문동주", 7, 6, special="reflect",),
    PlayerCard("심우준", 6, 8, special="disarm"),
    PlayerCard("류현진", 8, 9, special="disarm"),
    PlayerCard("김서현", 7, 6, special="drain"),
    PlayerCard("노시환", 9, 5, special="drain"),
    PlayerCard("정은원", 7, 8, special="quick_defense"),
    PlayerCard("채은성", 6, 9, special="versatile_power"),
    PlayerCard("하주석", 5, 6, special="pierce_defense"),
    PlayerCard("폰세", 7, 6, special="double_atk"),

    # 전설 카드
    PlayerCard("장종훈", 9, 7, special="legendary_power"),
    PlayerCard("김태균", 8, 8, special="legendary_power"),
    PlayerCard("송진우", 6, 10, special="legendary_power"),
    PlayerCard("정민철", 7, 8, special="legendary_power"),
    PlayerCard("구대성", 8, 9, special="legendary_power"),
    PlayerCard("박찬호", 10, 9, special="legendary_power"),
]

# 🔄 게임 초기화
def reset_game():
    cards = card_pool.copy()
    random.shuffle(cards)
    st.session_state.user_cards = cards[:15]
    st.session_state.com_cards = cards[15:30]
    st.session_state.com_used = set()
    st.session_state.user_score = 0
    st.session_state.com_score = 0
    st.session_state.round = 1
    st.session_state.game_over = False

    # 전설 카드에 '전설의 힘' 효과 적용
    for card in st.session_state.user_cards + st.session_state.com_cards:
        if card.special == "legendary_power":
            card.atk += 3
            card.def_ += 3

# 🧠 컴퓨터 카드 선택
def computer_choose_card(com_cards, user_card):
    unused = [card for card in com_cards if card.name not in st.session_state.com_used]
    if not unused:
        return com_cards[0]

    if user_card.def_ > user_card.atk:
        chosen = max(unused, key=lambda c: c.atk)
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
            msg = f"✨ **{card.name}**의 특수능력 발동! 공격력이 2배로 증가!"
        elif card.special == "one_hit_win":
            msg = f"💥 **{card.name}**의 특수능력 발동! 이번 라운드는 무조건 승리!"
        elif card.special == "shield":
            msg = f"🛡️ **{card.name}**의 특수능력 발동! 이번 공격을 방어합니다!"
        elif card.special == "reflect":
            msg = f"↩️ **{card.name}**의 특수능력 발동! 상대의 공격을 반사합니다!"
        elif card.special == "revive":
            msg = f"💖 **{card.name}**의 특수능력 발동! 패배해도 한 번 부활할 수 있습니다!"
        elif card.special == "disarm":
            msg = f"⚔️ **{card.name}**의 특수능력 발동! 상대방의 공격력을 절반으로 만듭니다!"
        elif card.special == "drain":
            msg = f"🩸 **{card.name}**의 특수능력 발동! 상대방의 공격력을 흡수합니다!"
        elif card.special == "quick_defense":
            msg = f"💨 **{card.name}**의 특수능력 발동! 수비력이 폭발적으로 증가합니다!"
        elif card.special == "pierce_defense":
            msg = f"🔪 **{card.name}**의 특수능력 발동! 상대방의 수비력을 관통합니다!"
        elif card.special == "versatile_power":
            msg = f"🌀 **{card.name}**의 특수능력 발동! 공격력과 수비력 중 하나가 강화됩니다!"
    return msg

# 🚩 초기 실행
if 'user_cards' not in st.session_state:
    reset_game()

# 🎮 UI 구성
st.title("⚾ 한화 이글스 카드 배틀 - 특수 능력 & 레벨업 모드")

st.markdown("---")
st.subheader("🔮 특수 능력 설명")
st.info("""
- **double_atk**: 공격력이 2배로 증가합니다.
- **one_hit_win**: 해당 라운드에서 무조건 승리합니다. (단, 상대방도 같은 능력이면 무승부)
- **shield**: 상대방의 공격을 방어하고, 내 공격력으로 승리 여부를 결정합니다.
- **reflect**: 상대방의 공격을 반사하여 승리합니다.
- **revive**: 한 번 패배해도 부활하여 살아남습니다.
- **disarm**: 상대방의 공격력을 일시적으로 절반으로 만듭니다.
- **drain**: 상대방의 공격력 일부를 흡수하여 내 공격력에 더합니다.
- **quick_defense**: 이번 라운드 수비력이 5 증가합니다.
- **pierce_defense**: 상대방 수비력 3을 무시하고 공격합니다.
- **versatile_power**: 공격력과 수비력 중 하나가 무작위로 5 증가합니다.
- **legendary_power**: 게임 시작 시 공격력과 수비력이 영구적으로 +3 증가합니다.
""")
st.markdown("---")

# 📋 새로운 선수별 특수 능력 목록 추가
with st.expander("📝 **선수별 특수 능력 목록 보기**"):
    special_info = {
        "리베라토": "double_atk (공격력 2배)",
        "폰세": "double_atk (공격력 2배)",
        "최재훈": "one_hit_win (무조건 승리)",
        "정우람": "shield (공격 방어)",
        "문동주": "reflect (공격 반사)",
        "심우준": "disarm (무장 해제)",
        "류현진": "disarm (무장 해제)",
        "김서현": "drain (흡수)",
        "노시환": "drain (흡수)",
        "정은원": "quick_defense (신속한 수비)",
        "채은성": "versatile_power (다재다능한 힘)",
        "하주석": "pierce_defense (방어 관통)",
        "장종훈": "legendary_power (전설의 힘)",
        "김태균": "legendary_power (전설의 힘)",
        "송진우": "legendary_power (전설의 힘)",
        "정민철": "legendary_power (전설의 힘)",
        "구대성": "legendary_power (전설의 힘)",
        "박찬호": "legendary_power (전설의 힘)",
    }
    for name, effect in special_info.items():
        st.write(f"- **{name}**: {effect}")

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

def format_card_with_special(i):
    card = st.session_state.user_cards[i]
    special_names = {
        "double_atk": "공격력 2배",
        "one_hit_win": "무조건 승리",
        "shield": "공격 방어",
        "reflect": "공격 반사",
        "revive": "한 번 부활",
        "disarm": "무장 해제",
        "drain": "흡수",
        "quick_defense": "신속한 수비",
        "pierce_defense": "방어 관통",
        "versatile_power": "다재다능한 힘",
        "legendary_power": "전설의 힘"
    }
    special_info = special_names.get(card.special, "")
    return f"{str(card)} ({special_info})" if special_info else str(card)

try:
    choice = st.selectbox("사용할 카드를 선택하세요:", range(len(st.session_state.user_cards)),
                          format_func=format_card_with_special)
except ValueError:
    st.error("사용할 수 있는 카드가 없습니다. 게임을 초기화해주세요.")
    st.stop()

if st.button("⚔️ 대결 시작"):
    user_card = st.session_state.user_cards[choice]
    com_card = computer_choose_card(st.session_state.com_cards, user_card)

    st.write(f"👤 **당신 카드**: {user_card.name}")
    st.write(f"💻 **컴퓨터 카드**: {com_card.name}")

    user_msg = apply_special(user_card, com_card)
    if user_msg: st.info(user_msg)

    com_msg = apply_special(com_card, user_card)
    if com_msg: st.info(com_msg)

    # 대결 로직
    result = None
    
    # 임시 변수 설정
    user_temp_atk = user_card.atk
    user_temp_def = user_card.def_
    com_temp_atk = com_card.atk
    com_temp_def = com_card.def_

    # 특수 능력에 따른 공격력/수비력 변화
    if user_card.special == "double_atk" and not user_card.used_special:
        user_temp_atk *= 2
        user_card.used_special = True
    if com_card.special == "double_atk" and not com_card.used_special:
        com_temp_atk *= 2
        com_card.used_special = True
        
    if user_card.special == "disarm" and not user_card.used_special:
        com_temp_atk = com_temp_atk // 2
        user_card.used_special = True
    if com_card.special == "disarm" and not com_card.used_special:
        user_temp_atk = user_temp_atk // 2
        com_card.used_special = True
        
    if user_card.special == "drain" and not user_card.used_special:
        drained_atk = com_card.atk // 2
        user_temp_atk += drained_atk
        com_temp_atk -= drained_atk
        user_card.used_special = True
    if com_card.special == "drain" and not com_card.used_special:
        drained_atk = user_card.atk // 2
        com_temp_atk += drained_atk
        user_temp_atk -= drained_atk
        com_card.used_special = True

    if user_card.special == "quick_defense" and not user_card.used_special:
        user_temp_def += 5
        user_card.used_special = True
    if com_card.special == "quick_defense" and not com_card.used_special:
        com_temp_def += 5
        com_card.used_special = True

    if user_card.special == "versatile_power" and not user_card.used_special:
        if random.choice([True, False]):
            st.write(f"**{user_card.name}**의 공격력이 강화됩니다!")
            user_temp_atk += 5
        else:
            st.write(f"**{user_card.name}**의 수비력이 강화됩니다!")
            user_temp_def += 5
        user_card.used_special = True
    if com_card.special == "versatile_power" and not com_card.used_special:
        if random.choice([True, False]):
            st.write(f"**{com_card.name}**의 공격력이 강화됩니다!")
            com_temp_atk += 5
        else:
            st.write(f"**{com_card.name}**의 수비력이 강화됩니다!")
            com_temp_def += 5
        com_card.used_special = True

    # one_hit_win, reflect, shield 능력 우선 처리
    if user_card.special == "one_hit_win" and not user_card.used_special:
        if com_card.special == "one_hit_win" and not com_card.used_special:
            result = 'draw'
        else:
            result = 'user'
            user_card.used_special = True
    elif com_card.special == "one_hit_win" and not com_card.used_special:
        result = 'com'
        com_card.used_special = True
    
    elif user_card.special == "reflect" and not user_card.used_special:
        result = 'user'
        user_card.used_special = True
    elif com_card.special == "reflect" and not com_card.used_special:
        result = 'com'
        com_card.used_special = True

    elif user_card.special == "shield" and not user_card.used_special:
        user_card.used_special = True
        if user_temp_atk > com_temp_def:
            result = 'user'
        else:
            result = 'draw'
    elif com_card.special == "shield" and not com_card.used_special:
        com_card.used_special = True
        if com_temp_atk > user_temp_def:
            result = 'com'
        else:
            result = 'draw'

    # 일반 대결 (공격력-수비력 차이로 승패 결정)
    else:
        # pierce_defense 능력은 여기에서 최종 공격력을 계산
        if user_card.special == "pierce_defense" and not user_card.used_special:
            com_temp_def = max(0, com_temp_def - 3) # 최소 0
            user_card.used_special = True
        if com_card.special == "pierce_defense" and not com_card.used_special:
            user_temp_def = max(0, user_temp_def - 3) # 최소 0
            com_card.used_special = True

        user_score = user_temp_atk - com_temp_def
        com_score = com_temp_atk - user_temp_def

        st.markdown(f"**대결 분석:**")
        st.write(f"- 당신의 공격력 ({user_temp_atk}) vs 컴퓨터의 수비력 ({com_temp_def}): **차이 {user_score}**")
        st.write(f"- 컴퓨터의 공격력 ({com_temp_atk}) vs 당신의 수비력 ({user_temp_def}): **차이 {com_score}**")

        if user_score > com_score:
            result = 'user'
        elif com_score > user_score:
            result = 'com'
        else:
            result = 'draw'

    # 결과 처리
    if result == 'user':
        st.success("🎉 당신이 이겼습니다!")
        # 승리 보너스 기능 추가
        if random.choice([True, False]):
            user_card.atk += 1
            st.write(f"🔥 **{user_card.name}**의 공격력이 1 상승했습니다!")
        else:
            user_card.def_ += 1
            st.write(f"🛡️ **{user_card.name}**의 수비력이 1 상승했습니다!")

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
```
