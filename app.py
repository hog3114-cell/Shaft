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
.bm-team { font-size:16.5px; font-weight:800; text-align:center;
    display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap:4px;
    padding:2px 0 8px; }
.bm-team, .bm-team:not(.bm-num) { color:#0B1B33 !important; }
.bm-badge-uo { background:#E3F4E8; color:#1E8449 !important; padding:2px 9px; border-radius:6px; font-size:11px; font-weight:800; margin-left:7px; }
.bm-badge-h  { background:#FCEEDB; color:#C9700A !important; padding:2px 9px; border-radius:6px; font-size:11px; font-weight:800; margin-left:7px; }
.bm-badge-ev { background:#E8EAF6; color:#3F51B5 !important; padding:2px 9px; border-radius:6px; font-size:11px; font-weight:800; margin-left:7px; }

/* ── ⭐ betman식 선택 버튼 (누르면 네이비로 칠해짐) ── */
div.row-widget.stRadio > div { flex-direction:row; gap:10px; padding-bottom:10px; flex-wrap:wrap; }
div.row-widget.stRadio label {
    background:#F4F6F9 !important;
    border:2px solid #E0E5EC !important;
    border-radius:12px !important;
    padding:16px 6px !important;
    flex:1 1 70px; min-width:70px;
    display:flex !important; align-items:center; justify-content:center;
    transition:all .15s ease;
    cursor:pointer;
}
div.row-widget.stRadio label p {
    color:#5A6678 !important; font-weight:800 !important; font-size:16px;
}
/* 동그란 라디오 점 완전 제거 */
div.row-widget.stRadio label > div:first-child,
div.row-widget.stRadio label [data-testid="stMarkdownContainer"] + div,
div.row-widget.stRadio input { display:none !important; width:0 !important; }
/* 선택된 버튼: 네이비 채움 + 흰 글씨 */
div.row-widget.stRadio label:has(input:checked) {
    background:#13284A !important;
    border-color:#13284A !important;
    box-shadow:0 4px 14px rgba(19,40,74,0.28);
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

/* ── 관리자 순위 카드 ── */
.rank-card {
    display:flex; align-items:center; gap:14px;
    background:#FFFFFF; border:1px solid #E6E9EF; border-radius:14px;
    padding:14px 18px; margin-bottom:11px;
    box-shadow:0 2px 10px rgba(11,27,51,0.05);
}
.rank-card.top1 { background:linear-gradient(120deg,#FFF8E7,#FFFFFF); border:1.5px solid #F5C451; }
.rank-medal { font-size:26px; min-width:34px; text-align:center; }
.rank-name { font-size:17px; font-weight:800; color:#0B1B33 !important; flex:1; }
.rank-score { font-size:15px; font-weight:800; color:#1B3A6B !important;
    background:#EAF0F8; padding:5px 12px; border-radius:20px; }

/* 섹션 소제목 가운데 정렬 */
.center-title { text-align:center; font-size:18px; font-weight:900;
    color:#0B1B33 !important; margin:8px 0 16px; }
.center-sub { text-align:center; font-size:13px; color:#5A6678 !important; margin-bottom:18px; }
/* selectbox 라벨 또렷하게 */
[data-testid="stWidgetLabel"] p { font-weight:700 !important; color:#0B1B33 !important; }
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

# 경기 팀 정보 (여기만 바꾸면 전체 반영)
TEAM_HOME = "대한민국"
TEAM_AWAY = "남아프리카공화국"
MATCH = f"{TEAM_HOME} vs {TEAM_AWAY}"

# 최종 스코어 선택지 (몇 대 몇 맞히기)
SCORE_OPTIONS = ["0:0", "1:0", "2:0", "2:1", "3:0", "3:1",
                 "0:1", "0:2", "1:2", "0:3", "1:3", "기타"]

QUESTION_MAP = {
    "q1": "1. 최종 승무패", "q3": "2. 핸디캡(-1.0)",
    "q4": "3. 첫 골 득점 국가", "q5": "4. 전반전 결과", "q6": "5. 대한민국 총 득점",
    "q7": "6. 양 팀 모두 득점", "q8": "7. 첫 옐로카드", "q9": "8. PK 발생", "q10": "9. 최종 스코어"
}

# 문항별 선택지 (관리자 정답 입력 & 채점에 사용)
OPTIONS_MAP = {
    "q1": ["승", "무", "패"], "q3": ["승", "무", "패"],
    "q4": ["한국", "상대팀", "무득점"], "q5": ["승", "무", "패"], "q6": ["0골", "1골", "2골+"],
    "q7": ["Yes", "No"], "q8": ["한국", "상대팀", "없음"], "q9": ["Yes", "No"], "q10": SCORE_OPTIONS
}

TOTAL_Q = len(QUESTION_MAP)  # 총 문항 수 (채점 표기에 사용)

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

            # 승부식 2종 (승무패 / 핸디캡)
            fixed = [
                (1, MATCH, "<span class='bm-badge-uo'>승무패</span>", ["승", "무", "패"], "q1"),
                (2, MATCH, "<span class='bm-badge-h'>핸디캡 -1.0</span>", ["승", "무", "패"], "q3"),
            ]
            for num, team, badge, opts, key in fixed:
                st.markdown(f"""<div class="bm-card"><div class="bm-card-head">
                    <span>⚽ 월드컵 축구</span><span>경기 {num}</span></div>
                    <div class="bm-team"><span class="bm-num">{num}</span>{team}{badge}</div></div>""",
                    unsafe_allow_html=True)
                picks[key] = st.radio(key, opts, horizontal=True, label_visibility="collapsed", key=key)

            # 이벤트 퀴즈 6종 (q4~q9) → 화면번호 3~8
            events = [
                ("q4", "첫 골 득점 국가", ["한국", "상대팀", "무득점"]),
                ("q5", "전반전 결과", ["승", "무", "패"]),
                ("q6", "대한민국 총 득점", ["0골", "1골", "2골+"]),
                ("q7", "양 팀 모두 득점", ["Yes", "No"]),
                ("q8", "첫 옐로카드", ["한국", "상대팀", "없음"]),
                ("q9", "페널티킥 발생", ["Yes", "No"]),
            ]
            for num, (key, title, opts) in enumerate(events, start=3):
                st.markdown(f"""<div class="bm-card"><div class="bm-card-head">
                    <span>🎯 이벤트 퀴즈</span><span>경기 {num}</span></div>
                    <div class="bm-team"><span class="bm-num">{num}</span>{title}
                    <span class='bm-badge-ev'>EVENT</span></div></div>""",
                    unsafe_allow_html=True)
                picks[key] = st.radio(key, opts, horizontal=True,
                                      label_visibility="collapsed", key=key)

            # q10: 최종 스코어 맞히기 (몇 대 몇) → 화면번호 9
            st.markdown(f"""<div class="bm-card"><div class="bm-card-head">
                <span>🏁 최종 스코어</span><span>경기 9</span></div>
                <div class="bm-team"><span class="bm-num">9</span>{MATCH}
                <span class='bm-badge-h'>SCORE</span></div></div>""",
                unsafe_allow_html=True)
            picks["q10"] = st.radio("q10", SCORE_OPTIONS, horizontal=True,
                                    label_visibility="collapsed", key="q10")

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
    st.markdown('<div class="center-title">🧾 내 토토 영수증</div>', unsafe_allow_html=True)
    search = st.text_input("조회할 이름", key="search", placeholder="이름을 입력하세요")
    if search:
        df = load_data()
        if not df.empty and search in df["name"].values:
            row = df[df["name"] == search].iloc[-1]
            st.markdown(f'<div class="center-sub"><b>{search}</b>님의 마킹 내역</div>',
                        unsafe_allow_html=True)
            rows_html = ""
            for q, label in QUESTION_MAP.items():
                if q in row and pd.notna(row[q]):
                    rows_html += f"""<div style="display:flex;justify-content:space-between;
                        padding:11px 4px;border-bottom:1px solid #F0F2F5;">
                        <span style="color:#5A6678;font-weight:600;">{label}</span>
                        <span style="color:#0B1B33;font-weight:800;">{row[q]}</span></div>"""
            st.markdown(f"""<div class="bm-card" style="padding:8px 18px;">{rows_html}</div>""",
                        unsafe_allow_html=True)
            if not is_locked:
                st.info("💡 수정하려면 '마킹하기'에서 같은 이름으로 다시 제출하세요.")
        else:
            st.error("등록된 내역이 없습니다. 이름을 확인하세요.")

# ============================================================
# 탭 3: 관리자 (정답 입력 → 자동 채점 → 순위)
# ============================================================
with tab_admin:
    st.markdown('<div class="center-title">👑 관리자 채점 룸</div>', unsafe_allow_html=True)

    df = load_data()
    st.markdown(f'<div class="center-sub">현재 참여자 <b>{len(df)}명</b> · 경기 종료 후 정답을 입력하세요</div>',
                unsafe_allow_html=True)

    # --- 정답 입력 ---
    st.markdown('<div class="center-title" style="font-size:15px;">🎯 정답 입력</div>', unsafe_allow_html=True)
    answers = {}
    for q, label in QUESTION_MAP.items():
        answers[q] = st.selectbox(label, OPTIONS_MAP[q], key=f"ans_{q}")

    st.write("")
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

            st.balloons()
            st.markdown('<div class="center-title">🏅 최종 순위</div>', unsafe_allow_html=True)

            medals = ["🥇", "🥈", "🥉"]
            for i, r in rank_df.iterrows():
                medal = medals[i] if i < 3 else f"{i+1}"
                top = "top1" if i == 0 else ""
                st.markdown(f"""<div class="rank-card {top}">
                    <span class="rank-medal">{medal}</span>
                    <span class="rank-name">{r['이름']}</span>
                    <span class="rank-score">{r['맞은 개수']} / {TOTAL_Q}</span></div>""",
                    unsafe_allow_html=True)
