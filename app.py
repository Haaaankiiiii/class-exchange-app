import csv
import streamlit as st
import pandas as pd

# =====================================
# 0. 페이지 설정
# =====================================
st.set_page_config(
    page_title="수업 교체 가능 시간표",
    page_icon="📚",
    layout="wide",
)

# =====================================
# 1. 커스텀 CSS
# =====================================
CUSTOM_CSS = """
<style>
/* 전체 배경 */
.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
}

/* 메인 레이아웃 폭/여백 */
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* 기본 텍스트 */
html, body, [class*="css"]  {
    font-size: 15px;
    color: #0f172a;
}

/* 제목 */
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}

.sub-title {
    font-size: 1rem;
    color: #475569;
    margin-bottom: 1.3rem;
}

/* 공통 카드 */
.card {
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(10px);
    border: 1px solid #e2e8f0;
    border-radius: 22px;
    padding: 20px 22px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    margin-bottom: 18px;
}

/* 필터 카드 */
.filter-card {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(12px);
    border: 1px solid #dbeafe;
    border-radius: 24px;
    padding: 18px 20px 14px 20px;
    box-shadow: 0 12px 32px rgba(37, 99, 235, 0.08);
    margin-bottom: 18px;
}

/* 섹션 제목 */
.section-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.4rem;
}

.section-caption {
    font-size: 0.92rem;
    color: #64748b;
    margin-bottom: 0.8rem;
}

/* 조회 조건 바 */
.condition-bar {
    background: linear-gradient(135deg, #eff6ff, #ffffff);
    border: 1px solid #dbeafe;
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 18px;
    color: #1e293b;
    font-size: 0.97rem;
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.06);
}

/* Metric 카드 */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.92);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 16px 18px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
}

[data-testid="metric-container"] label {
    color: #64748b !important;
    font-weight: 600;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0f172a;
    font-weight: 800;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    height: 46px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    font-weight: 800;
    font-size: 15px;
    transition: all 0.18s ease;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px rgba(37, 99, 235, 0.28);
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    color: white;
}

/* selectbox */
div[data-baseweb="select"] > div {
    min-height: 46px;
    border-radius: 14px !important;
    border: 1px solid #cbd5e1 !important;
    background: #ffffff !important;
    box-shadow: none !important;
}

label[data-testid="stWidgetLabel"] {
    font-weight: 700 !important;
    color: #334155 !important;
}

/* dataframe/table */
[data-testid="stDataFrame"] {
    background: transparent;
    border: none;
}

[data-testid="stDataFrame"] > div {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

/* html table */
table {
    border-collapse: collapse !important;
    width: 100% !important;
}

thead tr th {
    background: #f8fafc !important;
    color: #0f172a !important;
    font-weight: 800 !important;
    text-align: center !important;
    border-bottom: 1px solid #e2e8f0 !important;
}

tbody tr td {
    text-align: center !important;
    vertical-align: middle !important;
}

tbody tr:nth-child(odd) {
    background-color: #fcfdff !important;
}

/* 결과 카드 */
.slot-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 14px 16px;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
    margin-bottom: 12px;
}

.slot-label {
    font-size: 0.78rem;
    color: #64748b;
    margin-bottom: 6px;
    font-weight: 700;
}

.slot-title {
    font-size: 1.08rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}

.slot-teacher {
    font-size: 0.95rem;
    color: #334155;
}

/* 안내 카드 */
.empty-card {
    background: linear-gradient(135deg, #ffffff, #eff6ff);
    border: 1px dashed #93c5fd;
    border-radius: 24px;
    padding: 42px 28px;
    text-align: center;
    color: #334155;
    box-shadow: 0 10px 26px rgba(37, 99, 235, 0.05);
}

.empty-card .emoji {
    font-size: 2.2rem;
    margin-bottom: 10px;
}

.empty-card .title {
    font-size: 1.2rem;
    font-weight: 800;
    margin-bottom: 8px;
    color: #0f172a;
}

.empty-card .desc {
    font-size: 0.96rem;
    color: #64748b;
}

/* 구분선 */
hr {
    border: none;
    height: 1px;
    background: #e2e8f0;
    margin: 1rem 0 1.2rem 0;
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

    name_list = [row[0] for row in data[1:] if row]
    return data, name_list


def find_exchange_slots(
    data,
    teacher_name: str,
    selected_date: str,
    selected_class: str,
):
    """
    교체 가능한 (요일, 상대 선생님 이름, 교시) 리스트를 리턴.
    """
    if data is None:
        return []

    date_list = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    column = [row[0] for row in data]

    # 선택한 선생님 행 찾기
    name_index = None
    for i in range(len(column)):
        if teacher_name == column[i]:
            name_index = i
            break

    if name_index is None:
        return []

    # 선택한 반이 들어 있는 열 찾기
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

        for k in range(len(date_list)):  # 0~4
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


# =====================================
# 3. 보조 함수
# =====================================
def make_summary_tables(df_result: pd.DataFrame):
    grouped_period = (
        df_result.groupby("교시", observed=False)["상대 선생님"]
        .apply(lambda s: ", ".join(sorted(set(s))))
        .reset_index()
        .sort_values("교시")
        .rename(columns={"상대 선생님": "교체 가능한 선생님"})
    )

    grouped_teacher = (
        df_result.groupby("상대 선생님", observed=False)
        .apply(
            lambda g: ", ".join(
                f"{row['요일']} {row['교시']}교시"
                for _, row in g.sort_values(["요일", "교시"]).iterrows()
            ),
            include_groups=False
        )
        .reset_index(name="가능한 시간")
        .sort_values("상대 선생님")
    )

    return grouped_period, grouped_teacher


def render_slot_cards(df_result: pd.DataFrame, columns_count: int = 3):
    cols = st.columns(columns_count)
    for idx, row in df_result.iterrows():
        with cols[idx % columns_count]:
            st.markdown(
                f"""
                <div class="slot-card">
                    <div class="slot-label">교체 가능 슬롯</div>
                    <div class="slot-title">{row['요일']} · {row['교시']}교시</div>
                    <div class="slot-teacher">👩‍🏫 {row['상대 선생님']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =====================================
# 4. 메인 앱
# =====================================
def main():
    csv_filename = "기초시간표.csv"
    data, name_list = load_timetable(csv_filename)

    if data is None:
        st.stop()

    st.markdown('<div class="main-title">📚 수업 교체 가능 시간 조회</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">시간표를 기반으로 교체 가능한 선생님과 교시를 한눈에 확인할 수 있는 대시보드입니다.</div>',
        unsafe_allow_html=True
    )

    # 기본값
    default_teacher = name_list[0] if name_list else ""
    weekday_options = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    class_options = [
        "1학년1반", "1학년2반", "1학년3반", "1학년4반",
        "2학년1반", "2학년2반", "2학년3반", "2학년4반"
    ]

    # 검색 상태 유지
    if "searched" not in st.session_state:
        st.session_state.searched = False

    if "teacher_name" not in st.session_state:
        st.session_state.teacher_name = default_teacher

    if "selected_date" not in st.session_state:
        st.session_state.selected_date = weekday_options[0]

    if "selected_class" not in st.session_state:
        st.session_state.selected_class = class_options[0]

    # 상단 필터 바
    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([2.0, 1.2, 1.6, 1.0])

    with f1:
        teacher_name = st.selectbox(
            "선생님",
            options=name_list,
            index=name_list.index(st.session_state.teacher_name) if st.session_state.teacher_name in name_list else 0,
        )

    with f2:
        selected_date = st.selectbox(
            "요일",
            options=weekday_options,
            index=weekday_options.index(st.session_state.selected_date),
        )

    with f3:
        selected_class = st.selectbox(
            "반",
            options=class_options,
            index=class_options.index(st.session_state.selected_class),
        )

    with f4:
        st.write("")
        search_button = st.button("🔍 조회하기")

    st.markdown('</div>', unsafe_allow_html=True)

    if search_button:
        st.session_state.teacher_name = teacher_name
        st.session_state.selected_date = selected_date
        st.session_state.selected_class = selected_class
        st.session_state.searched = True

    # 검색 전 안내
    if not st.session_state.searched:
        st.markdown(
            """
            <div class="empty-card">
                <div class="emoji">🗂️</div>
                <div class="title">조건을 선택하고 조회해 보세요</div>
                <div class="desc">
                    상단에서 선생님, 요일, 반을 선택하면<br>
                    교체 가능한 시간과 상대 선생님을 대시보드 형태로 보여줍니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # 조회 실행
    results = find_exchange_slots(
        data=data,
        teacher_name=st.session_state.teacher_name,
        selected_date=st.session_state.selected_date,
        selected_class=st.session_state.selected_class,
    )

    st.markdown(
        f"""
        <div class="condition-bar">
            <b>현재 조회 조건</b> &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>선생님:</b> {st.session_state.teacher_name}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>요일:</b> {st.session_state.selected_date}
            &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>반:</b> {st.session_state.selected_class}
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

    df_result = (
        df_result.sort_values(["요일", "교시", "상대 선생님"])
        .reset_index(drop=True)
    )

    grouped_period, grouped_teacher = make_summary_tables(df_result)

    total_cnt = len(df_result)
    teacher_cnt = df_result["상대 선생님"].nunique()
    period_cnt = df_result["교시"].nunique()

    # 상단 요약 카드
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("총 교체 가능 시간", total_cnt)
    with m2:
        st.metric("참여 가능 선생님 수", teacher_cnt)
    with m3:
        st.metric("가능한 교시 수", period_cnt)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 메인 대시보드
    left, right = st.columns([1.7, 1.1], gap="large")

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 상세 결과</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">요일 → 교시 → 선생님 순으로 정렬된 전체 교체 가능 시간입니다.</div>',
            unsafe_allow_html=True
        )
        st.dataframe(
            df_result,
            use_container_width=True,
            hide_index=True,
            height=420
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🪄 빠른 카드 보기</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">표보다 더 직관적으로 보이도록 카드 형태로도 보여줍니다.</div>',
            unsafe_allow_html=True
        )
        render_slot_cards(df_result, columns_count=3)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⏰ 교시별 요약</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">각 교시에 교체 가능한 선생님을 묶어서 확인합니다.</div>',
            unsafe_allow_html=True
        )
        st.dataframe(
            grouped_period,
            use_container_width=True,
            hide_index=True,
            height=240
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">👩‍🏫 선생님별 요약</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">각 선생님이 가능한 시간대를 한 줄로 빠르게 볼 수 있습니다.</div>',
            unsafe_allow_html=True
        )
        st.dataframe(
            grouped_teacher,
            use_container_width=True,
            hide_index=True,
            height=240
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 텍스트 요약</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">간단히 읽기 좋은 형태로 정리했습니다.</div>',
            unsafe_allow_html=True
        )
        for _, row in grouped_teacher.iterrows():
            st.write(f"**{row['상대 선생님']}** · {row['가능한 시간']}")
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()