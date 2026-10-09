
import pymysql
import pandas as pd
import streamlit as st
from google import genai
from google.genai import types

def query_database(sql_query: str):
    """Thực thi câu lệnh SQL lấy số liệu thống kê."""
    db_config = st.secrets["mysql"]
    conn = pymysql.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        port=db_config.get("port", 3306),
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
        return pd.DataFrame(result)
    finally:
        conn.close()


# Cấu hình giao diện chuẩn cho điện thoại
st.set_page_config(page_title="Trợ Lý Tự Động Hóa", page_icon="⚡", layout="centered")

st.title("⚡ Trợ Lý Công Việc Tự Động")
st.caption("Xử lý Code, Kịch bản Video & Tự động hóa Facebook")

# Lấy API Key: ưu tiên lấy từ Secrets, nếu chưa có thì lấy từ ô nhập
api_key_from_secrets = st.secrets.get("GEMINI_API_KEY", "")
api_key = api_key_from_secrets if api_key_from_secrets else st.sidebar.text_input("Nhập Gemini API Key:", type="password")

# Chọn 1 trong 3 nhóm công việc
task = st.selectbox(
    "Chọn công việc cần làm:",
    [
        "1. Lập trình (Sửa bug, Tối ưu SQL, Thống kê)",
        "2. Kịch bản Video ngắn & Prompt Video AI",
        "3. Tự động hóa Facebook (Script Python)"
    ]
)

# Chỉ dẫn nghiệp vụ cho từng tác vụ
instructions = {
    "1. Lập trình (Sửa bug, Tối ưu SQL, Thống kê)": (
        "Bạn là chuyên gia lập trình. Hãy kiểm tra lỗi, tối ưu truy vấn SQL hoặc "
        "viết hàm thống kê. Đưa ra code chuẩn, giải thích ngắn gọn nguyên nhân."
    ),
    "2. Kịch bản Video ngắn & Prompt Video AI": (
        "Bạn là nhà sáng tạo nội dung triệu view. Hãy viết kịch bản video ngắn "
        "(Hook 3s, Body, CTA) và cung cấp kèm Prompt tiếng Anh chi tiết để tạo video bằng AI."
    ),
    "3. Tự động hóa Facebook (Script Python)": (
        "Bạn là kỹ sư tự động hóa. Hãy viết mã nguồn Python hoàn chỉnh dùng Facebook Graph API "
        "để đăng video/bài viết, xử lý lỗi chi tiết và hướng dẫn cấu hình token."
    )
}

# Khung nhập yêu cầu
user_prompt = st.text_area(
    "Nhập nội dung hoặc yêu cầu của bạn:",
    height=150,
    placeholder="Ví dụ: Viết kịch bản video 30s về mẹo dùng iPhone..."
)

# Nút thực hiện
if st.button("🚀 Bắt đầu xử lý", type="primary", use_container_width=True):
    if not api_key:
        st.warning("Vui lòng cấu hình GEMINI_API_KEY trong Secrets hoặc nhập ở thanh bên trái.")
    elif not user_prompt.strip():
        st.warning("Vui lòng nhập nội dung yêu cầu.")
    else:
        with st.spinner("Đang xử lý dữ liệu..."):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=instructions[task]
                    )
                )
                st.success("Hoàn thành!")
                st.markdown("### Kết quả:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")
