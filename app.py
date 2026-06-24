import streamlit as st
import datetime

# --- [1] 모바일 최적화 및 프로토 UI 완벽 복제 CSS ---
st.set_page_config(layout="centered", page_title="2026 사내 승부식", page_icon="⚽")
st.markdown("""
    <style>
    /* 전체 배경을 프로토 사이트처럼 옅은 회색으로 */
    .stApp { background-color: #F4F5F7; }
    
    /* 프로토 상단 헤더 스타일 */
    .proto-header { background-color: white; padding: 15px; border-bottom: 1px solid #ddd; font-weight: bold; font-size: 18px; display: flex; justify-content: space-between; }
    
    /* 조합 / 한경기 탭 스타일 (사진과 동일하게 남색/흰색) */
    .proto-tabs { display: flex; text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 10px; border-bottom: 1px solid #0F4C81; }
    .tab-active { background-color: #0F4C81; color: white; padding: 10px; width: 50%; }
    .tab-inactive { background-color: white; color: #555; padding: 10px; width: 50%; border-top: 1px solid #ddd; border-right: 1px solid #ddd; }
    
    /* 개별 경기 카드 스타일 */
    .match-card { background-color: white; border: 1px solid #ddd; margin-bottom: -1px; padding: 12px; }
    .match-title { font-size: 12px; color: #666; margin-bottom: 8px; display: flex; justify-content: space-between; }
    .match-content { font-size: 15px; font-weight: bold; display: flex; align-items: center; justify-content: space-between; }
    
    /* U/O, 핸디캡 배지 스타일 */
    .badge-uo { background-color: #E8F5E9; color: #2E7D32; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-left: 5px; }
    .badge-h { background-color: #FFF3E0; color: #E65100; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-left: 5px; }
    
    /* 입력창 및 라디오 버튼 커스텀 */
    div[role="radiogroup"] { flex-direction: row; justify-content: flex-end; gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 2026년 마감 시간 세팅 ---
DEADLINE = datetime.datetime(2026, 6, 25, 9, 50, 0) # 2026년 6월 25일 목요일 09:50
now = datetime.datetime.now()
is_locked = now > DEADLINE

# 임시 데이터베이스
if 'users_data' not in st.session_state: st.session_state.users_data = {}

# --- [3] 화면 상단 UI (사진 완벽 재현) ---
st.markdown('<div class="proto-header">프로토 승부식 74회차 <span style="color:#aaa; cursor:pointer;">🗑️</span></div>', unsafe_allow_html=True)
st.markdown('<div class="proto-tabs"><div class="tab-active">조합</div><div class="tab-inactive">한경기</div></div>', unsafe_allow_html=True)

# 시스템 모드 선택 (스트림릿 기본 탭 사용)
tab_main, tab_edit, tab_admin = st.tabs(["📝 마킹하기", "🔍 마이페이지", "👑 관리자 채점"])

with tab_main:
    if is_locked:
        st.error("🚨 제출이 마감되었습니다. (결과 발표 대기 중)")
    else:
        st.warning("⏳ 제출 마감: 목요일 오전 09:50 (마감 전까지 수정 가능)")
        user_name = st.text_input("👤 참여자 이름 (예: 민웅프로)", placeholder="이름을 입력해야 마킹이 시작됩니다.")
        
        if user_name:
            picks = {}
            
            # [1경기] 일반 승무패 (사진 복제)
            st.markdown('<div class="match-card"><div class="match-title"><span>⚽ 축월드컵 축구 승무패</span><span>✕</span></div><div class="match-content"><span>3431 대한민국</span></div></div>', unsafe_allow_html=True)
            picks['q1'] = st.radio("1", ["승", "무", "패"], label_visibility="collapsed", key="q1")
            
            # [2경기] 언더오버 (사진 속 초록색 U/O 배지 복제)
            st.markdown('<div class="match-card"><div class="match-title"><span>⚽ 축월드컵 축구 언더오버</span><span>✕</span></div><div class="match-content"><span>3442 대한민국 <span class="badge-uo">U/O 2.5</span></span></div></div>', unsafe_allow_html=True)
            picks['q2'] = st.radio("2", ["언더", "오버"], label_visibility="collapsed", key="q2")
            
            # [3경기] 핸디캡 (사진 속 주황색 H 배지 복제)
            st.markdown('<div class="match-card"><div class="match-title"><span>⚽ 축월드컵 축구 핸디캡</span><span>✕</span></div><div class="match-content"><span>3458 대한민국 <span class="badge-h">H -1.0</span></span></div></div>', unsafe_allow_html=True)
            picks['q3'] = st.radio("3", ["승", "무", "패"], label_visibility="collapsed", key="q3")
            
            # [4~10경기] (간략화 표기, 실제 사용 시 위 양식을 복사하여 10번까지 늘리면 됩니다)
            for i in range(4, 11):
                st.markdown(f'<div class="match-card"><div class="match-title"><span>⚽ 축월드컵 이벤트 퀴즈</span><span>✕</span></div><div class="match-content"><span>350{i} 특별항목 {i}번</span></div></div>', unsafe_allow_html=True)
                picks[f'q{i}'] = st.radio(str(i), ["1번 옵션", "2번 옵션"], label_visibility="collapsed", key=f"q{i}")
            
            st.write("---")
            if st.button("✅ 최종 조합 구매(제출)하기", type="primary", use_container_width=True):
                st.session_state.users_data[user_name] = picks
                st.success("제출 완료! 마이페이지 탭에서 확인 및 수정하세요.")

with tab_edit:
    st.markdown("### 🔍 내 마킹 확인 및 수정")
    search_name = st.text_input("조회할 이름을 입력하세요", key="search")
    if search_name in st.session_state.users_data:
        st.json(st.session_state.users_data[search_name])
        if not is_locked:
            st.info("💡 수정하려면 '마킹하기' 탭에서 다시 제출하시면 덮어쓰기 됩니다.")

with tab_admin:
    st.markdown("### 👑 관리자 정답 입력")
    admin_pw = st.text_input("비밀번호", type="password")
    if admin_pw == "1234":
        st.success("인증 완료")
        st.write("실제 결과를 입력하면 1,2,3등이 자동 산출됩니다.")
        ans_1 = st.radio("1경기 정답", ["승", "무", "패"])
        if st.button("🏆 결과 채점 및 발표"):
            st.balloons()
            st.metric("🥇 1등 예측", "현재 데이터베이스 연동 필요")