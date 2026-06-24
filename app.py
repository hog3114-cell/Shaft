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
# [1] 토토 스타일 CSS (betman식 선택 버튼 + 모던 색감)
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap');

/* ── 기본 토대 ── */
.stApp { background:#F0F2F5 !important; }
.stApp, .stApp * { font-family:'Pretendard','Apple SD Gothic Neo',sans-serif; }
.block-container { padding-top:3rem !important; padding-bottom:2rem; max-width:460px; }
header[data-testid="stHeader"] { background:transparent !important; height:0; }

/* 기본 글자 또렷하게 강제 */
.stApp p, .stApp label, .stApp span, .stApp div,
.stMarkdown, [data-testid="stWidgetLabel"] p { color:#0B1B33 !important; }
.stTextInput input { color:#0B1B33 !important; background:#FFFFFF !important;
    border:1.5px solid #D5DBE3 !important; border-radius:10px !important; font-weight:600; }
.stTextInput input::placeholder { color:#9AA4B2 !important; }

/* ── 헤더 (딥네이비 + 골드 포인트) ── */
.bm-header {
    background:linear-gradient(120deg,#0B1B33 0%,#13284A 60%,#1B3A6B 100%);
    padding:20px 22px 18px; border-radius:16px 16px 0 0;
    display:flex; align-items:center; gap:10px;
    box-shadow:0 6px 18px rgba(11,27,51,0.28);
}
.bm-header *, .bm-header { color:#FFFFFF !important; }
.bm-logo { font-size:22px; }
.bm-title { font-weight:900; font-size:19px; letter-spacing:-0.5px; }
.bm-round { background:#F5C451; color:#0B1B33 !important; font-size:12px;
    font-weight:800; padding:3px 9px; border-radius:20px; margin-left:auto; }

.bm-subbar {
    background:#FFFFFF; padding:11px 18px; border-radius:0 0 16px 16px;
    font-size:12.5px; border:1px solid #E6E9EF; border-top:none;
    margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;
}
.bm-subbar *, .bm-subbar { color:#5A6678 !important; font-weight:600; }
.bm-deadline { color:#D64545 !important; font-weight:800; }

/* ── 경기 카드 ── */
.bm-card {
    background:#FFFFFF; border:1px solid #E6E9EF; border-radius:14px;
    padding:15px 17px 6px; margin-bottom:13px;
    box-shadow:0 2px 10px rgba(11,27,51,0.05);
}
.bm-card-head {
    display:flex; justify-content:space-between; align-items:center;
    font-size:11.5px; margin-bottom:10px;
    border-bottom:1px solid #F0F2F5; padding-bottom:8px;
}
.bm-card-head *, .bm-card-head { color:#9AA4B2 !important; font-weight:700; }
.bm-num { background:#0B1B33 !important; color:#FFFFFF !important;
    padding:2px 8px; border-radius:5px; font-size:11px; margin-right:7px; font-weight:800; }
.bm-team { font-size:16.5px; font-weight:800; }
.bm-team, .bm-team:not(.bm-num) { color:#0B1B33 !important; }
.bm-badge-uo { background:#E3F4E8; color:#1E8449 !important; padding:2px 9px; border-radius:6px; font-size:11px; font-weight:800; margin-left:7px; }
.bm-badge-h  { background:#FCEEDB; color:#C9700A !important; padding:2px 9px; border-radius:6px; font-size:11px; font-weight:800; margin-left:7px; }
.bm-badge-ev { background:#E8EAF6; color:#3F51B5 !important; padding:2px 9px; border-radius:6px; font-size:11px; font-weight:800; margin-left:7px; }

/* ── ⭐ betman식 선택 버튼 (누르면 네이비로 칠해짐) ── */
div.row-widget.stRadio > div { flex-direction:row; gap:9px; padding-bottom:9px; }
div.row-widget.stRadio label {
    background:#F4F6F9 !important;
    border:1.5px solid #E0E5EC !important;
    border-radius:10px !important;
    padding:11px 4px !important;
    flex:1; justify-content:center;
    transition:all .15s ease;
    cursor:pointer;
}
div.row-widget.stRadio label p {
    color:#5A6678 !important; font-weight:800 !important; font-size:14.5px;
}
/* 기본 동그란 라디오 점 숨기기 */
div.row-widget.stRadio label > div:first-child { display:none !important; }
/* 선택된 버튼: 네이비 채움 + 흰 글씨 (:has 지원 브라우저) */
div.row-widget.stRadio label:has(input:checked) {
    background:#13284A !important;
    border-color:#13284A !important;
    box-shadow:0 4px 12px rgba(19,40,74,0.25);
}
div.row-widget.stRadio label:has(input:checked) p {
    color:#FFFFFF !important;
}

/* ── 제출 버튼 ── */
.stButton button[kind="primary"] {
    background:linear-gradient(120deg,#0B1B33,#1B3A6B) !important;
    border:none !important; font-weight:900 !important; border-radius:12px !important;
    height:54px !important; font-size:16px !important;
    box-shadow:0 6px 16px rgba(11,27,51,0.3) !important;
}
.stButton button[kind="primary"] p { color:#FFFFFF !important; }
.stButton button[kind="primary"]:hover { filter:brightness(1.12); }

/* 탭 스타일 살짝 정리 */
button[data-baseweb="tab"] { font-weight:700 !important; }
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

# 문항별 선택지 (관리자 정답 입력 & 채점에 사용)
OPTIONS_MAP = {
    "q1": ["승", "무", "패"], "q2": ["언더", "오버"], "q3": ["승", "무", "패"],
    "q4": ["한국", "상대팀", "무득점"], "q5": ["승", "무", "패"], "q6": ["0골", "1골", "2골+"],
    "q7": ["Yes", "No"], "q8": ["한국", "상대팀", "없음"], "q9": ["Yes", "No"], "q10": ["홀수", "짝수"]
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
st.markdown('<div class="bm-header"><span class="bm-logo">🏆</span><span class="bm-title">기계의장부 스포츠 토토</span><span class="bm-round">1회차</span></div>', unsafe_allow_html=True)
st.markdown('<div class="bm-subbar"><span>⚽ 이벤트 승부식</span><span class="bm-deadline">마감 6/25(목) 09:50</span></div>', unsafe_allow_html=True)

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
# 탭 3: 관리자 (정답 입력 → 자동 채점 → 순위)
# ============================================================
with tab_admin:
    st.markdown("### 👑 관리자 채점 룸")
    pw = st.text_input("관리자 암호", type="password")

    if pw == st.secrets.get("admin_pw", "1234"):
        st.success("✅ 인증 완료")
        df = load_data()
        st.metric("총 참여자 수", f"{len(df)}명")

        # --- 제출 현황(엑셀 그대로 보기) ---
        with st.expander("📋 제출 현황 전체 보기 (구글 시트 원본)", expanded=False):
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("아직 제출된 픽이 없습니다.")

        # --- 정답 입력 ---
        st.markdown("#### 🎯 정답 입력 (경기 종료 후)")
        answers = {}
        for q, label in QUESTION_MAP.items():
            answers[q] = st.selectbox(label, OPTIONS_MAP[q], key=f"ans_{q}")

        # --- 자동 채점 ---
        if st.button("🏆 자동 채점 및 순위 발표", type="primary", use_container_width=True):
            if df.empty:
                st.warning("채점할 제출 내역이 없습니다.")
            else:
                results = []
                for _, row in df.iterrows():
                    score = sum(1 for q in QUESTION_MAP
                                if q in row and str(row[q]) == answers[q])
                    results.append({"이름": row["name"], "맞은 개수": score})

                rank_df = pd.DataFrame(results).sort_values(
                    "맞은 개수", ascending=False).reset_index(drop=True)
                rank_df.index = rank_df.index + 1  # 1등부터
                rank_df.index.name = "순위"

                st.balloons()
                st.markdown("#### 🥇 최종 순위")

                # 1~3등 강조
                medals = ["🥇", "🥈", "🥉"]
                for i, (_, r) in enumerate(rank_df.head(3).iterrows()):
                    st.metric(f"{medals[i]} {i+1}등 · {r['이름']}",
                              f"{r['맞은 개수']} / 10개 정답")

                st.markdown("#### 📊 전체 순위표")
                st.dataframe(rank_df, use_container_width=True)
    elif pw:
        st.error("암호가 틀렸습니다.")
