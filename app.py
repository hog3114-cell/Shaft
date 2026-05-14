import streamlit as st
import datetime

# --- [기본 설정] 브라우저 넓게 쓰기 & 디자인 ---
st.set_page_config(layout="wide", page_title="2026 올림픽 스코어보드", page_icon="🏆")

st.markdown("""
    <style>
    .main-title { font-size:60px !important; font-weight: 900; text-align: center; color: #FFD700; text-shadow: 2px 2px 4px #000000; margin-bottom: 10px; }
    .game-title { font-size:30px !important; text-align: center; color: #00FFFF; margin-bottom: 30px; background-color: #333333; padding: 10px; border-radius: 10px; }
    .team-name { font-size: 35px !important; font-weight: bold; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- [데이터 저장소 (Session State) 초기화] ---
if 'team1_score' not in st.session_state: st.session_state.team1_score = 0
if 'team2_score' not in st.session_state: st.session_state.team2_score = 0
if 'team1_name' not in st.session_state: st.session_state.team1_name = "1팀 (청팀)"
if 'team2_name' not in st.session_state: st.session_state.team2_name = "2팀 (백팀)"
if 'team1_img' not in st.session_state: st.session_state.team1_img = None
if 'team2_img' not in st.session_state: st.session_state.team2_img = None
if 'current_game' not in st.session_state: st.session_state.current_game = "대기 중..."
if 'log' not in st.session_state: st.session_state.log = []

# 점수 업데이트 함수 (애니메이션 포함)
def update_score(team, points, msg):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    if team == 1: st.session_state.team1_score += points
    else: st.session_state.team2_score += points
    
    st.session_state.log.insert(0, f"[{now}] {team}팀 {points}점 - {msg}")
    if points > 0: st.balloons() # 점수 획득 시 풍선 효과!

# ==========================================
# 🔐 [호스트/수정 모드] 사이드바 영역
# ==========================================
with st.sidebar:
    st.title("🔒 관리자 로그인")
    admin_pw = st.text_input("진행자 비밀번호 (숫자 1234)", type="password")
    
    if admin_pw == "1234": # 비밀번호 일치 시 관리자 패널 활성화
        st.success("인증 완료!")
        
        # 탭(Tab) 기능으로 '진행 모드'와 '수정 모드' 분리
        tab1, tab2 = st.tabs(["🎮 진행(Host) 모드", "⚙️ 설정(Edit) 모드"])
        
        # --- 🎮 진행 모드 탭 ---
        with tab1:
            st.session_state.current_game = st.selectbox(
                "현재 진행 종목",
                ("1. 신서유기 릴레이 인물 퀴즈", "2. 고요 속의 외침", "3. 99초 스탠바이 큐", "결승. 단체 줄다리기")
            )
            st.divider()
            st.write(f"**{st.session_state.team1_name} 컨트롤**")
            c1, c2 = st.columns(2)
            if c1.button("+10점", key="t1_p10"): update_score(1, 10, "득점")
            if c2.button("-10점", key="t1_m10"): update_score(1, -10, "감점")
            
            st.divider()
            st.write(f"**{st.session_state.team2_name} 컨트롤**")
            c3, c4 = st.columns(2)
            if c3.button("+10점", key="t2_p10"): update_score(2, 10, "득점")
            if c4.button("-10점", key="t2_m10"): update_score(2, -10, "감점")

        # --- ⚙️ 설정 수정 모드 탭 ---
        with tab2:
            st.write("💡 **팀 이름 및 사진 세팅**")
            # 1팀 설정
            st.session_state.team1_name = st.text_input("1팀 이름 변경", st.session_state.team1_name)
            img1 = st.file_uploader("1팀 사진/로고 업로드", type=['png', 'jpg', 'jpeg'], key="img1")
            if img1: st.session_state.team1_img = img1
                
            st.divider()
            # 2팀 설정
            st.session_state.team2_name = st.text_input("2팀 이름 변경", st.session_state.team2_name)
            img2 = st.file_uploader("2팀 사진/로고 업로드", type=['png', 'jpg', 'jpeg'], key="img2")
            if img2: st.session_state.team2_img = img2
            
            st.divider()
            if st.button("🚨 전체 점수 및 기록 초기화"):
                st.session_state.team1_score = 0
                st.session_state.team2_score = 0
                st.session_state.log = []
                st.rerun()

# ==========================================
# 🖥️ [게스트 모드] 메인 화면 영역 (모두가 보는 화면)
# ==========================================
st.markdown('<p class="main-title">🏆 2026 부서 화합 워크샵 🏆</p>', unsafe_allow_html=True)
st.markdown(f'<p class="game-title">진행 중인 종목 ▶ <b>{st.session_state.current_game}</b></p>', unsafe_allow_html=True)

# 1팀과 2팀 화면 분할
col1, space, col2 = st.columns([4, 1, 4]) # 가운데 띄어쓰기(space) 공간 확보

with col1:
    # 수정 모드에서 바꾼 팀 이름이 적용됨
    st.markdown(f'<p class="team-name" style="color:#60A5FA;">🟦 {st.session_state.team1_name}</p>', unsafe_allow_html=True)
    # 업로드한 사진이 있으면 화면에 띄우고, 없으면 기본 아이콘 표시
    if st.session_state.team1_img:
        st.image(st.session_state.team1_img, use_container_width=True)
    else:
        st.info("사진이 없습니다. (수정 모드에서 업로드)")
    # 점수판
    st.metric(label="Score", value=f"{st.session_state.team1_score} 점")

with col2:
    st.markdown(f'<p class="team-name" style="color:#F87171;">🟥 {st.session_state.team2_name}</p>', unsafe_allow_html=True)
    if st.session_state.team2_img:
        st.image(st.session_state.team2_img, use_container_width=True)
    else:
        st.info("사진이 없습니다. (수정 모드에서 업로드)")
    st.metric(label="Score", value=f"{st.session_state.team2_score} 점")

st.write("---")
# 로그 뷰어 (가장 최신 3개 기록만 표시)
st.subheader("📢 실시간 경기 로그")
if st.session_state.log:
    for log_msg in st.session_state.log[:3]:
        st.code(log_msg)
else:
    st.write("경기가 시작되지 않았습니다.")