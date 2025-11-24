import csv
import streamlit as st

# -----------------------------
# 1. 데이터 불러오기
# -----------------------------
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
    기존 Tkinter 코드의 conclude() 로직을 그대로 옮긴 함수.
    교체 가능한 (요일, 상대 선생님 이름, 교시) 리스트를 리턴.
    """
    if data is None:
        return []

    date_list = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    # 전체 선생님 이름 컬럼
    column = [row[0] for row in data]

    # --- 선택한 선생님의 행 index 찾기 ---
    name_index = None
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


# -----------------------------
# 2. Streamlit UI
# -----------------------------
def main():
    st.set_page_config(page_title="수업 교체 가능 시간표", layout="wide")

    st.title("📚 수업 교체 가능 시간 조회")
    st.caption("CSV 시간표를 기반으로 교체 가능한 선생님과 교시를 찾아줍니다.")

    csv_filename = "기초시간표.csv"

    data, name_list = load_timetable(csv_filename)

    if data is None:
        st.stop()

    # ---- 입력 영역 ----
    with st.sidebar:
        st.header("🔧 조건 선택")

        teacher_name = st.selectbox("본인 이름을 선택하세요.", options=name_list)

        selected_date = st.selectbox(
            "요일을 선택하세요.",
            options=["월요일", "화요일", "수요일", "목요일", "금요일"],
        )

        # 기존 코드에 맞춰 반 목록 고정
        selected_class = st.selectbox(
            "반을 선택하세요.",
            options=["1학년1반", "1학년2반", "1학년3반", "1학년4반"],
        )

        search_button = st.button("🔍 교체 가능 시간 찾기")

    # ---- 메인 영역 ----
    st.subheader("🗓 선택한 조건")
    st.write(f"- 선생님: **{teacher_name}**")
    st.write(f"- 요일: **{selected_date}**")
    st.write(f"- 반: **{selected_class}**")

    st.markdown("---")

    if search_button:
        results = find_exchange_slots(
            data=data,
            teacher_name=teacher_name,
            selected_date=selected_date,
            selected_class=selected_class,
        )

        if not results:
            st.warning("교체 가능한 시간이 없습니다.")
        else:
            st.success(f"총 **{len(results)}개**의 교체 가능 시간이 있습니다.")
            # 표로 보기 좋게 정리
            df_result = (
                # (요일, 선생님, 교시) 튜플 리스트 → DataFrame
                # 예: [("월요일", "홍길동", 3), ...]
                # 컬럼명: 요일, 상대 선생님, 교시
                # 정렬까지
                __import__("pandas")
                .DataFrame(results, columns=["요일", "상대 선생님", "교시"])
                .sort_values(["요일", "교시", "상대 선생님"])
            )
            st.dataframe(df_result, use_container_width=True)

            # 문장으로도 출력
            st.markdown("### 📋 상세 목록")
            for day, other_teacher, period in results:
                st.write(f"- {day} {other_teacher} 선생님의 **{period}교시**와 교체 가능합니다.")


if __name__ == "__main__":
    main()
