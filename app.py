import streamlit as st
import datetime
import pandas as pd # 마이페이지 표(Table) 출력을 위해 pandas 라이브러리 추가

# --- [1] 모바일 최적화 및 프로토 UI 완벽 복제 CSS (다크모드 충돌 해결) ---
st.set_page_config(layout="centered", page_title="기계의장부 스포츠 토토", page_icon="⚽")

# 다크모드/라이트모드 충돌을 막기 위해 글자색(color)을 강제 고정(!important)합니다.
st.markdown("""
    <style>
    /* 전체 배경을 프로토 사이트처럼 옅은 회색으로 */
    .stApp { background-color: #F4F5F7; }
    
    /* 탭 상단 남색 디자인 (글자색 진한 회색으로 강제 고정) */
    .proto-header { background-color: white !important; color: #333333 !important; padding: 15px; border-bottom: 2px solid #0F4C81; font-weight: 900; font-size: 20px; display: flex; justify-content: space-between; margin-bottom: 10px; border-radius: 8px 8px 0 0; }
    .proto-tabs { display: flex; text-align: center; font-weight: bold; font-size: 15px; margin-bottom: 20px; }
    .tab-active { background-color: #0F4C81 !important; color: white !important; padding: 12px; width: 50%; border-radius: 5px 0 0 5px; }
    .tab-inactive { background-color: white !important; color: #555555 !important; padding: 12px; width: 50%; border: 1px solid #ddd; border-left: none; border-radius: 0 5px 5px 0; }
    
    /* 카드 내부 글자색 강제 고정 (다크모드에서 흰 글씨 안 보이게) */
    .match-card-title { font-size: 13px; color: #666666 !important; margin-bottom: 8px; font-weight: bold; }
    .match-card-content { font-size: 16px; font-weight: 900; color: #111111 !important; padding-top: 5px; }
    
    /* U/O, 핸디캡 배지 스타일 */
    .badge-uo { background-color: #E8F5E9 !important; color: #2E7D32 !important; padding: 3px 8px; border-radius: 4px; font-size: 12px; margin-left: 8px; font-weight: bold; }
    .badge-h { background-color: #FFF3E0 !important; color: #E65100 !important; padding: 3px 8px; border-radius: 4px; font-size: 12px; margin-left: 8px; font-weight: bold; }
    
    /* 라디오 버튼 가로 정렬 */
    div.row-widget.stRadio > div { flex-direction: row; justify-content: flex-end; gap: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 2026년 마감 시간 세팅 ---
DEADLINE = datetime.datetime(2026, 6, 25, 9, 50, 0) # 2026년 6월 25일 목요일 09:50
now = datetime.datetime.now()
is_locked = now > DEADLINE

# 임시 데이터베이스 (추후 구글 시트로 변경 예정)
if 'users_data' not in st.session_state: st.session_state.users_data = {}

# 문항 맵핑용 딕셔너리 (마이페이지에서 예쁘게 보여주기 위함)
QUESTION_MAP = {
    "q1": "1. 축구 최종 승무패", "q2": "2. 언더오버 (2.5 기준)", "q3": "3. 핸디캡 (-1.0 적용)",
    "q4": "4. 첫 골 득점 국가", "q5": "5. 전반전 결과 예측", "q6": "6. 대한민국 총 득점 수",
    "q7": "7. 양 팀 모두 득점 여부", "q8": "8. 첫 옐로카드 국가", "q9": "9. 페널티킥(PK) 발생", "q10": "10. 최종 스코어 홀/짝"
}

# --- [3] 화면 상단 UI (기계의장부 맞춤 타이틀 적용) ---
st.markdown('<div class="proto-header">🏆 기계의장부 스포츠 토토 1회 <span style="color:#aaa; cursor:pointer;">🗑️</span></div>', unsafe_allow_html=True)
st.markdown('<div class="proto-tabs"><div class="tab-active">조합 구매</div><div class="tab-inactive">한경기 구매</div></div>', unsafe_allow_html=True)

# 시스템 모드 선택 탭
tab_main, tab_edit, tab_admin = st.tabs(["📝 마킹하기", "🧾 마이페이지", "👑 관리자 채점"])

with tab_main:
    if is_locked:
        st.error("🚨 제출이 마감되었습니다. (결과 발표 대기 중)")
    else:
        st.info("⏳ 제출 마감: 목요일 오전 09:50 (마감 전까지 무제한 수정 가능)")
        user_name = st.text_input("👤 참여자 이름 (예: 김민웅)", placeholder="이름을 입력해야 마킹 용지가 열립니다.")
        
        if user_name:
            picks = {}
            st.write("---")
            
            # [1경기] 승무패
            with st.container(border=True):
                st.markdown("<div class='match-card-title'>⚽ 축월드컵 축구 승무패 <span style='float:right; color:#ccc;'>✕</span></div>", unsafe_allow_html=True)
                col1, col2 = st.columns([1.2, 1.8])
                with col1: st.markdown("<div class='match-card-content'>3431 대한민국</div>", unsafe_allow_html=True)
                with col2: picks['q1'] = st.radio("1", ["승", "무", "패"], horizontal=True, label_visibility="collapsed", key="q1")
            
            # [2경기] 언더오버
            with st.container(border=True):
                st.markdown("<div class='match-card-title'>⚽ 축월드컵 축구 언더오버 <span style='float:right; color:#ccc;'>✕</span></div>", unsafe_allow_html=True)
                col1, col2 = st.columns([1.2, 1.8])
                with col1: st.markdown("<div class='match-card-content'>3442 대한민국 <span class='badge-uo'>U/O 2.5</span></div>", unsafe_allow_html=True)
                with col2: picks['q2'] = st.radio("2", ["언더", "오버"], horizontal=True, label_visibility="collapsed", key="q2")
                    
            # [3경기] 핸디캡
            with st.container(border=True):
                st.markdown("<div class='match-card-title'>⚽ 축월드컵 축구 핸디캡 <span style='float:right; color:#ccc;'>✕</span></div>", unsafe_allow_html=True)
                col1, col2 = st.columns([1.2, 1.8])
                with col1: st.markdown("<div class='match-card-content'>3458 대한민국 <span class='badge-h'>H -1.0</span></div>", unsafe_allow_html=True)
                with col2: picks['q3'] = st.radio("3", ["승", "무", "패"], horizontal=True, label_visibility="collapsed", key="q3")

            # [4~10경기] 이벤트 퀴즈
            questions = [
                ("첫 골 득점 국가", ["한국", "상대팀", "무득점"]),
                ("전반전 결과", ["승", "무", "패"]),
                ("대한민국 총 득점 수", ["0골", "1골", "2골이상"]),
                ("양 팀 모두 득점 여부", ["Yes", "No"]),
                ("첫 옐로카드 국가", ["한국", "상대팀", "없음"]),
                ("페널티킥(PK) 발생", ["Yes", "No"]),
                ("최종 스코어 홀/짝", ["홀수", "짝수"])
            ]
            
            for idx, (q_title, options) in enumerate(questions, start=4):
                with st.container(border=True):
                    st.markdown(f"<div class='match-card-title'>⚽ 축월드컵 이벤트 퀴즈 <span style='float:right; color:#ccc;'>✕</span></div>", unsafe_allow_html=True)
                    col1, col2 = st.columns([1.2, 1.8])
                    with col1: st.markdown(f"<div class='match-card-content'>350{idx} {q_title}</div>", unsafe_allow_html=True)
                    with col2: picks[f'q{idx}'] = st.radio(str(idx), options, horizontal=True, label_visibility="collapsed", key=f"q{idx}")
            
            st.write("---")
            if st.button("✅ 최종 조합 구매 (픽 제출하기)", type="primary", use_container_width=True):
                st.session_state.users_data[user_name] = picks
                st.success(f"{user_name}님의 픽이 정상적으로 등록되었습니다! 마이페이지를 확인하세요.")

# ==========================================
# 탭 2: 마이페이지 (UI 전면 개편 - 표 형태)
# ==========================================
with tab_edit:
    st.markdown("### 🧾 내 토토 영수증 확인")
    search_name = st.text_input("조회할 이름을 입력하세요 (예: 김민웅)", key="search")
    
    if search_name in st.session_state.users_data:
        st.success(f"**{search_name}**님의 마킹 내역입니다.")
        user_picks = st.session_state.users_data[search_name]
        
        # 보기 싫은 JSON 대신 깔끔한 표(데이터프레임)로 변환하여 출력
        display_data = []
        for q_key, answer in user_picks.items():
            display_data.append({"경기 항목": QUESTION_MAP[q_key], "나의 픽": answer})
            
        df = pd.DataFrame(display_data)
        st.table(df) # 표 형태로 예쁘게 출력
        
        if not is_locked:
            st.warning("💡 수정하려면 '마킹하기' 탭에서 이름을 똑같이 적고 다시 제출하시면 됩니다.")
    elif search_name:
        st.error("등록된 마킹 내역이 없습니다. 이름을 다시 확인해 주세요.")

# ==========================================
# 탭 3: 관리자 페이지 (UI 복구)
# ==========================================
with tab_admin:
    st.markdown("### 👑 관리자 전용 채점 룸")
    # 다크모드에서도 잘 보이도록 기본 컴포넌트 활용
    admin_pw = st.text_input("관리자 암호를 입력하세요", type="password", help="결과 채점용 암호입니다.")
    
    if admin_pw == "1234":
        st.success("✅ 인증 완료: 관리자 모드 활성화")
        st.info("실제 경기가 종료된 후 아래 정답을 세팅하고 채점 버튼을 누르세요.")
        
        # 관리자가 실제 결과 세팅
        ans_1 = st.selectbox("1경기 정답", ["승", "무", "패"])
        ans_2 = st.selectbox("2경기 정답", ["언더", "오버"])
        
        if st.button("🏆 전체 채점 및 순위 발표 (애니메이션 시작)", use_container_width=True):
            st.balloons()
            st.markdown("#### 🎁 임시 채점 결과 (DB 연동 시 활성화됨)")
            st.metric("🥇 1등 (가오픈)", "데이터베이스 연동 전입니다.")
