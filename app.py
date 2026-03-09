import csv
import streamlit as st
import pandas as pd

# =====================================
# 0. 페이지 설정
# =====================================
st.set_page_config(
    page_title="수업 교체 가능 시간표",
    layout="wide",
)

# =====================================
# 1. 커스텀 CSS
# =====================================
CUSTOM_CSS = """
<style>
/* 전체 앱 배경 */
.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
}

/* 메인 영역 폭/여백 */
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* 제목/텍스트 */
h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 800;
    letter-spacing: -0.02em;
}

p, label, .stCaption, .stMarkdown, .stText {
    color: #475569;
}

/* 공통 카드 */
.custom-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 22px;
    padding: 20px 22px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    margin-bottom: 18px;
}

/* 상단 히어로 카드 */
.hero-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: white;
    border-radius: 26px;
    padding: 28px 30px;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 2rem;
    font-weight: 900;
    margin-bottom: 6px;
    color: white;
}

.hero-desc {
    font-size: 1rem;
    color: rgba(255,255,255,0.82);
    margin-bottom: 0;
}

/* 필터 카드 */
.filter-card {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(10px);
    border: 1px solid #dbeafe;
    border-radius: 24px;
    padding: 20px 22px 14px 22px;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.08);
    margin-bottom: 18px;
}

/* selectbox */
div[data-baseweb="select"] > div {
    min-height: 46px;
    border-radius: 14px !important;
    border: 1px solid #cbd5e1 !important;
    background: white !important;
}

/* 버튼 */
.stButton > button {
    height: 46px;
    border-radius: 14px;
    border: none;
    font-weight: 800;
    font-size: 15px;
    color: white;
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    box-shadow: 0 10px 22px rgba(37, 99, 235, 0.22);
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
    color: white;
}

/* metric 카드 */
[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 18px 18px;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.05);
}

/* metric 내부 */
[data-testid="metric-container"] label {
    color: #64748b !important;
    font-weight: 700 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 900 !important;
}

/* 데이터프레임 카드 느낌 */
[data-testid="stDataFrame"] {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 8px;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
}

/* 표 헤더 */
thead tr th {
    background-color: #eff6ff !important;
    color: #0f172a !important;
    font-weight: 800 !important;
    text-align: center !important;
}

/* 표 셀 */
tbody tr td {
    text-align: center !important;
    font-size: 14px !important;
}

/* 홀수 줄 배경 */
tbody tr:nth-child(odd) {
    background-color: #f8fafc !important;
}

/* 구분 텍스트 */
.section-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}

.section-caption {
    font-size: 0.92rem;
    color: #64748b;
    margin-bottom: 12px;
}

/* 조건 표시 카드 */
.condition-bar {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 14px 16px;
    margin-top: 6px;
    margin-bottom: 16px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
    font-size: 15px;
    color: #334155;
}

/* 배지 */
.badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    background: #dbeafe;
    color: #1d4ed8;
    font-size: 12px;
    font-weight: 800;
    margin-right: 8px;
}

/* 결과 카드 */
.result-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 16px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    margin-bottom: 14px;
    min-height: 130px;
}

.result-card-top {
    font-size: 12px;
    font-weight: 800;
    color: #64748b;
    margin-bottom: 10px;
}

.result-card-main {
    font-size: 20px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 8px;
}

.result-card-sub {
    font-size: 15px;
    color: #334155;
    font-weight: 600;
}

/* 안내 카드 */
.empty-state {
    background: white;
    border: 1px dashed #bfdbfe;
    border-radius: 22px;
    padding: 34px 26px;
    text-align: center;
    color: #475569;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.03);
}

/* expander */
.streamlit-expanderHeader {
    font-weight: 800;
    color: #0f172a;
}

/* 모바일 대응 */
@media (max-width: 900px) {
    .hero-title {
        font-size: 1.6rem;
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =====================================
# 2. 데이터 불러오기
# =====================================
@st.cache_data
def load_timetable(csv_filename: str):
    try:
        with open(csv_filename, mode="r", newline="", encoding="cp949") as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        st.error(f"{csv_filename} 파일을 찾을 수 없습니다.")
        return None, None

    name_list = [row[0] for row in data[1:]]
    return data, name_list


def find_exchange_slots(
    data,
    teacher_name: str,
    selected_date: str,
    selected_class: str,
):
    """
    기존 Tkinter conclude() 로직을 Streamlit용으로 옮긴 함수.
    교체 가능한 (요일, 상대 선생님, 교시) 리스트를 리턴.
    """
    if data is None:
        return []

    date_list = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    column = [row[0] for row in data]

    name_index = None
    for i in range(len(column)):
        if teacher_name == column[i]:
            name_index = i
            break

    if name_index is None:
        return []

    class_index_list = []
    for j in range(1, 36):
        if j < len(data[name_index]) and selected_class == data[name_index][j]:
            class_index_list.append(j)

    results = []

    for class_idx in class_index_list:
        class_num = class_idx

        if 1 <= class_num <= 7:
            date = date_list[0]
        elif 8 <= class_num <= 14:
            date = date_list[1]
        elif 15 <= class_num <= 21:
            date = date_list[2]
        elif 22 <= class_num <= 28:
            date = date_list[3]
        else:
            date = date_list[4]

        if selected_date != date:
            continue

        for k in range(len(date_list)):
            day_name = date_list[k]

            for i in range(1, len(column)):
                other_teacher = column[i]
                if other_teacher == teacher_name:
                    continue

                for m in range(7 * k + 1, 7 * k + 8):
                    if (
                        m >= len(data[i])
                        or class_idx >= len(data[i])
                        or class_idx >= len(data[name_index])
                    ):
                        continue

                    if data[i][m] == selected_class:
                        if data[i][class_idx] == "" and data[name_index][m] == "":
                            period = 7 if m % 7 == 0 else m % 7
                            results.append((day_name, other_teacher, period))

    return results


def make_teacher_summary(df_result: pd.DataFrame) -> pd.DataFrame:
    df_teacher = (
        df_result.groupby("상대 선생님")
        .apply(
            lambda g: ", ".join(
                f"{row['요일']} {row['교시']}교시"
                for _, row in g.sort_values(["요일", "교시"]).iterrows()
            )
        )
        .reset_index(name="가능한 시간")
        .sort_values("상대 선생님")
    )
    return df_teacher


def make_period_summary(df_result: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df_result.groupby("교시")["상대 선생님"]
        .apply(lambda s: ", ".join(sorted(set(s))))
        .reset_index()
        .sort_values("교시")
    )
    grouped.rename(columns={"상대 선생님": "교체 가능한 선생님들"}, inplace=True)
    return grouped


# =====================================
# 3. 메인 UI
# =====================================
def main():
    csv_filename = "기초시간표.csv"
    data, name_list = load_timetable(csv_filename)

    if data is None:
        st.stop()

    # -----------------------------
    # 상단 헤더
    # -----------------------------
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">📚 수업 교체 가능 시간 조회</div>
            <p class="hero-desc">
                시간표를 기반으로 교체 가능한 선생님과 교시를 빠르게 찾을 수 있는 대시보드입니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # 상단 필터 카드
    # -----------------------------
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title">🔎 조회 조건 선택</div>'
        '<div class="section-caption">사이드바 대신 상단에서 바로 조건을 고르고 결과를 한 화면에서 확인하세요.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns([2.2, 1.3, 1.5, 1.0])

    with col1:
        teacher_name = st.selectbox(
            "선생님",
            options=name_list,
            key="teacher_name",
        )

    with col2:
        selected_date = st.selectbox(
            "요일",
            options=["월요일", "화요일", "수요일", "목요일", "금요일"],
            key="selected_date",
        )

    with col3:
        selected_class = st.selectbox(
            "반",
            options=[
                "1학년1반", "1학년2반", "1학년3반", "1학년4반",
                "2학년1반", "2학년2반", "2학년3반", "2학년4반"
            ],
            key="selected_class",
        )

    with col4:
        st.write("")
        st.write("")
        search_button = st.button("조회하기", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # 검색 전 안내
    # -----------------------------
    if not search_button:
        st.markdown(
            """
            <div class="empty-state">
                <h3 style="margin-bottom:8px;">먼저 조회 조건을 선택해 주세요</h3>
                <p style="margin-bottom:0;">
                    상단에서 <b>선생님</b>, <b>요일</b>, <b>반</b>을 선택한 뒤
                    <b>조회하기</b> 버튼을 누르면 교체 가능한 시간이 대시보드 형태로 표시됩니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # -----------------------------
    # 검색 실행
    # -----------------------------
    results = find_exchange_slots(
        data=data,
        teacher_name=teacher_name,
        selected_date=selected_date,
        selected_class=selected_class,
    )

    st.markdown(
        f"""
        <div class="condition-bar">
            <span class="badge">조회 조건</span>
            <b>{teacher_name}</b> · {selected_date} · {selected_class}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not results:
        st.warning("❌ 교체 가능한 시간이 없습니다.")
        return

    df_result = pd.DataFrame(results, columns=["요일", "상대 선생님", "교시"])
    weekday_order = ["월요일", "화요일", "수요일", "목요일", "금요일"]

    df_result["요일"] = pd.Categorical(
        df_result["요일"],
        categories=weekday_order,
        ordered=True
    )

    df_result = df_result.sort_values(["요일", "교시", "상대 선생님"]).reset_index(drop=True)

    df_period = make_period_summary(df_result)
    df_teacher = make_teacher_summary(df_result)

    total_cnt = len(df_result)
    teacher_cnt = df_result["상대 선생님"].nunique()
    period_cnt = df_result["교시"].nunique()

    # -----------------------------
    # 상단 요약 카드
    # -----------------------------
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("총 교체 가능 시간", total_cnt)
    with m2:
        st.metric("참여 가능 선생님 수", teacher_cnt)
    with m3:
        st.metric("가능한 교시 종류", period_cnt)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # 2단 대시보드 레이아웃
    # -----------------------------
    left, right = st.columns([1.7, 1.15], gap="large")

    with left:
        st.markdown(
            '<div class="section-title">📋 상세 결과</div>'
            '<div class="section-caption">요일 → 교시 → 선생님 순으로 정렬된 전체 결과입니다.</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_result, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">🪄 카드형 빠른 보기</div>'
            '<div class="section-caption">한눈에 보기 쉽게 카드 형태로도 제공합니다.</div>',
            unsafe_allow_html=True,
        )

        card_cols = st.columns(3)
        for idx, row in df_result.iterrows():
            with card_cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-card-top">교체 가능 슬롯</div>
                        <div class="result-card-main">{row['요일']} · {row['교시']}교시</div>
                        <div class="result-card-sub">👩‍🏫 {row['상대 선생님']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with right:
        st.markdown(
            '<div class="section-title">⏰ 교시별 요약</div>'
            '<div class="section-caption">각 교시에 누가 가능한지 빠르게 확인할 수 있습니다.</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_period, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">👩‍🏫 선생님별 요약</div>'
            '<div class="section-caption">각 선생님이 가능한 시간을 묶어서 보여줍니다.</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_teacher, use_container_width=True, hide_index=True)

        with st.expander("텍스트로 간단히 보기"):
            for _, row in df_teacher.iterrows():
                st.write(f"- **{row['상대 선생님']}**: {row['가능한 시간']}")


if __name__ == "__main__":
    main()