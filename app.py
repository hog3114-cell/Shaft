import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ============================================================
# 기계의장부 스포츠 토토 (betman 스타일 / 라이트 테마 강제)
# 데이터 영구 저장: Google Sheets 연동
# ============================================================

st.set_page_config(layout="centered", page_title="기계의장부 스포츠 토토", page_icon="⚽")

# ------------------------------------------------------------
# [1] betman 스타일 CSS (라이트 테마 전제 → 색상 충돌 없음)
# ------------------------------------------------------------
st.markdown("""
<style>
/* 전체 배경: betman 옅은 회색 */
.stApp { background-color: #EFF1F4; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 480px; }

/* 상단 남색 헤더 (betman 톤) */
.bm-header {
    background: linear-gradient(135deg, #0F4C81 0%, #1565A8 100%);
    color: #FFFFFF; padding: 18px 20px; border-radius: 12px 12px 0 0;
    font-weight: 800; font-size: 19px; display:flex; align-items:center; gap:8px;
    box-shadow: 0 2px 8px rgba(15,76,129,0.25);
}
.bm-subbar {
    background:#FFFFFF; padding:10px 16px; border-radius:0 0 12px 12px;
    font-size:13px; color:#555; border:1px solid #E3E6EA; border-top:none;
    margin-bottom:16px; display:flex; justify-content:space-between;
}
.bm-round { color:#0F4C81; font-weight:700; }

/* 경기 카드 */
.bm-card {
    background:#FFFFFF; border:1px solid #E3E6EA; border-radius:10px;
    padding:14px 16px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.04);
}
.bm-card-head {
    display:flex; justify-content:space-between; align-items:center;
    font-size:12px; color:#8A93A0; font-weight:600; margin-bottom:8px;
    border-bottom:1px dashed #EEE; padding-bottom:6px;
}
.bm-num { background:#0F4C81; color:#FFF; padding:2px 7px; border-radius:4px; font-size:11px; margin-right:6px; }
.bm-team { font-size:16px; font-weight:800; color:#1A1A1A; }
.bm-badge-uo { background:#E8F5E9; color:#2E7D32; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; margin-left:6px; }
.bm-badge-h  { background:#FFF3E0; color:#E65100; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; margin-left:6px; }
.bm-badge-ev { background:#EDE7F6; color:#5E35B1; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; margin-left:6px; }

/* 라디오 버튼: betman 선택지처럼 가로 정렬 */
div.row-widget.stRadio > div { flex-direction:row; gap:8px; }
div.row-widget.stRadio label {
    background:#F4F5F7; border:1px solid #DDE1E6; border-radius:6px;
    padding:6px 4px; flex:1; justify-content:center; font-weight:600;
}

/* 제출 버튼 */
.stButton button[kind="primary"] {
    background:#0F4C81; border:none; font-weight:800; border-radius:8px; height:50px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# [2] 마감 시간 & 구글 시트 연결
# ------------------------------------------------------------
DEADLINE = datetime.datetime(2026, 6, 25, 9, 50, 0)
now = datetime.datetime.now()
is_locked = now > DEADLINE

# 구글 시트 연결 (secrets.toml 필요 - 아래 설명 참고)
conn = st.connection("gsheets", type=GSheetsConnection)

QUESTION_MAP = {
    "q1": "1. 축구 최종 승무패", "q2": "2. 언더오버(2.5)", "q3": "3. 핸디캡(-1.0)",
    "q4": "4. 첫 골 득점 국가", "q5": "5. 전반전 결과", "q6": "6. 대한민국 총 득점",
    "q7": "7. 양 팀 모두 득점", "q8": "8. 첫 옐로카드", "q9": "9. PK 발생", "q10": "10. 최종스코어 홀짝"
}

def load_data():
    """시트 전체를 DataFrame으로 읽기 (캐시 0초로 항상 최신)"""
    try:
        df = conn.read(worksheet="picks", ttl=0)
        return df.dropna(how="all")
    except Exception:
        # 시트가 비었거나 첫 실행일 때 빈 틀 반환
        return pd.DataFrame(columns=["name"] + list(QUESTION_MAP.keys()) + ["updated_at"])

def save_pick(name, picks):
    """이름 기준 upsert: 있으면 갱신, 없으면 추가"""
    df = load_data()
    row = {"name": name, **picks, "updated_at": now.strftime("%Y-%m-%d %H:%M:%S")}
    if not df.empty and name in df["name"].values:
        df = df[df["name"] != name]  # 기존 행 제거 후 재삽입(수정)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    conn.update(worksheet="picks", data=df)

# ------------------------------------------------------------
# [3] 상단 헤더
# ------------------------------------------------------------
st.markdown('<div class="bm-header">🏆 기계의장부 스포츠 토토 <span class="bm-round">1회차</span></div>', unsafe_allow_html=True)
st.markdown(f'<div class="bm-subbar"><span>이벤트 승부식</span><span>마감: 6/25(목) 09:50</span></div>', unsafe_allow_html=True)

tab_main, tab_my, tab_admin = st.tabs(["📝 마킹하기", "🧾 마이페이지", "👑 관리자"])

# ============================================================
# 탭 1: 마킹하기
# ============================================================
with tab_main:
    if is_locked:
        st.error("🚨 제출이 마감되었습니다. (결과 발표 대기 중)")
    else:
        st.info("⏳ 마감 전까지 무제한 수정 가능 (이름 동일하게 재제출)")
        user_name = st.text_input("👤 참여자 이름", placeholder="이름을 입력하면 마킹 용지가 열립니다")

        if user_name:
            picks = {}

            # 승부식 3종 (승무패 / 언더오버 / 핸디캡)
            fixed = [
                ("3431", "대한민국", "", ["승", "무", "패"], "q1"),
                ("3442", "대한민국", "<span class='bm-badge-uo'>U/O 2.5</span>", ["언더", "오버"], "q2"),
                ("3458", "대한민국", "<span class='bm-badge-h'>H -1.0</span>", ["승", "무", "패"], "q3"),
            ]
            for code, team, badge, opts, key in fixed:
                st.markdown(f"""<div class="bm-card"><div class="bm-card-head">
                    <span>⚽ 월드컵 축구</span><span>✕</span></div>
                    <div class="bm-team"><span class="bm-num">{code}</span>{team}{badge}</div></div>""",
                    unsafe_allow_html=True)
                picks[key] = st.radio(key, opts, horizontal=True, label_visibility="collapsed", key=key)

            # 이벤트 퀴즈 7종
            events = [
                ("첫 골 득점 국가", ["한국", "상대팀", "무득점"]),
                ("전반전 결과", ["승", "무", "패"]),
                ("대한민국 총 득점", ["0골", "1골", "2골+"]),
                ("양 팀 모두 득점", ["Yes", "No"]),
                ("첫 옐로카드", ["한국", "상대팀", "없음"]),
                ("페널티킥 발생", ["Yes", "No"]),
                ("최종스코어 홀짝", ["홀수", "짝수"]),
            ]
            for idx, (title, opts) in enumerate(events, start=4):
                st.markdown(f"""<div class="bm-card"><div class="bm-card-head">
                    <span>🎯 이벤트 퀴즈</span><span>✕</span></div>
                    <div class="bm-team"><span class="bm-num">350{idx}</span>{title}
                    <span class='bm-badge-ev'>EVENT</span></div></div>""",
                    unsafe_allow_html=True)
                picks[f"q{idx}"] = st.radio(f"q{idx}", opts, horizontal=True,
                                            label_visibility="collapsed", key=f"q{idx}")

            st.write("")
            if st.button("✅ 최종 조합 구매 (픽 제출)", type="primary", use_container_width=True):
                try:
                    save_pick(user_name, picks)
                    st.success(f"{user_name}님 픽이 구글 시트에 저장되었습니다! 마이페이지에서 확인하세요.")
                except Exception as e:
                    st.error(f"저장 실패: 시트 연결을 확인하세요. ({e})")

# ============================================================
# 탭 2: 마이페이지
# ============================================================
with tab_my:
    st.markdown("### 🧾 내 토토 영수증")
    search = st.text_input("조회할 이름", key="search")
    if search:
        df = load_data()
        if not df.empty and search in df["name"].values:
            row = df[df["name"] == search].iloc[-1]
            st.success(f"**{search}**님의 마킹 내역")
            for q, label in QUESTION_MAP.items():
                if q in row and pd.notna(row[q]):
                    st.markdown(f"- **{label}** → `{row[q]}`")
            if not is_locked:
                st.warning("💡 수정: '마킹하기'에서 같은 이름으로 재제출")
        else:
            st.error("등록된 내역이 없습니다. 이름을 확인하세요.")

# ============================================================
# 탭 3: 관리자
# ============================================================
with tab_admin:
    st.markdown("### 👑 관리자 채점 룸")
    pw = st.text_input("관리자 암호", type="password")
    if pw == st.secrets.get("admin_pw", "1234"):
        st.success("✅ 인증 완료")
        df = load_data()
        st.metric("총 참여자 수", f"{len(df)}명")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        if st.button("🏆 채점 및 순위 발표", use_container_width=True):
            st.balloons()
            st.info("정답 세팅 로직은 경기 종료 후 연결 예정")
    elif pw:
        st.error("암호가 틀렸습니다.")
