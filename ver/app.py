import csv
import streamlit as st
import pandas as pd

# =====================================
# 0. 간단 스타일(CSS) 적용
# =====================================
CUSTOM_CSS = """
<style>
/* 전체 글자 크기 조금 줄이기 */
body, .stMarkdown, .stDataFrame, .stTable {
    font-size: 14px;
}

/* 표 헤더 진하게 */
.dataframe thead tr th {
    font-weight: 600;
}

/* 줄무늬 표 */
.dataframe tbody tr:nth-child(odd) {
    background-color: #f9fafb;
}

/* 사이드바 글자 크기 */
section[data-testid="stSidebar"] * {
    font-size: 14px;
}

/* 표 모든 셀 가운데 정렬 */
table td, table th {
    text-align: center !important;
}

/* 데이터프레임의 내부 테이블도 강제 정렬 */
[data-testid="stDataFrame"] div div table td {
    text-align: center !important;
}
[data-testid="stDataFrame"] div div table th {
    text-align: center !important;
}
</style>
"""

# =====================================
# 1. 데이터 불러오기
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

    # 첫 열: 선생님 이름 (0번째는 헤더라서 1행부터)
    name_list = [row[0] for row in data[1:]]
    return data, name_list


def find_exchange_slots(
    data,
    teacher_name: str,
    selected_date: str,
    selected_class: str,
):
    """
    기존 Tkinter 코드 conclude() 로직을 그대로 옮긴 함수.
    교체 가능한 (요일, 상대 선생님 이름, 교시) 리스트를 리턴.
    """
    if data is None:
        return []

    date_list = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    # 전체 선생님 이름 컬럼
    column = [row[0] for row in data]

    # --- 선택한 선생님의 행 index 찾기 ---
    name_index = None    # <- None으로 초기화 해야 안전
    for i in range(len(column)):
        if teacher_name == column[i]:
            name_index = i
            break

    if name_index is None:
        return []

    # --- 선택한 반이 들어 있는 열 index들 찾기 (최대 35교시) ---
    class_index_list = []
    for j in range(1, 36):
        if j < len(data[name_index]) and selected_class == data[name_index][j]:
            class_index_list.append(j)

    results = []

    # --- 각 수업 시간(class_index)에 대해 교체 가능한 상대 찾기 ---
    for class_idx in class_index_list:
        class_num = class_idx

        # 열 번호에 따라 요일 계산
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

        # 사용자가 선택한 요일과 다르면 패스
        if selected_date != date:
            continue

        # 이 요일(k)에 대해서 다른 선생님들 탐색
        for k in range(len(date_list)):  # 0~4: 월~금
            day_name = date_list[k]

            for i in range(1, len(column)):  # 1행부터: 실제 선생님
                other_teacher = column[i]
                if other_teacher == teacher_name:
                    continue

                # 이 선생님의 해당 요일(7교시 분량) 범위
                for m in range(7 * k + 1, 7 * k + 8):
                    if m >= len(data[i]) or class_idx >= len(data[i]) or class_idx >= len(data[name_index]):
                        continue

                    # 같은 반을 가르치고 있는 시간인지 확인
                    if data[i][m] == selected_class:
                        # 서로 빈 시간인지 확인
                        if data[i][class_idx] == "" and data[name_index][m] == "":
                            # 교시 계산 (1~7교시)
                            period = 7 if m % 7 == 0 else m % 7
                            results.append((day_name, other_teacher, period))

    return results


# =====================================
# 2. Streamlit UI
# =====================================
def main():
    st.set_page_config(page_title="수업 교체 가능 시간표", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.title("📚 수업 교체 가능 시간 조회")
    st.caption("CSV 시간표를 기반으로 교체 가능한 선생님과 교시를 찾아줍니다.")

    csv_filename = "기초시간표.csv"

    data, name_list = load_timetable(csv_filename)

    if data is None:
        st.stop()

    # ---- 사이드바: 검색 조건 ----
    with st.sidebar:
        st.header("🔧 조건 선택")

        teacher_name = st.selectbox("본인 이름을 선택하세요.", options=name_list)

        selected_date = st.selectbox(
            "요일을 선택하세요.",
            options=["월요일", "화요일", "수요일", "목요일", "금요일"],
        )

        selected_class = st.selectbox(
            "반을 선택하세요.",
            options=["1학년1반", "1학년2반", "1학년3반", "1학년4반", "2학년1반", "2학년2반", "2학년3반", "2학년4반"],
        )

        search_button = st.button("🔍 교체 가능 시간 찾기")

    # ---- 상단 정보 카드 ----
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("선택한 선생님", teacher_name)
    with col_info2:
        st.metric("요일", selected_date)
    with col_info3:
        st.metric("반", selected_class)

    st.markdown("---")

    if search_button:
        results = find_exchange_slots(
            data=data,
            teacher_name=teacher_name,
            selected_date=selected_date,
            selected_class=selected_class,
        )

        if not results:
            st.warning("❌ 교체 가능한 시간이 없습니다.")
            return

        # 튜플 리스트 → DataFrame
        df_result = pd.DataFrame(results, columns=["요일", "상대 선생님", "교시"])
        weekday_order = ["월요일", "화요일", "수요일", "목요일", "금요일"]

        df_result["요일"] = pd.Categorical(
            df_result["요일"],
            categories=weekday_order,
            ordered=True
        )

        # 요일 → 교시 → 상대 선생님 순으로 다시 정렬
        df_result = df_result.sort_values(["요일", "교시", "상대 선생님"]).reset_index(drop=True)


        total_cnt = len(df_result)

        # 요약 카드
        st.subheader("✅ 검색 결과 요약")
        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.metric("총 교체 가능 시간 수", total_cnt)
        with col_sum2:
            st.metric("참여 가능 선생님 수", df_result["상대 선생님"].nunique())

        st.markdown("---")

        # 🔹 탭으로 결과 보기 나누기
        tab1, tab2, tab3 = st.tabs(["📋 표 형식 보기", "⏰ 교시별 요약", "👩‍🏫 선생님별 요약"])

        # =======================
        # 탭 1: 표 형식 보기
        # =======================
        with tab1:
            st.markdown("#### 📋 상세 표")
            st.caption("요일-교시-선생님 순으로 정렬된 전체 교체 가능 시간입니다.")
            st.table(
                df_result
            )

        # =======================
        # 탭 2: 교시별 요약
        # =======================
        with tab2:
            st.markdown("#### ⏰ 교시별 요약")
            st.caption("각 교시에 교체 가능한 선생님 목록을 요약해서 보여줍니다.")

            # 교시별 : 해당 교시에 가능한 선생님 리스트
            grouped = (
                df_result
                .groupby("교시")["상대 선생님"]
                .apply(lambda s: ", ".join(sorted(set(s))))
                .reset_index()
                .sort_values("교시")
            )
            grouped.rename(columns={"교시": "교시", "상대 선생님": "교체 가능한 선생님들"}, inplace=True)

            st.table(grouped)

        # =======================
        # 탭 3: 선생님별 요약
        # =======================
        with tab3:
            st.markdown("#### 👩‍🏫 선생님별 요약")
            st.caption("각 선생님이 교체 가능한 요일/교시 목록을 한 줄로 요약합니다.")

            df_teacher = (
                df_result
                .groupby("상대 선생님")
                .apply(lambda g: ", ".join(
                    f"{row['요일']} {row['교시']}교시" for _, row in g.sort_values(["요일", "교시"]).iterrows()
                ))
                .reset_index(name="가능한 시간")
                .sort_values("상대 선생님")
            )

            st.table(
                df_teacher
            )

            st.markdown("### 📌 텍스트로도 보기")
            for _, row in df_teacher.iterrows():
                st.write(f"- **{row['상대 선생님']}**: {row['가능한 시간']}")


if __name__ == "__main__":
    main()
